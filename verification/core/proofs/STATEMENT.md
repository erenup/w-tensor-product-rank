# Exact rank of arbitrary products of generalized W tensors

For every integer k>=2 and all integers d_1,...,d_k>=3, over C, the rank
with respect to the fixed partially symmetric blocks is

    R_(d_1,...,d_k)(product_i x_i^(d_i-1) y_i)
       = 2^(k-1) * (sum_i d_i - 2*k + 2).

The decomposition permits arbitrary complex vectors in each of the k
blocks, arbitrary complex coefficients, repeated nodes, and coordinates
equal to zero. No support-curve, affine-support, real, or symmetry-between-
blocks restriction is imposed. This is exact rank, not border rank or the
rank of a regrouping of modes. The upper bound is the published theorem of
Canino--Casarotti--Santarsiero, arXiv:2512.05828, Theorem 1.1. The
new assertion is the matching universal lower bound.

In particular the cubic triple has exact rank 20, and all k-fold
cubic products have rank 2^(k-1)(k+2).

The abstract lower theorem, valid also for k=1 and d_i>=2, is as follows.
Let beta_i be nonzero complex numbers and gamma_i arbitrary complex numbers.
Suppose n nodes z_l in C^k with nonzero complex weights w_l satisfy

    sum_l w_l product_i z_(i,l)^e_i = product_i m_i(e_i)
    for all 0<=e_i<=d_i,

where m_i(0)=gamma_i, m_i(1)=beta_i, and m_i(e)=0 for 2<=e<=d_i.
Then

    n >= 2^k + 2^(k-1)*sum_i(d_i-2).

Repeated nodes and zero coordinates are explicitly allowed. The abstract
statement is a lower bound only; no existence claim for a minimal cubature
formula is needed for the tensor-rank conclusion.
