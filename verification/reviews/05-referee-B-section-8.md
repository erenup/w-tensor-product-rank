# Section 8 referee report B

**Verdict for Section 8: ACCEPT WITH CORRECTIONS.** No mathematical gap or error was found. All corrections below concern wording, precision or credit.

Before reading Section 8 in detail the referee sketched an independent route: (a) moments truncated above b_i with β_i≠0; (b) test functions Z^ι/h^{b}, with each Gram factor anti-triangular; (c) a Z^{d+1}/(1+tZ) block whose leading Laurent term is set by β_i; (d) one finite choice of t; (e) a lattice avoiding the box ∏[-a_i,b_i], plus character orthogonality. Section 8 follows exactly this route; the earlier accepted plain-text proof, read afterwards, agrees.

| # | Step (location) | Status | Note |
|---|---|---|---|
| 1 | Thm 8.1 statement and scope | OK | Opening sentence needs a fix (corr. 1) |
| 2 | (8.2) δ_i, q_i, N; N=M when b=1 | OK | |
| 3 | Thm 8.2 hypotheses | OK | b_i≥1, d_i≥2b_i only in the preamble (corr. 2) |
| 4 | Reuse of Lemmas 4.1, 5.1, 6.1; the pairing | OK | Needs only linearity; admissible t makes every evaluation defined, and the polynomial equals the rational function at the nodes |
| 5 | Lists U and V_i, their counts | OK | s-range nonempty iff δ_i>0; V_i has δ_i·q_i members |
| 6 | Lemma 8.1: G_i, det = (-1)^{b(b+1)/2}β^{b+1}, Kronecker form | OK | Degree 2b+δ=d; entries vanish for e+e'>b |
| 7 | Lemma 8.2: orthogonality | OK | h exponent d_i-s-b_i≥0; degrees in [b_i+1, d_i] |
| 8 | Lemma 8.3: anti-triangular blocks | OK | s+s' runs over [2b_i+2, 2d_i-2b_i]; the full antidiagonal s+s'=d_i+1 exists |
| 9 | Lemma 8.4: division identity | OK | At z=0 every term vanishes because b≥1 |
| 10 | Lemma 8.5: Laurent expansion | OK | Power t^{-(d-b+1)}, sign (-1)^{d-b}, coefficients in C(t_j: j≠i); det leading term t^{-(d-b+1)q_i}·det C_i with det C_i a nonzero constant. For k=1 see corr. 3 |
| 11 | Proof of Thm 8.2: avoidance polynomial | OK | D_i·det H_i is a polynomial; one finite t suffices |
| 12 | Prop 8.1: γ choice, (8.zw), operator, m_i(e), β_i = binom(d_i,b_i)^{-1} | OK | Moments hold on the whole box |
| 13 | Lemma 8.6: det Δ=N, index, box avoidance | OK | Cases σ>0, σ<0, σ=0 all correct, including δ_i=0 |
| 14–15 | Lemma 8.7 and Prop 8.2 | OK | Coefficients exact; N nonzero summands; distinct tuples |
| 16 | Remark 8.1 | OK | Range k≥1, d_i≥2 is right: k=1 gives d, all d_i=2 gives 2^k |
| 17 | Two-block algebra and citations | OK | Checked against the sources |
| 18 | Example 8.1 | OK | det(2I+J)=20, det(3I+J)=54 |
| 19 | Remark 8.2 (b_i=0) | OK | The failure occurs exactly at the z=0 remainder (negative test) |

**Corrections**
1. Line 4, "arbitrary positive exponents": Thm 8.1 assumes a_i≥b_i. Add: "Interchanging x_i and y_i preserves the form; for arbitrary positive exponents the rank is N with (a_i,b_i) replaced by (max, min)."
2. Thm 8.2: make it self-contained: "Let k≥1, let b_i≥1 and d_i≥2b_i be integers, and let N be as in (8.2)". Remark 8.2 shows b_i≥1 is essential.
3. Lemmas 8.1 and 8.5 when k=1: state that an empty Kronecker product is the 1×1 matrix (1) and that the index set is then a single point.
4. Prop 8.2: the exponent vector e clashes with the basis vectors and with the scalar e used earlier; rename it (e.g. to \mathbf c).
5. "the classical rank of a binary monomial": add a citation.
6. Credit (recommended): for k=2 the support of Prop 8.2 is exactly the point set of Gałązka's construction; say so after "two-dimensional torus".
7. Optional: in Lemma 8.4 the hypothesis d≥2b is unnecessary; d≥b suffices.
8. Optional, paper-wide: separate counters put Lemma 8.1, Proposition 8.1, Remark 8.1 and Example 8.1 side by side; N_i in Section 7 clashes with N.

**Independent tests**
- Upper bound, exact arithmetic in Q(ζ_N) (integer reduction modulo Φ_N): every coefficient of the character identity in Prop 8.2, plus det Δ=N, brute-force box avoidance and |Γ̂|=N, in 1821 cases: k=1–3 with b_i∈{1,2,3}, a_i-b_i∈{0,…,3}; k=4 cases including unequal blocks (3,2,4,1;1,2,1,1), (3,3,3,3;2,2,2,2), (5,1,2,3;2,1,2,1), and the 20 and 54 examples. All pass. Negative control: a diagonal lattice hits the box.
- Lower-bound pipeline, mod 2^61-1 (and primes p≡1 mod N for the character decompositions); 84 runs, all positive checks pass:
  - random decompositions of F_{a,b} with r up to 151 > N, containing zero coordinates, exact and proportional repeated nodes, and shared coordinates;
  - the tight N-term character decompositions (r = N = rank E) for 20, 54 and 48 (k=4), also augmented by a null combination adding a zero coordinate and a repeated node;
  - Thm 8.2 with random lower moments, an all-zero point and repeated points.
  Checks per run: moments on the full box; U-block = ⊗G_i; the det G_i formula; every cross block is 0; the (s,s') blocks are 0 or H_i as stated; Laurent coefficients of t_i^{-1},…,t_i^{-(d-b)} vanish and the t_i^{-(d-b+1)} coefficient equals (-1)^{d-b}β_i⊗G_j (computed independently from the series of 1/(1+tz)); det H_i≠0 and rank Gram = rank E = N.
- Negative controls, all failing as required: x^4 with b=0 (Laurent coefficients do not match, det H=0); x1^3·x2^2y2 with its 3-term decomposition (b=(0,1)): Laurent check fails, rank 3 < 9; adding s=d-b+1 functions to a tight decomposition: cross blocks nonzero, rank 20 < 32; a perturbed weight: identity and moments fail.
- sympy: Lemma 8.4 for b≤4, d∈[2b,2b+4], including the remainder order; formula (8.mi) for a≤5 and the operator applied to (ux+vy)^d; det G_i with symbolic moments for b≤4, δ≤3.
- Build: latexmk clean, no undefined references or citations.
- Citations checked against the sources: Gałązka arXiv v3 Thm 1.5(i),(ii) and §7.1; BBGOV v2 Prop 4.3 (assumes a≤b; the max-expression is symmetric, so the statement is correct); Behr Cor 5.4 and Thm 1.1, with §6 leaving k≥3 open; CCS Thm 1.1 assumes k≥2, d_i≥3.
