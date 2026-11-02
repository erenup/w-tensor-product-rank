# Referee report A: Sections 1–7 (W-product lower bound) and the binary-monomial generalization

## 1. Verdicts
- Part 1 (W-product lower bound, manuscript + sketch): ACCEPT WITH CORRECTIONS (all minor/expository; no gap or error).
  The lower-bound argument does not use k>=2 or d_i>=3 (valid for k>=1, d_i>=2); those hypotheses matter only for the cited upper bound.
- Part 2 (binary-monomial generalization, lower and upper bound): ACCEPT WITH CORRECTIONS (minor notation/wording; no gap or error).
  Lattice construction and character decomposition correct; b_i=1, a_i=d_i-1 gives exactly M.

## 2. Theorems verified
Part 1 (00_introduction.tex:36-42): k>=2, d_i>=3, over C, blocks fixed: R_d(prod x_i^{d_i-1} y_i) = M = 2^{k-1}(sum d_i - 2k + 2).
Lower bound proved: any finite decomposition (complex c, a, b; no support/distinct-node restrictions; zero coordinates
allowed; no positivity) has r >= M; abstractly: gamma_i in C, beta_i != 0, m_i(0)=gamma_i, m_i(1)=beta_i, m_i(e)=0 for
2<=e<=d_i, nodes/weights satisfying product moments on the full box => #nodes >= M. Upper bound cited (CCS Thm 1.1); Part 2's
prop:upper with b_i=1 gives an independent proof for all d_i>=2.
Part 2: abstract lower bound (lower_bound.tex:8-38; STATEMENT.md:84-94): b_i>=1, d_i>=2b_i, m_i vanishing on z^e for
b_i<e<=d_i, beta_i=m_i(z^{b_i})!=0, arbitrary lower moments, nonzero weights, full-box product moments =>
n >= N = prod q_i + sum (d_i-2b_i) prod_{j!=i} q_j, q_i=b_i+1. Rank formula for k>=1, a_i>=b_i>=1:
R(prod x_i^{a_i} y_i^{b_i}) = prod(b_i+1) + sum (a_i-b_i) prod_{j!=i}(b_j+1); upper bound = N-term character identity (9).

## 3. Step tables
Part 1 (P = .../TR29/source/paper/): 1 statement 00:13-42 OK; 2 delete zero summands 01:3 minor (implicit; afterwards
c!=0, (a,b)!=(0,0)); 3 existence of gamma_i 01:23-25 OK (wording); 4 coordinate change/term count/w!=0 01:7-29 OK
(block det 1); 5 coefficients <=> full-box moments 02:3-28 OK (both directions); 6 linear extension, product rule
03:3-29 OK; 7 caveat on L on rational functions 03:35-37 OK; 8 "admissible t" 04:4-9 minor (undefined); 9 G=E^T W E
04:26-55 OK; 10 "remaining entries handled in Appendix B" 04:22-24 minor (only s+s'=d_i+1 entries needed); 11 G invertible
=> rank E = M => r>=M 05:7-19 OK (transpose bilinear form); 12 families B_0,B_i, count M 06:8-29 OK; 13 k=3,d=3 example
06:34-56 OK; 14 G_0=(x)G_i, det G_i=-beta_i^2 06:88-99 OK; 15 cross blocks vanish 06:101-107, A:3-33 OK; 16 example
G_1(x)G_2 06:111-125 OK; 17 H_i definition 06:128-140 OK; 18 anti-triangular, det G_i=±det H_i^{d_i-2} 06:142-164,
A:35-45 OK; 19 example d_i=5 06:166-186 OK; 20 finite division identity B:52-66 OK; 21 Laurent leading term
(-1)^{d-1} beta (x) G_j B:68-96, 06:192-212 OK; 22 det H_i nonzero rational function B:98-108 minor (state that
denominators involve only t_i); 23 one finite choice of t via Q(t) 06:214-232 minor (state numerator/denominator);
24 assembly 06:260-270 OK; 25 upper bound OK; 26 edge cases (repeated nodes, zeros, a=0, d_i=3, k=2) OK; 27 sketch OK.
Part 2: statements consistent OK; U list, det G_i=(-1)^{q(q-1)/2} beta^q OK; orthogonality OK; anti-triangular V_i,
det=±det H_i^{delta_i} OK; Laurent identity (b>=1 handles z=0) OK; leading coefficient, det H_i!=0 OK; finite chart OK/minor
(PROOF.md: name the denominator); reduction m_i(z^e)=(d-e)! b! gamma^{b-e}/((b-e)! d!), beta=1/binom(d,b) OK (re-derived,
mod-p checked); det A = N, lattice index N OK; lattice meets box only at 0 OK (brute force 1240 tuples); character
orthogonality OK; character decomposition (9) OK (all coefficients mod p on 14 cases); specializations (k=1, k=2,
b_i=1, a_i=b_i, 54) OK; exclusion of b_i=0 OK; literature/context NOT verified (web restricted).

## 4. Corrections
Part 1:
1. 01:3, 01:25: "delete its zero summands; this does not increase r; afterwards c_l != 0 and (a_il,b_il) != (0,0)";
   "a pair with b_il != 0 excludes only -a_il/b_il; a pair with b_il = 0 has a_il != 0 and excludes nothing".
2. 04:4-5: add "(we call such t admissible)" (used at 06:64, 05:24).
3. 04:22-24: "Only the entries with s+s' = d_i+1 in Lemma 7.2 fall outside P_d and are needed; they are treated in
   Appendix B. Entries with s+s' >= d_i+2 are never evaluated."
4. 06:193, B:106: add "entries of H_i have denominators only of the form 1+t_i z_il, so the other t_j may be specialized
   to arbitrary complex values; a nonzero specialization gives det H_i != 0 in C(t)".
5. 06:221-222: take D_i = prod_l (1+t_i z_il)^q and N_i := D_i det H_i in C[t], or note det H_i = N_i(t)/D_i(t) at an
   admissible t with D_i(t) != 0.
6. 06:30: "linear independence of the evaluation vectors ev(phi_a)"; optionally remark that the lower bound uses neither
   k>=2 nor d_i>=3.
7. (optional) letter a overloaded (a_il, Gram indices, Appendix B summation index B:56, 78) — rename the B index.
8. main.tex:82: restrict "Lean covers its algebraic core" to Gram assembly, anti-diagonal determinant, formal Laurent
   leading term and parameter avoidance; test functions, cross-block cancellations and the reduction to moments are text-only.
Part 2:
9. PROOF.md:3-5: "Its lower mechanism" -> "The lower mechanism of this proof".
10. PROOF.md:133-135: "all h factors and the polynomials P_i = D_i^{r_i} det H_i, where D_i = prod_l (1+t_i z_{i,l})".
11. Notation clashes: upper_bound.tex exponent tuple m vs functionals m_i (use e); group H, integer H=-S, blocks H_i
    (rename group Gamma, integer h); character group G vs G_i; lower_bound.tex:189 "s=b_i+1+a" vs a_i; lower_bound.tex:92
    index r vs r_i.
12. lower_bound.tex:86-88: add "(with coefficients in K)".
13. Context citations to check against sources: context.tex:349-351 attributes "Prop 4.3" (lower bound sum d_i-k+1) to
    BBCG while LITERATURE.md item 3 uses "Prop 4.3" for BBGV; Behr Thm 1.1 "for d_1,d_2>=2" (context.tex:386); BBCG Thm 3.6
    not mentioned in LITERATURE.md.
14. main.tex:43-44: "nondegenerate at one finite choice of parameters".

## 5. Lean correspondence (Statement.lean, Definitions.lean read, not built; no sorry/admit/axiom/native_decide/extern)
Lemmas 2.1, 3.1, 4.1 — paper-only. G=E^T W E — definitional (weightedGram). Dimension lemma — target 5
OrthogonalGramAssembly (block form). Count M and r>=M — target 6 TR29GramLowerBound, conditional on Gram hypotheses.
Lemma 7.1 cross-block cancellation, (x)G_i, det G_i — paper-only. Lemma 7.2 zero/H_i pattern — paper-only; its determinant
consequence — target 4 AntiDiagonalBlockTheorem (r=d_i-2, shift s->s-2). Laurent leading term — targets 2+3 (formal series,
b=1, d=d_i, M_l = w_l A(z_l)); moment hypotheses, identification of rational H_i with the series, transfer to "nonzero
rational function" — paper-only. Lemma B.1 — paper-only. Prop 7.4 — target 7 FiniteChartAvoidance (given nonzero N_i,
D_i; their nonvanishing paper-only). CCS upper bound — outside Lean. Target 1 UnivariateMomentBound — not used by Part 1
(k=1 case of Part 2's abstract bound).

## 6. Checker commands and outputs
Accepted W-product package, python3 -S -s -B verification/run.py:
  PASS check_charts.py / exact_cyclotomic.py / check_exact.py (normal, optimized, hash-seed); PASS 8 upper examples;
  3 cubatures; 24 inline negative-control executions; 3 proof bindings; RESULT: PASS TR-29 binary-monomial product
  verification; PASS 15 inline negative-control executions; 2 proof bindings; RESULT: PASS TR-29 verification (exit 0,
  Python 3.12.10; same from verification/ and under -O).
Binary-monomial package, python3 -S -s -B verification/run.py: PASS check_exact.py (3 modes); PASS 8 upper
  examples; 3 cubatures; 24 inline negative-control executions; 3 proof bindings; RESULT: PASS (exit 0).
Own tests: lattice_box.py -> "lattice/box check OK on 1240 exponent tuples"; gram_modp.py (two primes ~1e9, 3e9;
14 cases incl. N=20,32,51,54,56,64; repeated node, cancelling pair with zero coordinates and a point at infinity; random
gamma, t; full-box moments vs reduction formula, G_U=(x)G_i, det formulas, zero cross blocks, anti-triangular zeros,
H_i blocks, exact Laurent remainder entrywise, det H_i != 0, full Gram rank N) -> "ALL REFEREE MOD-p CHECKS PASSED".
