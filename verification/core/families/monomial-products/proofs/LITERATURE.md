# Bounded prior-work check and exact scope

No claim is made that a published conjecture
already specifies the all-k formula. A bounded source check was
performed; no exhaustive novelty or priority assertion is made.

1. Maciej Galazka, *Multigraded apolarity*, arXiv:1601.06211v3,
   Theorem 1.5(i) and section 7.1, gives the two-factor upper bound
   (a_1+1)(b_2+1)+(b_1+1)(a_2+1)-(b_1+1)(b_2+1).
   Its proof constructs reduced torus points by binomial equations.
   The same theorem includes two-factor lower bounds and exact special
   cases. The paper does not claim our all-k formula in these passages.
   Primary source: https://arxiv.org/abs/1601.06211 .

2. The catalogue's Behr submission, *The partially symmetric rank
   of a product of two W-states and of bihomogeneous binary monomials*,
   Corollary 5.4 (label cor:monomial), states the exact two-factor value
   (a_1+1)(a_2+1)-(a_1-b_1)(a_2-b_2). Its section on three or more
   factors says the three-block W question remains open in that work.
   This is an unpublished manuscript. Its exact result is an overlap of our formula,
   not a new claim here. Its reference to Galazka's thesis
   Remark 1.8 motivates the broader monomial-product question; we have
   not directly verified that separate thesis remark.

3. Edoardo Ballico, Alessandra Bernardi, Fulvio Gesmundo and Emanuele
   Ventura, *Geometric conditions for strict submultiplicativity of
   rank and border rank*, arXiv:1909.03811v2, Proposition 4.3, gives a
   two-binary-monomial lower bound and describes it as far from sharp.
   Primary source:
   https://arxiv.org/abs/1909.03811 .

4. Ballico--Bernardi--Christandl--Gesmundo, *On the partially symmetric
   rank of tensor products of W-states and other symmetric tensors*,
   arXiv:1803.01623, discusses binary monomials/Dicke states and provides
   bounds for products of W-states. Theorem 3.3 gives the cubic-W
   tensor-power upper bound; Remark 3.4 explains its scope.
   https://arxiv.org/abs/1803.01623 .

5. Canino--Casarotti--Santarsiero, *A new bound on the rank of tensor
   product of W-states*, arXiv:2512.05828, Theorem 1.1, for k>=2 and all d_i>=3, gives
   2^(k-1)(sum d_i-2k+2) as an all-W upper bound. This is the upper
   theorem cited in the [W-product proof](../../../proofs/PROOF.md).
   https://arxiv.org/abs/2512.05828 .

The new target is every k>=3 positive binary-monomial product with at
least one smaller exponent b_i>=2. It is distinct from the all-W TR29
family, and from the asymptotic subrank of one Dicke tensor with
all its tensor modes kept separate. Here each
binary monomial remains a fixed symmetric block and the object is its
finite complex partially symmetric rank.

No result in this package depends on accepting a cited theorem as a
black box: the lower bound, lattice construction and character identity
are proved in full. The references are context for the target and its overlap, not
part of a purported computer proof.
