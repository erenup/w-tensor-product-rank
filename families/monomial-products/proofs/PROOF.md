# Product-moment Gram blocks and a finite character decomposition

All scalars are complex. All Gram pairings are symmetric bilinear, not
Hermitian. Its lower
mechanism generalizes the [W-product proof](../../../proofs/PROOF.md); the upper
mechanism below is a separate elementary finite-group construction.

## 1. Abstract lower bound

Assume the moment hypotheses of STATEMENT.md. Write q_i=b_i+1,
delta_i=d_i-2b_i>=0 and Q=product_i q_i. For parameters t in C^k, put

    h_(i,l)=1+t_i z_(i,l),
    w_l(t)=w_l product_i h_(i,l)^d_i.

For now work over the rational function field C(t_1,...,t_k). Every h
is a nonzero polynomial. On C(t)^n use the diagonal bilinear pairing

    <f,g>_t = sum_l w_l(t) f(l)g(l).

We will exhibit a list of N=Q+sum_i delta_i Q/q_i vectors with an
invertible Gram matrix. The rational determinants will also justify a
single finite choice of all the parameters; no decomposition limit is
used.

The first list, U, consists of vectors indexed by 0<=epsilon_i<=b_i:

    u_epsilon(l)=product_i z_(i,l)^epsilon_i / h_(i,l)^b_i.

For each i with delta_i>0, the list V_i consists of vectors indexed by
b_i+1<=s<=d_i-b_i and 0<=epsilon_j<=b_j for j!=i:

    v_(i,s,epsilon)(l)=z_(i,l)^s / h_(i,l)^s
                        * product_(j!=i) z_(j,l)^epsilon_j / h_(j,l)^b_j.

Thus U has Q vectors and V_i has delta_i Q/q_i vectors.

### 1.1 The U Gram matrix

Define the q_i by q_i matrix (indices 0,...,b_i)

    G_i(t_i)[p,r] = m_i(z_i^(p+r)(1+t_i z_i)^(d_i-2b_i)).

The argument of m_i has degree at most d_i. If p+r>b_i the entry
is zero. If p+r=b_i the entry is beta_i=m_i(z_i^b_i)!=0. Reversing
column order makes G_i triangular with diagonal beta_i, so

    det G_i = (-1)^(q_i(q_i-1)/2) beta_i^q_i != 0.

This holds for every t_i, with arbitrary lower moments. The product
moment identity makes the U Gram matrix exactly tensor_product_i G_i.
Consequently this matrix is invertible and U is linearly independent.

### 1.2 Orthogonality between different lists

Pair v_(i,s,epsilon) with any u_eta. The factor in coordinate i after
including w_l(t) is

    z_i^(s+eta_i)(1+t_i z_i)^(d_i-s-b_i).

Its h exponent is nonnegative because s<=d_i-b_i. Every monomial
has degree at least s>b_i and at most d_i-b_i+eta_i<=d_i. Its m_i
value is therefore zero. Each other coordinate is a polynomial of
degree at most d_j. The product moment identity proves <V_i,U>=0.

For i!=j, pair a vector from V_i with one from V_j. The same
coordinate-i factor, now with eta_i coming from V_j, has zero moment;
the coordinate-j factor is also polynomial of degree at most d_j,
and every remaining coordinate has the U-Gram form. Thus <V_i,V_j>=0.
This calculation uses only moments inside the stated degree box.

### 1.3 The Gram matrix inside V_i

Order its blocks by increasing s. Its (s,s') block, with rows/columns
epsilon,eta, has entries

    sum_l w_l z_(i,l)^(s+s') h_(i,l)^(d_i-s-s')
               * product_(j!=i) z_(j,l)^(epsilon_j+eta_j)
                                  h_(j,l)^(d_j-2b_j).             (1)

If s+s'<=d_i, this expression is in the moment box and its
coordinate-i degrees are greater than b_i; the block is zero.
If s+s'=d_i+1, the block is the same matrix H_i(t), namely

    H_i[epsilon,eta]
      = sum_l w_l z_(i,l)^(d_i+1)/(1+t_i z_(i,l))
          * product_(j!=i) z_(j,l)^(epsilon_j+eta_j)
                             (1+t_j z_(j,l))^(d_j-2b_j).         (2)

There are delta_i blocks in each direction. Reverse the s'-block
columns. On every diagonal, s+s'=d_i+1; above it, s+s'<=d_i.
The reversed matrix is block lower triangular. Therefore, up to the
column-reversal sign, its determinant is

    det(H_i(t))^delta_i.                                        (3)

We prove H_i invertible as a rational matrix, rather than assume that
an arbitrary special choice of chart makes it so.

### 1.4 Laurent leading coefficient; zero coordinates included

For integers d>=2b, b>=1, the following finite rational identity holds
for t!=0 whenever 1+tz!=0, including z=0:

    z^(d+1)/(1+tz)
       = sum_(p=b)^d (-1)^(d-p) z^p t^(-(d+1-p))
         + (-1)^(d+1-b) z^b t^(-(d+1-b))/(1+tz).                 (4)

Multiplication by (1+tz)t^(d+1-b) verifies it by cancellation.
For each fixed nonzero z, the remainder is O(t^(-(d-b+2))) at
infinity. For z=0 both the remainder and all other terms vanish
identically since b>=1. Thus this leading-term calculation never
divides by a node coordinate. It is equivalently an identity in
formal Laurent series in t^(-1).

Apply (4) to the finite sum (2), treating all other parameters as
coefficients. Every coefficient involving z_i^p with b_i<p<=d_i
vanishes by the product moment identity. The coefficient for p=b_i
is beta_i tensor_product_(j!=i) G_j(t_j). Hence

    H_i(t) = (-1)^(d_i-b_i) beta_i t_i^(-(d_i-b_i+1))
                        * tensor_product_(j!=i) G_j(t_j)
              + O(t_i^(-(d_i-b_i+2))).                         (5)

The leading coefficient matrix is invertible. If r_i=Q/q_i, the
coefficient of t_i^(-(d_i-b_i+1)r_i) in det H_i is its nonzero
determinant. Thus det H_i is not the zero rational function. This
argument works for each i separately over C(t_j:j!=i); it does not
require a simultaneous limiting path for the different parameters.

### 1.5 One finite chart and dimension count

There are finitely many h factors and finitely many rational
determinants det H_i. The product of all h factors and all nonzero
numerators of those determinants is a nonzero polynomial. Over the
infinite field C it has a point of nonvanishing. Choose that finite
parameter vector. All vectors and pairings are then defined, every
U and V_i Gram matrix is invertible, and different lists are mutually
orthogonal. Their full Gram matrix is invertible. In particular their
N vectors are linearly independent in C^n, which forces n>=N.

Repeated nodes and zero coordinates were allowed throughout. Zero
weights, if initially present, can be deleted. No positivity or
rank-additivity principle was used. This proves the abstract theorem.

## 2. Reduction from every fixed-block decomposition

Write F=product_i x_i^a_i y_i^b_i and d_i=a_i+b_i. Start with any
length-n complex decomposition

    F=sum_l c_l product_i (u_(i,l)x_i+v_(i,l)y_i)^d_i.

Delete zero summands. Each remaining c_l and each factor vector is
nonzero. For each i choose gamma_i with
u_(i,l)+gamma_i v_(i,l)!=0 for all l; only finitely many choices are
excluded. Set

    z_(i,l)=v_(i,l)/(u_(i,l)+gamma_i v_(i,l)),
    w_l=c_l product_i(u_(i,l)+gamma_i v_(i,l))^d_i.

Apply product_i (partial_x_i+gamma_i partial_y_i)^(d_i-e_i)
partial_y_i^e_i to the decomposition and divide by product_i d_i!.
The resulting moments factor, with

    m_i(z_i^e) = [(d_i-e)! b_i! / ((b_i-e)! d_i!)]
                     * gamma_i^(b_i-e),             0<=e<=b_i,
    m_i(z_i^e) = 0,                                 b_i<e<=d_i.

In particular beta_i=(a_i! b_i!)/(d_i!)=1/binom(d_i,b_i), which is
nonzero, and d_i>=2b_i. Section 1 applies and gives R(F)>=N(a,b). This is a
bound on every decomposition, including ones with original support
at infinity or v_(i,l)=0. The two choices of auxiliary coordinates
are made after fixing an arbitrary finite decomposition and have
both been justified by explicit finite nonvanishing conditions.

## 3. A matching N-term upper bound by characters

Set q_i=b_i+1 and delta_i=a_i-b_i. Let delta be the column vector
of these nonnegative integers and 1 the column vector of k ones.
Define the integer matrix

    A=diag(q_1,...,q_k)+delta*1^T,

so A_ij=q_i*[i=j]+delta_i. Let Lambda=A Z^k. Column
multilinearity of the determinant (two columns contributed by the
rank-one term are proportional) gives

    det A=product_i q_i+sum_i delta_i product_(j!=i)q_j=N>0.      (6)

Thus Z^k/Lambda is a finite abelian group of order N.

### 3.1 The lattice misses the coefficient box

We claim

    Lambda intersect product_i[-a_i,b_i] = {0}.                 (7)

Suppose u=A z belongs to that box, with z in Z^k, and write
S=sum_i z_i. Then u_i=q_i z_i+delta_i S.

If S>0, the upper bound u_i<=b_i=q_i-1 and delta_i>=0 imply
q_i z_i<=q_i-1 for each i, so every z_i<=0, a contradiction.

If S<0, put H=-S>=1. The lower bound
u_i>=-a_i=-(q_i-1+delta_i) implies

    q_i z_i >= -q_i+1+(H-1)delta_i >= -q_i+1.

Consequently every z_i>=0, again a contradiction. If S=0, the
upper bounds give z_i<=0 for every i; their zero sum forces z=0.
This proves (7), including cases delta_i=0.

### 3.2 Character orthogonality gives the decomposition

Let G=Hom(Z^k/Lambda,C^*) be the character group. It has N elements.
For chi in G put theta_i(chi)=chi(e_i+Lambda), a nonzero root of
unity. The basic finite-group identity is

    sum_(chi in G) chi(u+Lambda)
      = N if u in Lambda, and 0 otherwise.                     (8)

For completeness, the finite abelian group is a product of cyclic
groups; its characters are the corresponding products of roots of
unity. The sum is a product of finite geometric sums, which proves
both its cardinality and (8).

The claimed exact decomposition is

    F = [1/(N product_i binom(d_i,a_i))]
          * sum_(chi in G) product_i theta_i(chi)^(-a_i)
                             (theta_i(chi)x_i+y_i)^d_i.        (9)

Indeed, for an exponent tuple 0<=e_i<=d_i the coefficient of
product_i x_i^e_i y_i^(d_i-e_i) on the right is

    [product_i binom(d_i,e_i)/(N product_i binom(d_i,a_i))]
       * sum_(chi in G) chi(e-a+Lambda).

Here e-a lies in product_i[-a_i,b_i]. By (7)-(8) the coefficient
vanishes unless e=a, where it equals 1. This proves (9) identically,
over C, with exactly N nonzero weighted fixed-block pure powers.
Distinct characters give distinct normalized support tuples because
the e_i generate the quotient, although only the upper bound needs
the length count. Therefore R(F)<=N, matching section 2.

## 4. Checks on scope and boundary cases

For k=1, N=a_1+1, the classical rank of a positive binary monomial.
For k=2, N=(a_1+1)(a_2+1)-(a_1-b_1)(a_2-b_2), the prior two-factor
formula. For every b_i=1, N=2^(k-1)(sum_i d_i-2k+2), the
W-product formula, now with an elementary independent upper construction.
If a_i=b_i in every coordinate, all V_i are absent and
N=product_i(b_i+1). If k=3 and (a_i,b_i)=(3,2), N=27+3*9=54.

The hypothesis b_i>=1 is used in the zero-coordinate remainder in
(4). The proposed formula is not valid generally if b_i=0 is allowed:
already x^a has rank 1, whereas the formula gives a+1 for a>=1.
No such factor is included. A pure-power factor may
instead be removed from the rank question by evaluation/contraction,
but that separate reduction is not needed for the target statement.

This proof concerns finite decompositions. There is no claimed
extension of its lower bound to border rank, no grouping of blocks,
and no restriction to decompositions of the form (9) in the lower
argument. Exact finite checker examples support the arithmetic but
do not replace the all-parameter proof.
