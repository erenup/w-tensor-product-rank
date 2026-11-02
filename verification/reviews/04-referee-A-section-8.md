# Section 8 referee report A

**Verdict for Section 8: ACCEPT WITH CORRECTIONS.** No mathematical gap or error was found. The section faithfully reproduces the accepted monomial-products proof (`STATEMENT.md`/`PROOF.md` and the earlier `lower_bound.tex`, `upper_bound.tex`). The corrections below concern wording and conventions only.

Files reviewed (sha256): `sections/07_binary_monomials.tex` b4142314e3a0caf5da0214003c84a426158f5c4d3aaaa2ce3aa921632bf3e605; `sections/00_introduction.tex` 2e9efdd1a4ba2cc4e22babcf075ae638808ac2b57e1044fdc9df2ca61a718c06; `refs.bib` 562ccad55df80f61a02637551528cad0cd8b1e22ea05ee5a8d69fb3a13355519. The out-of-tree build is clean: 16 pages, no undefined or duplicate references, and every \ref/\eqref/\Cref target in Section 8 points to the intended object.

| Result / step | Location | Status | Note |
|---|---|---|---|
| Thm 8.1 statement, scope | ll.17-37 | minor | Correct. "Arbitrary positive exponents" (l.4) is broader than a_i≥b_i (corr. 2). |
| Lemma 4.1 reused with general m_i | ll.74-82 | OK | Its proof uses only linearity. |
| Pairing; Lemmas 5.1/6.1 apply to any list | ll.84-97 | OK | Neither lemma needs W invertible. |
| Lists U, V_i, counts δ_i q_i, N | ll.99-118 | OK | They reduce to B_0, B_i when b=1. |
| q_i meaning | (38), ll.116/186/291/299 | OK | q_i = ∏_{j≠i}(b_j+1), the accepted source's r_i; consistent with Section 7's q. |
| Lemma 8.1: G_i anti-triangular, det | (44)-(45) | OK | Reversal sign (-1)^{b(b+1)/2}, degrees ≤ 2b+δ = d. |
| Lemma 8.2: orthogonality | ll.155-182 | OK | Degree range (b_i, d_i] checked; the exponent d_i-s-b_i ≥ 0. |
| Lemma 8.3: anti-triangular blocks | ll.195-223 | OK | s+s' = d_i+1+α-α'. |
| Lemma 8.4: division identity, z=0 | (48) | OK | Telescoping checked; b≥1 makes every term vanish at z=0; for b=1 it becomes (63). |
| Lemma 8.5: Laurent leading term | (49)-(50) | OK | Leading term (-1)^{d-b}β t^{-(d-b+1)}; the det coefficient is at t^{-(d-b+1)q_i}. |
| k=1 conventions | §8.1 | minor | The empty Kronecker product and the singleton I_1 are not stated (corr. 1). |
| Finite parameter choice; proof of Thm 8.2 | (51), ll.298-323 | OK | D_i·det H_i is a polynomial; one admissible finite t. |
| Prop 8.1: γ choice, z, w, operator, m_i(e), β_i | (52)-(54) | OK | β_i = a!b!/d! = 1/binom(d,b), d≥2b, δ = a-b. |
| Lemma 8.6: det Δ = N, index, box avoidance | ll.421-466 | OK | Column convention; all three σ cases checked, including δ_i = 0. |
| Lemma 8.7; Prop 8.2: N-term identity | (57)-(59) | OK | e - a lies in ∏[-a_i, b_i]; terms nonproportional. |
| Remark 8.1; k=1/k=2 formulas; Example 8.1; a=b; Remark 8.2 | ll.546-627 | OK | Algebra checked; the b=0 counterexample is right. |
| Citations: Gałązka, BBGV, Behr; bib metadata | ll.572-599; `refs.bib` | OK / minor | Gałązka Thm 1.5(i) matches with (k0,k1,l0,l1) = (a1,b1,a2,b2), and Section 7.1 has the binomial ideal on the torus. BBGV Prop 4.3 is stated with a ≤ b (corr. 3). Behr has Thm 1.1 and Cor 5.4, and his Section 6 leaves k≥3 open. Crossref confirms both DOIs, volumes, pages and the five-author published version. |
| Closing sentence of the introduction | `00_introduction.tex` | OK | Accurate. |

**Corrections**
1. §8.1, after l.118 (or in the paragraph at ll.74-82), add: "Empty products, including empty Kronecker products of matrices, equal $1$; when $k=1$, $`\mathcal I_1`$ consists of the empty tuple." Without it, k=1 in Thm 8.2 leaves H_1, A_{ι,ȷ} and ⊗_{j≠i}G_j undefined.
2. l.4: replace "binary monomials with arbitrary positive exponents" with "binary monomials $`x_i^{a_i}y_i^{b_i}`$ with $`a_i\ge b_i\ge1`$".
3. ll.587-588: after the citation of Proposition 4.3 of the BBGV arXiv version, add "(stated there with the roles of $`x_i`$ and $`y_i`$ exchanged)".
4. Optional, l.243: "leaving exactly the numerator on the left" → "leaving $t^{d+1-b}z^{d+1}$".
5. Optional, outside Section 8, in the declaration on the use of generative AI: the sentence on what Lean covers reads as if it covered Section 8; Section 8 is paper-only. Suggested: "The lower-bound argument for Theorem 1.1 …". The abstract does not mention Thm 8.1; an editorial decision.

**Independent tests** (output identical under `-O`)
- Accepted checker: `verification/run.py` → PASS.
- Upper bound (stdlib, exact in Z[x]/Φ_N): characters enumerated as c with Δᵀc ≡ 0 mod N; every coefficient of identity (58) verified in seven cases: (2,2,2|1,1,1) N=20, (3,3,3|2,2,2) N=54, (5,2|2,1) N=15, (4,2,3|1,2,1) N=42, (3|2) N=4, (2,3|2,3) N=12, and a k=4 case with N=72. In every case det Δ = index = number of characters = N. Box avoidance holds in 688 exhaustive small cases with k=2,3. For k=2, Gałązka's bound = Behr's formula = N for all a,b ≤ 8, and BBGV's bound is ≤ N; b=1 gives M for k ≤ 4 and d_i ≤ 7. Negative controls rejected: the row lattice Δᵀ meets the box for (5,2|2,1); 19 of the 20 terms do not give F; for b=0 the formula exceeds rank 1.
- Lower bound mod p (p ≈ 2^61, p ≡ 1 mod N): points and weights from the character decompositions with random γ, plus a split (repeated) point and a cancelling pair at a zero coordinate. In all four cases (20, 54, 15, 42): the moments match (54) on the whole box with β = 1/binom; the N×N Gram matrix has zero cross blocks, its U-block equals ⊗G_i, and det G_i matches (45); the V_i blocks are anti-triangular with H_i and det = ±det(H_i)^δ; rank G = rank E = N.
- Lower bound, exact over Q: product-grid cubatures with random lower moments and zero nodes, b=(2,1), d=(6,3) (N=13, r=28) and b=(1,2,1), d=(3,5,2) (N=22, r=72, includes δ_3 = 0). All checks pass; the exact Gram determinant is nonzero.
- Negative controls: b=0 with x^3 gives H ≡ 0 and Gram rank 1 < 4; violating m_1(b_1+1)=0 makes the cross blocks nonzero; adding an s=b_i function makes the Gram matrix singular.
- sympy: (48) holds for b ≤ 4 and d ∈ [2b, 2b+4], with remainder of order t^{-(d-b+2)}; (54) and the action of the operator on (ux+vy)^d hold for a ≤ 5; the exact limit of t_i^{d-b+1}H_i equals (-1)^{d-b}β⊗G_j for i=1,2 on the zero-node cubature, and det H_i ~ det C_i t^{-(d-b+1)q_i} with det C_i = -9/25 and 27/125.
