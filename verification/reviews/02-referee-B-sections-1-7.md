# Referee report B: Sections 1–7 (W-product lower bound) and the binary-monomial generalization

## 1. Verdicts
- Part 1 (the W-product manuscript of 1 November 2026, with its sketch): ACCEPT WITH CORRECTIONS — minor wording/notation; no gap, no error.
- Part 2 (binary-monomial theorem, both bounds; families/monomial-products/proofs/*, paper/): ACCEPT WITH CORRECTIONS —
  minor notation/explicitness; no gap, no error.

## 2. Theorems verified
T1 (00_introduction.tex:36-42): k>=2, d_i>=3, over C: least r with prod x_i^{d_i-1} y_i = sum_{l<=r} c_l prod
(a_il x_i + b_il y_i)^{d_i} is M = 2^{k-1}(sum d_i - 2k + 2); new part r >= M for every complex decomposition; upper bound
CCS arXiv:2512.05828 Thm 1.1 (abstract confirms the bound; range from the citation). The argument proves
r >= 2^k + 2^{k-1} sum(d_i-2) for all k>=1, d_i>=2.
T2 (paper/main.tex:75-88, STATEMENT.md:68-82): k>=1, a_i>=b_i>=1: R(prod x^{a_i} y^{b_i}) = N = prod(b_i+1) +
sum (a_i-b_i) prod_{j!=i}(b_j+1).
T2' (lower_bound.tex:8-38): b_i>=1, d_i>=2b_i, m_i(z^e)=0 for b_i<e<=d_i, m_i(z^{b_i})!=0, full-box product moments,
nonzero complex weights => n >= prod q_i + sum (d_i-2b_i) prod_{j!=i} q_j, q_i=b_i+1.
Reductions: b_i=1, a_i=d_i-1 -> M; k=1 -> a+1; k=2 -> (a_1+1)(a_2+1)-(a_1-b_1)(a_2-b_2) (= Galazka bound quoted);
(3,2)^3 -> 54, (2,1)^3 -> 20, (2,1)^2 -> 8; (a_i+1) prod_{j!=i} q_j <= N <= prod(a_i+1).
Independent pre-reading sketch (affine-chart normalization -> full-box product moments -> rank of bilinear Gram
E^T W E; denominators (1+t_i z_i)^{-s} kill moments of degree in (b_i,d_i]; orthogonal + anti-triangular blocks; leading
term as t_i -> infinity) matches the written route.

## 3. Step tables
Part 1: 1 definitions/target/cited bound 00:13-29 OK; 2 choice of gamma_i 01:22-26 OK (unimodular, term count kept);
3 normalized identity 01:11-29 minor ("w_l != 0" needs c_l != 0); 4 full-box moments + converse 02:3-28 minor (division by
binom(d,e) implicit); 5 linear extension/product rule 03:12-29 OK; 6 Gram coefficients, G=E^T W E 04:3-55 OK; 7 G
invertible => rank E = M => r >= M 05:7-19 OK; 8 B_0, B_i, count M 06:8-47 OK; 9 G_0 Kronecker, det G_i=-beta^2
06:88-99 OK (mod p); 10 cross blocks vanish 06:101-107 + App A minor (B_i-B_j j-th factor only in (A.2)); 11
anti-triangular, det G_i = ±(det H_i)^{d_i-2} 06:142-186 OK; 12 Laurent leading term 06:192-212 + App B OK (wording);
13 one finite t 06:214-232 OK; 14 theorem proof 06:260-270 OK; 15 Example 6.4 OK (|det C| = 3^{-12}); 16 sketch OK.
Part 2: statement/specializations OK; pairing over C(t), lists U, V_i OK; U Gram Kronecker, det = ±beta^q OK;
orthogonality OK; anti-triangular V_i OK (letter clash a); identity (4) exact (b>=1 at z=0) OK; leading term
(-1)^{d-b} beta t^{-(d-b+1)} (x) G_j, det H_i != 0 OK; finite t and count OK/minor (PROOF.md numerators); reduction
m_i(z^e) OK (two ways); det A = N, index N OK; lattice misses box except 0 OK (incl. delta_i=0); character
orthogonality, identity (9) OK; main proof, Cor. W OK; literature not verified.

## 4. Corrections
Part 1:
1. 01_coordinates.tex:25-26: "Because zero summands were deleted, every c_l != 0 and every pair (a_il,b_il) != (0,0);
   hence every w_l != 0"; replace "each nonzero factor" by "each pair (a_il,b_il) != (0,0) (none is excluded when b_il = 0)".
2. 02_moments.tex:23-25: "...gives gamma_i, 1, 0 for e_i = 0, 1, >=2; after division by binom(d_i,e_i) these are gamma_i,
   beta_i = 1/d_i, 0; on the right, (X+zY)^d contributes binom(d,e) z^e."
3. (optional) 02_moments.tex:21: division applied to both sides.
4. 06_test_functions.tex:105-107: add "and the j-th factor Z_j^{s'+iota_j} h_j^{d_j-s'-1} is a polynomial of degree
   <= d_j (see (A.2))."
5. 06_test_functions.tex:194: "with the other parameters fixed" -> "for arbitrary fixed t_j (j != i); H_i is polynomial in
   t_j"; end of proof: "a rational function that is nonzero on one such line is nonzero."
6. (optional) 06_test_functions.tex:221-222: D_i = prod_l (1+t_i z_il)^q, N_i = D_i det H_i.
7. B_laurent.tex:56,78: rename summation index a -> n.
8. sketch/pre.tex:22-25: delete unused author macros (superscript 3 conflicts with "2" in the sketch header).
Part 2:
9. PROOF.md:133-135: name P_i = D_i^{r_i} det H_i with D_i = prod_l h_{i,l} (as lower_bound.tex:266-273).
10. lower_bound.tex:189-191: offset "s = b_i+1+a" reuses a; use c, c'.
11. upper_bound.tex:62, PROOF.md:204: "H = -S" clashes with group H and H_i; use sigma.
12. upper_bound.tex:130-139: exponent vector m clashes with m_i and cyclic orders m_j; use e.
13. (optional) PROOF.md:40-48 vs 125: r and r_i share a letter.

## 5. Independent tests
A character decompositions (exact vs cyclotomic polynomial; group size = det A = N): (2,2;1,1) 8; (2,2,2;1,1,1) 20;
(3,3,3;2,2,2) 54; (3,4;1,1) 14; (2,2,2,2;1,1,1,1) 48; (4,3,2;2,1,2) 48; (5;2) 6; (2,1;2,1) 6; (3,2,5;3,1,2) 60 — 0 wrong
coefficients; negative control (transposed lattice A^T for a=(3,2), b=(1,1) hits the box at (-3,1)) rejected.
C lattice lemma exhaustive over 2406 tuples (k<=3, a<=4; k=4, a<=3): no nonzero lattice point in any box; det A = N.
B full lower-bound pipeline mod p (p = 1 mod L, ~1e9): exact decomposition, random chart gamma, full-box moments, random
admissible t, test functions in paper order; Kronecker block, zero cross blocks, zero V-blocks below the anti-diagonal and
H_i on it, rank G = rank E = N; cases 8, 20, 10, 54, 48, 48 pass; negative controls (corrupted weight; duplicated test
vector) detected. Observation: at gamma=0, t=0 the Gram matrix is singular (cubic triple: rank G = 11, rank E = 15 of 20)
— the generic choice of t is genuinely needed; the proof never claims invertibility for every t.
B' zero coordinates, repeated nodes, r > N: decompositions of prod(X^a Y^b + c X^d) via subset sums of character
decompositions and pure powers, one weight split 3w-2w; for b=1 mapped via y -> y - cx to decompositions of F with
b_il = 0 and run through the Part 1 reduction; cases with 16 (8 zero coords), 55 (45), 19, 113 (72; the 54 case), 23
nodes — all pass, rank = N.
Laurent: exact (sympy) identities (B.1) and (4) for all 1<=b<=d<=10, sign-flip control rejected; numerical screening
(mpmath 60 digits) T^{d-b+1} H_i(T) -> claimed leading matrix with relative error O(1/T) (3e-4, 3e-8, 3e-12 at
T = 1e4, 1e8, 1e12) in the 20, 54, (3,4) cases; |det C| = 3^{-12}, 10^{-27} match closed forms (screening only).

## 6. Checker commands and final lines
Accepted W-product package: python3 -S -s -B verification/run.py (exit 0, empty stderr, Python 3.12.10) — PASS check_charts.py,
exact_cyclotomic.py, check_exact.py (3 modes); 8 upper examples; 3 cubatures; 24 inline negative-control executions;
3 proof bindings; RESULT: PASS TR-29 binary-monomial product verification; PASS 15 inline negative-control executions;
2 proof bindings; RESULT: PASS TR-29 verification.
Binary-monomial package: python3 -S -s -B verification/run.py (exit 0) — PASS check_exact.py (3 modes); 8 upper
examples; 3 cubatures; 24 inline negative-control executions; 3 proof bindings; RESULT: PASS.
paper/SHA256SUMS checks OK; source tree clean after all runs.

## 7. Scope
Lean read for scope only (not built): algebraic core + conditional Gram assembly, consistent with the papers.
Literature beyond the CCS abstract not checked. Nothing inside the manuscript directory was run.
