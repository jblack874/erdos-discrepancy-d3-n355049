# Erdős discrepancy: a ±1 sequence of length 355,897 with discrepancy 3

**C(3) ≥ 355,897: a SAT re-solve of the tail of the earlier 355,049-term sequence, checked by two independent exact checkers.**

AlphaEvolve Problem 6.40 asks for long ±1 sequences whose sums along every homogeneous arithmetic progression d, 2d, …, md stay within ±C. For C = 3, P. G. Prendergast posted a 355,000-term sequence on [issue #23](https://github.com/google-deepmind/alphaevolve_repository_of_problems/issues/23) and showed that one more term can always be added (C(3) ≥ 355,001). This repository first appended 49 terms to his sequence by tail backtracking (355,049, kept below as the first result). An incremental SAT re-solve of the last 5,000 positions then broke the wall at 355,050 and reached 355,897. The first 350,049 terms are still Prendergast's, unchanged.

## Current result: 355,897 (2026-11-24)

1. **Mathematical objective.** Maximize N such that x₁, …, x_N ∈ {+1, −1} satisfies |x_d + x_{2d} + … + x_{md}| ≤ 3 for every d ≥ 1 and every md ≤ N.
2. **Baseline.** 355,049 (this repository, first result, posted on issue #23 on 2026-11-24). Before that, 355,001 (Prendergast).
3. **Candidate result.** N = 355,897 (+848 over 355,049, +896 over 355,001). `certificate/erdos_d3_n355897_signs.txt`, SHA-256 `b5419d58…4922`.
4. **Verification.** Exact integer arithmetic, the same two independent checkers (`checkers/edp_checkA.py`, `checkers/edp_checkB.c`). Both pass at discrepancy 3, and both reject a control with the first sign flipped (discrepancy 5). See `logs/checkers_355897.log` and `manifest_n355897.json`. Mathbox computation-audit: finite assertion verified in the stated range.
5. **Record eligibility.** Venue: the issue #23 thread, which has no minimum step. Same file format (one line of `+`/`-`, no newline). Bar re-scanned 2026-11-24 17:02 UTC: highest claim in the thread was 355,049.
6. **Novelty.** Improved construction. The method (SAT on a sliding window of free positions) is standard. Literature check: apparently new within the stated scope (issue #23 thread and a web search).
7. **Search economics.** One CaDiCaL run (window 4,000 after starting at 2,000) gave all 848 terms in 48.5 minutes on one core: 848 satisfiable solves, 2 unsatisfiable, about 17.5 terms per minute. Two side runs (windows 5,000 and 8,000) reached 355,676 and 355,466.
8. **Decision.** Continue. The run stopped at its time limit, not at a wall.

| Quantity | Value |
|---|---|
| Length | 355,897 |
| Discrepancy (max over all d, m) | 3 |
| First terms identical to Prendergast's sequence | 350,049 |
| Positions 350,050–355,049 changed from the 355,049 certificate | 1,010 |
| Gain over 355,049 | +848 |

### Run the SAT search

```sh
pip install python-sat
python3 search/edp_sat.py certificate/erdos_d3_n355049_signs.txt out 2000 5000 1000 120 2900 cadical195
```

Arguments: input signs, output folder, window min, window max, window step, per-solve seconds (CaDiCaL ignores this limit), total seconds, solver. Each progression gets a 7-state one-hot walk over partial sums −3..3. Positions up to N − W are fixed by assumptions, the length grows by one per satisfiable solve, phases start from the current signs, and the window widens on an unsatisfiable or timed-out solve. Logs of the three runs are in `logs/sat_*.log`.

## First result: 355,049 (tail backtrack)


1. **Mathematical objective.** Maximize N such that x₁, …, x_N ∈ {+1, −1} satisfies |x_d + x_{2d} + … + x_{md}| ≤ 3 for every d ≥ 1 and every md ≤ N. C(3) is the largest such N (AlphaEvolve notation).
2. **Baseline.** 355,000 (Prendergast, issue #23, gist [rev 98bc47d8](https://gist.github.com/pgprendergast/9e2c6d24cf0c28b569990bddb95adf07), SHA-256 `a04938ea…adcb`), extended to 355,001 by his parity argument (11/23/2026). The best published value is 127,645 (Konev–Lisitsa 2014; Le Bras–Gomes–Selman 2014).
3. **Candidate result.** N = 355,049 (+48 over 355,001, +49 over 355,000). `certificate/erdos_d3_n355049_signs.txt`, SHA-256 `a7407cde…7598`. A second, different 49-term tail of the same length is in `erdos_d3_n355049_signs_alt.txt`.
4. **Verification.** Exact integer arithmetic, two independent checkers (`checkers/edp_checkA.py`, NumPy cumulative sums; `checkers/edp_checkB.c`, plain C loops). Both pass both certificates at discrepancy 3, both reproduce the 355,000 record, both pass the two 355,001 extensions (confirming the parity argument), and both reject a control with the first sign flipped (discrepancy 5). Mathbox computation-audit: finite assertion verified in the stated range.
5. **Record eligibility.** Venue: the issue #23 thread, which has no minimum step. The certificate uses Prendergast's file format (one line of `+`/`-`, no newline). Bar re-scanned 2026-11-24 09:31 CT.
6. **Novelty.** Improved construction, not new technique. Literature check: apparently new within the stated scope (issue #23 thread, the AlphaEvolve repository, a web search covering arXiv 2511.02864, 1405.3097 and 1407.2510). Other venues were not checked.
7. **Search economics.** Two runs of 55 s on one core each (2 cores total), about 3.5 × 10⁹ search nodes per run. Both runs reached 355,049 and stalled there. Gain about 52 terms per wall-clock minute.
8. **Decision.** Modify the method. The wall is described under Honest limits; the next step is a SAT re-solve of the last few thousand positions, seeded with these signs.

### Numbers

| Quantity | Value |
|---|---|
| Length | 355,049 |
| Discrepancy (max over all d, m) | 3 |
| Terms changed from Prendergast's 355,000 | 0 |
| Terms appended | 49 |
| Gain over the 355,001 bar | +48 |
| Blocked position | 355,050 = 2·3³·5²·263 (48 divisors) |
| Clash at 355,050 | S₄₅ = +3; S₉ = S₂₆₃ = −3 |

## Verification rules

- A file passes only if every partial sum along every progression d, 2d, 3d, … up to N lies in [−3, 3].
- Both checkers must pass. They share no code with each other or with the search.
- Each checker must reproduce Prendergast's 355,000 record before it is trusted, and must reject a perturbed copy.

## Honest limits

- The 355,897 sequence changes 1,010 of the last 5,000 terms of the 355,049 certificate, so it no longer extends Prendergast's full 355,000 terms; it agrees with them on the first 350,049.
- The SAT search was stopped by its time limit at 355,897; how far it can go is untested.
- The gain is small and comes from extending the tail only. Prendergast reported the same pattern (a night of tail extension moved 255,000 to 257,799); his larger gains came from re-solving with the multiplicative rules.
- The search stalls at 355,050. Its progression sums for d = 45 (+3) and d = 9, 263 (−3) force opposite signs. The terms that set those sums (355,005, 355,041 and 354,787) all lie inside the search window, so the block can be broken in principle, but chronological backtracking does not find the way out in these runs.
- No Lean proof. The claim rests on the two checkers.
- The novelty scope is limited to the sources listed in item 6.

## Run it

```sh
python3 checkers/edp_checkA.py certificate/erdos_d3_n355897_signs.txt 3
cc -O2 -o checkB checkers/edp_checkB.c && ./checkB certificate/erdos_d3_n355897_signs.txt 3
python3 checkers/edp_checkA.py certificate/erdos_d3_n355049_signs.txt 3
./checkB certificate/erdos_d3_n355049_signs.txt 3
sha256sum -c SHA256SUMS
```

Expected: `discrepancy=3 ... PASS` from both checkers, in about 1.5 s (A) and 0.02 s (B).

To repeat the search from Prendergast's file (`erdos_d3_n355000_signs.txt` from his gist):

```sh
cc -O3 -o edp_tail search/edp_tail.c
./edp_tail erdos_d3_n355000_signs.txt 3 2000 1 55 out.txt
```

Arguments: input, C, window W (positions after N − W may change), seed, seconds, output.

## How it works

| Piece | Where |
|---|---|
| Certificate (355,897 signs, current) | `certificate/erdos_d3_n355897_signs.txt` |
| Certificate (355,049 signs) | `certificate/erdos_d3_n355049_signs.txt` |
| Alternate certificate (different tail) | `certificate/erdos_d3_n355049_signs_alt.txt` |
| Checker A (NumPy) | `checkers/edp_checkA.py` |
| Checker B (C) | `checkers/edp_checkB.c` |
| Tail backtrack search | `search/edp_tail.c` |
| SAT window search | `search/edp_sat.py` |
| Search and checker logs | `logs/` |
| Computation manifests (Mathbox) | `manifest.json` (355,049), `manifest_n355897.json` (355,897) |
| Checksums | `SHA256SUMS` |

## Method

1. Fix positions 1 to N − W of Prendergast's sequence and load every progression's partial sum up to that point.
2. Run a depth-first search from N − W + 1. At each position n, try the original sign first where one exists; past the end, try the sign that pulls the sum of n's divisor progressions toward 0. A sign is allowed only if every progression through n stays within ±3. Backtrack chronologically.
3. Keep the longest prefix reached. Runs with W = 2,000 and W = 20,000 both reached 355,049 with different tails.

## Stack

C (gcc -O3) for the backtrack search and checker B; Python 3 with NumPy for checker A; Python 3 with PySAT and CaDiCaL 1.9.5 for the SAT search. Two to four CPU cores.

## Sources and credit

- P. G. Prendergast, issue [#23](https://github.com/google-deepmind/alphaevolve_repository_of_problems/issues/23) on google-deepmind/alphaevolve_repository_of_problems, and the 355,000-term sequence in his [gist](https://gist.github.com/pgprendergast/9e2c6d24cf0c28b569990bddb95adf07) (revision 98bc47d8). The first 355,000 terms of the 355,049 certificate and the first 350,049 terms of the 355,897 certificate are his, unchanged.
- A. Ignatiev, A. Morgado, J. Marques-Silva, PySAT; A. Biere et al., CaDiCaL.
- B. Konev, A. Lisitsa, *Computer-aided proof of Erdős discrepancy properties*, arXiv:1405.3097.
- R. Le Bras, C. P. Gomes, B. Selman, *On the Erdős discrepancy problem*, arXiv:1407.2510.
- B. Georgiev et al., *Mathematical exploration and discovery at scale* (AlphaEvolve), arXiv:2511.02864, Problem 6.40.

Prepared with AI assistance (Claude, Anthropic).
