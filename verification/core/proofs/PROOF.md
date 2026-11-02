# Generic charts make the orthogonal moment blocks nondegenerate

All scalars are complex; every pairing below is symmetric bilinear, not
Hermitian. There is no positivity assumption and no limiting decomposition.

## 1. Abstract setup and the finite choice of parameters

Use the nodes, weights, degrees, and product functional of STATEMENT.md.
For a parameter vector t=(t_1,...,t_k), put

    h_(i,l)=1+t_i*z_(i,l),
    w_l(t)=w_l * product_i h_(i,l)^d_i.

We shall choose t with all h_(i,l) nonzero and with finitely many rational
determinants nonzero. It suffices to prove that each determinant is a
nonzero element of C(t_1,...,t_k). The product of their nonzero numerators
and the finitely many nonconstant h factors is a nonzero polynomial; its
nonvanishing locus in C^k is nonempty. This is the only use of genericity.
It changes an auxiliary pairing and basis, not the decomposition or nodes.

On B=C^n define

    <u,v>_t = sum_l w_l(t)*u_l*v_l.

This is nondegenerate when all h's are nonzero, because every w_l is nonzero.

Define 2^k vectors indexed by epsilon in {0,1}^k:

    u_epsilon(l)=product_i z_(i,l)^epsilon_i / h_(i,l).

For each i with d_i>=3, define (d_i-2)*2^(k-1) additional vectors indexed
by s=2,...,d_i-1 and epsilon in {0,1}^{[k]\{i}}:

    v_(i,s,epsilon)(l)
      = z_(i,l)^s / h_(i,l)^s
        * product_(j!=i) z_(j,l)^epsilon_j / h_(j,l).

Let U_t and V_(i,t) be their spans. For d_i=2 the latter space is omitted.
The goal is to show the whole list is linearly independent at a suitable
t. Its length is exactly the asserted lower bound.

## 2. U has a nondegenerate Gram matrix for every allowed chart

The Gram entry for u_epsilon,u_eta is the product functional applied to

    product_i z_i^(epsilon_i+eta_i)*(1+t_i*z_i)^(d_i-2).

Each coordinate degree is at most d_i, so the prescribed moments apply.
Let

    G_i(t_i) = [[gamma_i+(d_i-2)*t_i*beta_i, beta_i],
                [beta_i,                         0]].

The Gram matrix of the u's is the tensor product of these G_i. Each
determinant is -beta_i^2 != 0. Consequently the u's are independent,
dim U_t=2^k, and U_t is nondegenerate.

## 3. Distinct blocks are orthogonal

For a v_(i,s,epsilon) paired with any u_eta, the coordinate-i factor
after multiplying by the weight is

    z_i^(s+eta_i)*(1+t_i*z_i)^(d_i-s-1).

The exponent d_i-s-1 is nonnegative since s<=d_i-1. Every monomial has
coordinate-i degree between 2 and d_i, so its moment vanishes. All other
coordinate degrees are at most their d_j. Thus V_(i,t) is orthogonal
to U_t.

Likewise for i!=j, the coordinate-i factor of a product of a vector in
V_(i,t) with one in V_(j,t) is

    z_i^(s+eta_i)*(1+t_i*z_i)^(d_i-s-1),

and the analogous coordinate-j factor has the same property. The other
coordinates have the U-Gram form. All factors are polynomials within the
moment box, and the coordinate-i moment is zero. Thus different V blocks
are pairwise orthogonal. No assertion of dimension additivity has yet
been made.

## 4. The Gram matrix within a V block is anti-triangular in s

Group the V_(i,t) basis by increasing s=2,...,d_i-1. Its (s,s') block has
rows/columns indexed by epsilon,eta in {0,1}^{[k]\{i}} and entries

    sum_l w_l * z_(i,l)^(s+s') * h_(i,l)^(d_i-s-s')
          * product_(j!=i) z_(j,l)^(epsilon_j+eta_j)
                           * h_(j,l)^(d_j-2).             (1)

When s+s'<=d_i this is a polynomial inside the moment box with
coordinate-i degree at least four, and is zero. When s+s'=d_i+1 the
block is the same matrix H_i(t) for every such pair:

    H_i(t)[epsilon,eta]
       = sum_l w_l * z_(i,l)^(d_i+1)/(1+t_i*z_(i,l))
           * product_(j!=i) z_(j,l)^(epsilon_j+eta_j)
                            * (1+t_j*z_(j,l))^(d_j-2).   (2)

Reverse the order of the s'-block columns. The resulting block matrix
is lower triangular, with H_i on every diagonal block: on the diagonal
s+s'=d_i+1, and above it s+s'<=d_i. There are d_i-2 diagonal blocks.
Therefore the original determinant, up to a sign, is

    det(H_i(t))^(d_i-2).                                 (3)

It remains to prove det(H_i) is not the zero rational function. This
step is necessary: a special chart can give a singular Gram matrix,
as happens in the symmetric sign-diagonal cubic regression.

## 5. Exact Laurent leading coefficient of H_i

Treat t_i as a variable at infinity with the other parameters fixed
(equivalently work in C(t_j:j!=i)((t_i^{-1}))). For every fixed z!=0,

    z^(d_i+1)/(1+t_i*z)
      = z^d_i/t_i - z^(d_i-1)/t_i^2 + ...
          + (-1)^(d_i-1)*z/t_i^d_i + O(t_i^(-d_i-1)).   (4)

For z=0 the left side and all displayed coefficients are exactly zero,
so the same expansion through the displayed order holds. Thus no node
with a zero coordinate has been excluded or divided by.

Insert (4) into the finite sum (2). For the powers z_i^d_i down to
z_i^2 the coefficient vanishes by the stipulated product moments.
For the z_i coefficient it equals beta_i times the tensor product of
the other G_j matrices, since all the other polynomial degrees are
at most d_j. Hence the matrix Laurent expansion is

    H_i(t) = (-1)^(d_i-1) * beta_i * t_i^(-d_i)
                    * tensor_product_(j!=i) G_j(t_j)
               + O(t_i^(-d_i-1)).                       (5)

The leading coefficient matrix is invertible. In particular if
q=2^(k-1), the coefficient of t_i^(-d_i*q) in det H_i is the
nonzero determinant of that matrix. Therefore det H_i is a nonzero
rational function. This argument is valid for every i independently;
we do not require the different parameters to approach infinity in
one common limit.

For clarity, the identity underlying (4), valid even at z=0, is

    z^(d+1)/(1+t*z)
      = sum_(r=0)^(d-1) (-1)^r*z^(d-r)/t^(r+1)
          + (-1)^d*z/[t^d*(1+t*z)].                     (6)

Its last term is O(t^(-d-1)) at each fixed nonzero z and is identically
zero at z=0. Thus the Laurent calculation follows from an exact finite
identity, with no numerical approximation assumption.

## 6. Independence and the lower bound

Choose one finite complex parameter vector outside all pole and determinant
zero sets, as justified in section 1. Section 2 makes U_t nondegenerate.
Equations (3)-(5) make the Gram matrices of all V_(i,t) nondegenerate.
Section 3 makes these blocks pairwise orthogonal and orthogonal to U_t.

The Gram matrix of the full concatenated list is therefore block diagonal
with invertible diagonal blocks. Its columns must be linearly independent
in C^n. Consequently

    n >= 2^k + sum_i (d_i-2)*2^(k-1)
      = 2^(k-1)*(sum_i d_i - 2*k + 2).

Repeated nodes cause no issue. If they gave a linear dependence in the
evaluation list, it would contradict the just-proved Gram invertibility.
Zero weights may be deleted in advance. This proves the abstract theorem.

## 7. Reduction from every partially symmetric tensor decomposition

Let F=product_i x_i^(d_i-1)y_i. Start with an arbitrary length-n complex
decomposition

    F = sum_l alpha_l * product_i (a_(i,l)*x_i+b_(i,l)*y_i)^d_i,

deleting any zero summands. Thus every alpha_l and every factor vector is
nonzero. For each i choose gamma_i such that
a_(i,l)+gamma_i*b_(i,l) != 0 for every l; only finitely many values are
excluded. Define

    z_(i,l)=b_(i,l)/(a_(i,l)+gamma_i*b_(i,l)),
    w_l=alpha_l * product_i(a_(i,l)+gamma_i*b_(i,l))^d_i.

Apply the differential operator

    product_i (partial_x_i+gamma_i*partial_y_i)^(d_i-e_i)
                    * partial_y_i^e_i

and divide by product_i d_i!. The decomposition gives the moment sum
in STATEMENT.md. Differentiation of the target gives

    m_i(0)=gamma_i, m_i(1)=1/d_i, m_i(e)=0 for 2<=e<=d_i.

Every beta_i=1/d_i is nonzero. The abstract theorem applies and proves
the lower bound for every complex decomposition, including original
points at infinity and factors with b_(i,l)=0. There is no assumption
of generic support: both chart choices are auxiliary to an arbitrary
fixed decomposition, with existence proved after that choice.

## 8. Matching upper bound and exact scope

For k>=2 and all d_i>=3, Canino--Casarotti--Santarsiero, arXiv:2512.05828,
Theorem 1.1, proves the partially symmetric upper bound
2^(k-1)*(sum d_i-2k+2). Combining it with section 7 gives the
exact rank in STATEMENT.md. The nonzero scalar in the catalogue's tensor
normalization of W_d has no effect on rank over C.

This lower proof uses finite decompositions and auxiliary diagonal
bilinear forms. It gives no analogous lower bound for border rank;
indeed the border rank can be only 2^k. It gives no conclusion about
rank after grouping modes from different blocks. No restriction to the
published upper construction is used in the lower proof.
