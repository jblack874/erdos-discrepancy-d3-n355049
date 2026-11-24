#!/usr/bin/env python3
# Checker A (numpy): max over d>=1, m>=1 of |sum_{j<=m} x_{jd}| for a +/- string file. usage: edp_checkA.py file [C]
import sys, numpy as np
s = open(sys.argv[1], 'rb').read().strip()
C = int(sys.argv[2]) if len(sys.argv) > 2 else 3
assert set(s) <= {ord('+'), ord('-')}, "bad characters"
x = np.where(np.frombuffer(s, dtype=np.uint8) == ord('+'), 1, -1).astype(np.int64)
N = len(x); worst = 0; wd = 0
for d in range(1, N + 1):
    m = np.abs(np.cumsum(x[d-1::d])).max()
    if m > worst: worst, wd = int(m), d
print(f"checkA N={N} discrepancy={worst} (first worst d={wd}) {'PASS' if worst <= C else 'FAIL'} at C={C}")
sys.exit(0 if worst <= C else 1)
