# TR-29: exact scope of the Lean core

The definitions and seven targets below are proved by `TR29.core_theorems`.
This algebraic core supports the [written proof](../proofs/PROOF.md).
Build and audit commands are in [README.md](README.md).

## What the aggregate certifies

`CoreTheorems` is the conjunction of seven propositions. All scalars in
their statements are the ordinary complex numbers except that targets 2
and 3 quantify over every field K of Lean type Type (including C and
rational-function coefficient fields over C). All dimensions and exponents
are universally quantified natural numbers. There is no
maximum degree, number of nodes, matrix size, or number of blocks.

1. `UnivariateMomentBound`: for b>=1,d>=b, arbitrary z_l,w_l in C, a
   nonzero moment sum_l w_l z_l^b and zero moments for b<e<=d imply
   n>=d-b+1. Weights need not be positive or nonzero; nodes may repeat
   or be zero. The target assumes no vanishing of lower moments.
   This is a full one-coordinate theorem, not a finite example.

2. `GeometricKernelIdentity`: over every such field K, the series with coefficient
   (-z^(-1))^e is an actual inverse of 1+C(z^(-1))X. Lean's inverse
   at z=0 is zero; the kernel at that node is consequently 1, and the
   identity remains valid. In the next target its contribution is
   multiplied by z^d, with d>=b>=1, so that node contributes zero.

3. `MatrixMomentLeadingTheorem`: over every such field K, for every matrix size q and finite
   collection of matrix weights M_l, suppose the actual matrix
   B=sum_l M_l z_l^b has nonzero determinant and all matrix moments
   for b<e<=d vanish. The actual formal-series matrix is

       H(X)[i,j] = X sum_l C(M_l[i,j] z_l^d)
                                  * geometricKernel(z_l).

   With D=d-b+1, all its entrywise coefficients below D vanish,
   its entrywise coefficient at D is (-1)^(d-b)B, and det H is
   nonzero in K[[X]]. The last assertion is a conclusion, not a
   hypothesis. Neither linear independence nor genericity is assumed.
   The formal inverse identity identifies this expression with the
   expansion at X=t^(-1) of the rational matrix in the written proof,
   node by node when z is nonzero; zero nodes contribute zero.

4. `AntiDiagonalBlockTheorem`: for arbitrary r,q, an actual square
   matrix indexed by Fin r times Fin q has zero (s,t) block when
   s+t+1<r and the same nonsingular matrix H when s+t+1=r. These
   hypotheses imply that the full determinant is nonzero. Blocks
   beyond the anti-diagonal are unrestricted; r=0 or q=0 is allowed.
   This is exactly the written first-anti-diagonal dimension mechanism
   after shifting s from 2,...,d_i-1 to 0,...,d_i-3.

5. `OrthogonalGramAssembly`: for arbitrary vectors v_(b,i) in C^n
   and weights w_l, the pairing is literally sum_l w_l u_l v_l,
   without complex conjugation. The hypotheses are zero cross-block
   pairings and nonzero determinants of each actual within-block
   Gram matrix. The conclusions are linear independence of the
   entire concatenated vector family and sum_b m_b<=n. This does
   not assume that independence or dimension additivity.

6. `TR29GramLowerBound`: specialize the preceding interface to one
   block of size 2^k and, for each i, a block of size
   (d_i-2)2^(k-1), with k>=1 and all d_i>=2. Under the same explicit
   Gram hypotheses, derive

       n >= 2^(k-1)(sum_i d_i - 2k + 2).

   The Lean subtraction is natural subtraction; d_i>=2 and k>=1
   must justify the arithmetic identity. The extra determinant and
   orthogonality hypotheses are intentional and are not hidden in
   an opaque admissibility predicate. The target is the conditional
   assembly core, NOT the full multivariate cubature theorem from
   just its moment hypotheses.

7. `FiniteChartAvoidance`: given arbitrary z_(i,l) and any finite
   list of nonzero multivariate polynomials p_j in k variables,
   there exists one finite complex tuple t at which every p_j is
   nonzero and all factors 1+t_i z_(i,l) are nonzero. The input
   polynomials may be unrelated and no simultaneous limiting path
   or separately chosen tuple for each polynomial is allowed.

The aggregate theorem proves the conjunction of all seven propositions.
These are genuine universally quantified algebraic results, not
propositions defined to return precomputed rank counts.

## Boundaries that remain in the written proof

This project does **not** certify the full k-coordinate cubature lower
theorem from only the prescribed product moments. In particular it does
not construct the specific U/V vectors from all multivariate moment
data, prove every resulting cross-block cancellation, or automatically
bind all those vectors to the Gram hypotheses of target 6.

The matrix-moment lemma does cover rational-function coefficient fields
in the other k-1 parameters. The written proof's identification of each
specific rational H_i with this formal series, its determinant numerator
polynomial, and the transfer from a nonzero series determinant to that
particular polynomial remain outside this contract. Target 7 starts with
explicitly nonzero input polynomials; it does not assert that any
particular unformalized numerator is nonzero.

The differential-operator affine-chart reduction from an arbitrary
partially symmetric tensor decomposition to product moments is outside
Lean, as is the cited published upper bound. No Lean theorem here
states the exact complex tensor rank formula or proves a multivariate
rank lower bound without the Gram hypotheses. No real, border,
regrouped-mode or unrestricted nonsymmetric rank assertion is included.
The finite-character upper construction for arbitrary binary-monomial
products is also outside this contract.

The cyclotomic and finite Gram checker examples in the verification suite
are supporting regressions and are not premises of the universal formal
targets. Their Python success is not presented as a Lean proof. The
kernel certification in this scope concerns the seven algebraic targets
above; it does not rely on the finite computations being exhaustive.

## Trust and resources

Lean is pinned to v4.34.0-rc2 and Mathlib to
85e3a25e006c35636f0e53b0e9296caca2685bc0. Proofs use only standard
axioms (propext, Classical.choice, Quot.sound), with no placeholder,
custom axiom, native_decide, compiler trust override or external oracle.
The audit performs a clean build, exact-type and transitive-axiom
checks for all seven targets and the aggregate, literal source/contract
bindings, and negative controls that actually fail. The build uses two Lean
workers and serial module compilation.
