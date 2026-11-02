# Exact rank of every product of binary monomials

Let k>=1 and let a_i>=b_i>=1 be integers for i=1,...,k. Set
d_i=a_i+b_i, q_i=b_i+1, and delta_i=a_i-b_i. In the complex vector space
tensor_product_i Sym^(d_i)(C^2), let

    F = product_i x_i^a_i y_i^b_i.

The fixed-block partially symmetric rank R(F) is the least number n of
summands in an identity

    F = sum_(l=1)^n c_l product_i (u_(i,l)x_i+v_(i,l)y_i)^d_i,

with arbitrary complex coefficients and factor vectors. The blocks and
their degrees are fixed. No reality, support, or genericity condition is
imposed on the decomposition.

**Theorem.**

    R(F) = N(a,b)
         = product_i (b_i+1)
           + sum_i (a_i-b_i) product_(j!=i) (b_j+1).

Empty products equal 1. The target subfamily is
k>=3, max_i b_i>=2.
The statement also includes the known one- and two-block cases and the
all-b_i=1 family of the [W-product theorem](../../../proofs/STATEMENT.md); those overlaps
are not claimed as independent new results. Pure-power factors b_i=0
are excluded. No assertion is made about grouped-mode, unrestricted
nonsymmetric, real, cactus, or border rank.

In particular, R((x^3 y^2) tensor (x^3 y^2) tensor (x^3 y^2))=54.

**Abstract lower-bound theorem.** Let n be a positive integer, with
nodes z_l in C^k and nonzero complex weights w_l. Let integers b_i>=1
and d_i>=2b_i be given. Suppose linear functionals m_i on C[z_i] up
to degree d_i satisfy m_i(z_i^e)=0 for b_i<e<=d_i and
m_i(z_i^b_i)!=0, and suppose

    sum_l w_l product_i z_(i,l)^e_i
      = product_i m_i(z_i^e_i)     (0<=e_i<=d_i).

Then n>=product_i(b_i+1)+sum_i(d_i-2b_i)product_(j!=i)(b_j+1).
Nodes may repeat and any of their coordinates may be zero.
