#!/usr/bin/env python3
# Incremental SAT extension of a discrepancy-C +/- sequence.
# usage: edp_sat.py signs.txt outdir Wmin Wmax Wstep per_solve_seconds total_seconds [solver]
import sys, time, threading, os
import numpy as np
from pysat.solvers import Solver

sig, outdir = sys.argv[1], sys.argv[2]
Wmin, Wmax, Wstep = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
per_solve, total = float(sys.argv[6]), float(sys.argv[7])
sname = sys.argv[8] if len(sys.argv) > 8 else 'cadical195'
C = 3
T0 = time.time()
s = open(sig, 'rb').read().strip()
x = [0] + [1 if c == ord('+') else -1 for c in s]
N = len(x) - 1
LMAX = N + 20000
B = N - Wmax  # positions 1..B are constants
# divisors sieve up to LMAX for positions > B
divs = {p: [] for p in range(B + 1, LMAX + 1)}
for d in range(1, LMAX + 1):
    start = ((B // d) + 1) * d
    for p in range(start, LMAX + 1, d):
        divs[p].append(d)
# prefix sums of progression d over multiples <= B
xs = np.array(x, dtype=np.int64)
init = {}
for d in range(1, B + 1):
    init[d] = int(xs[d:B + 1:d].sum())
nv = [0]
def new():
    nv[0] += 1
    return nv[0]
xv = {p: new() for p in range(B + 1, LMAX + 1)}
TRUE = new()
solver = Solver(name=sname)
solver.add_clause([TRUE])
last = {}  # d -> list of 7 state vars (index v+3) or ('const', v)
def add_pos(p):
    xp = xv[p]
    for d in divs[p]:
        prev = last.get(d)
        if prev is None:
            prev = ('const', init.get(d, 0))
        new_state = [new() for _ in range(7)]
        if prev[0] == 'const':
            v = prev[1]
            pairs = [(None, v)]
        else:
            pairs = [(prev[1][v + 3], v) for v in range(-C, C + 1)]
        for lit, v in pairs:
            pre = [] if lit is None else [-lit]
            if v < C:
                solver.add_clause(pre + [-xp, new_state[v + 4]])
            else:
                solver.add_clause(pre + [-xp])
            if v > -C:
                solver.add_clause(pre + [xp, new_state[v + 2]])
            else:
                solver.add_clause(pre + [xp])
        last[d] = ('vars', new_state)

def solve(assum, limit):
    t = threading.Timer(limit, solver.interrupt)
    t.start()
    r = solver.solve_limited(assumptions=assum, expect_interrupt=True)
    t.cancel()
    try:
        solver.clear_interrupt()
    except NotImplementedError:
        pass
    return r

for p in range(B + 1, N + 1):
    add_pos(p)
# phases: current signs
solver.set_phases([xv[p] if x[p] > 0 else -xv[p] for p in range(B + 1, N + 1)])
W = Wmin
L = N
best = N
log = open(os.path.join(outdir, 'sat.log'), 'a')
def P(*a):
    msg = ' '.join(str(z) for z in a)
    print(msg, flush=True); log.write(msg + '\n'); log.flush()
P(f'start N={N} B={B} Wmin={Wmin} Wmax={Wmax} solver={sname} vars={nv[0]} build={time.time()-T0:.1f}s')
cur = list(x)  # current best assignment for positions 1..L
while time.time() - T0 < total and L < LMAX:
    add_pos(L + 1)
    while True:
        assum = [xv[p] if cur[p] > 0 else -xv[p] for p in range(B + 1, L + 1 - W)] if L + 1 - W > B else []
        t1 = time.time()
        r = solve(assum, min(per_solve, max(1, total - (time.time() - T0))))
        dt = time.time() - t1
        if r is True:
            m = solver.get_model()
            mm = set(l for l in m if l > 0)
            L += 1
            cur = cur[:B + 1] + [1 if xv[p] in mm else -1 for p in range(B + 1, L + 1)]
            if L > best:
                best = L
                open(os.path.join(outdir, 'best_signs.txt'), 'w').write(''.join('+' if v > 0 else '-' for v in cur[1:]))
                changed = sum(1 for p in range(B + 1, N + 1) if cur[p] != x[p])
                P(f'SAT L={L} W={W} solve={dt:.2f}s changed_vs_orig={changed} t={time.time()-T0:.0f}s')
            break
        else:
            P(f'{"UNSAT" if r is False else "TIMEOUT"} at L={L+1} W={W} solve={dt:.1f}s t={time.time()-T0:.0f}s')
            if W >= Wmax or time.time() - T0 > total:
                P(f'stop best={best}')
                sys.exit(0)
            W = min(Wmax, W + Wstep)
P(f'end best={best} t={time.time()-T0:.0f}s')
