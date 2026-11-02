import TR29.Definitions

/-! Universal algebraic targets.
These definitions name propositions; they do not assert their truth. -/

namespace TR29

open scoped BigOperators

/-- Full one-coordinate moment lower bound, with no support restrictions. -/
def UnivariateMomentBound : Prop :=
  ∀ (n d b : ℕ), 1 ≤ b → b ≤ d → ∀ z w : CVector n,
  scalarMoment z w b ≠ 0 →
  (∀ e : ℕ, b < e → e ≤ d → scalarMoment z w e = 0) →
  d - b + 1 ≤ n

/-- The kernel is an actual inverse, including z=0 (where both sides are 1). -/
def GeometricKernelIdentity : Prop :=
  ∀ (K : Type) [Field K] (z : K),
    (1 + PowerSeries.C z⁻¹ * PowerSeries.X) * geometricKernel z = 1

/-- All assertions about the actual matrix-valued formal expansion. -/
structure MomentLeadingConclusions (K : Type*) [Field K]
    (n q d b : ℕ) (z : Fin n → K)
    (M : Fin n → Matrix (Fin q) (Fin q) K) : Prop where
  lower_coefficients : ∀ e : ℕ, e < d - b + 1 →
    seriesCoeff (momentSeries d z M) e = 0
  first_coefficient : seriesCoeff (momentSeries d z M) (d - b + 1) =
    (-1 : K) ^ (d - b) • matrixMoment z M b
  determinant_nonzero : (momentSeries d z M).det ≠ 0

/-- Moment hypotheses imply a nonzero determinant; it is not a hypothesis. -/
def MatrixMomentLeadingTheorem : Prop :=
  ∀ (K : Type) [Field K] (n q d b : ℕ), 1 ≤ b → b ≤ d →
  ∀ (z : Fin n → K) (M : Fin n → Matrix (Fin q) (Fin q) K),
  (matrixMoment z M b).det ≠ 0 →
  (∀ e : ℕ, b < e → e ≤ d → matrixMoment z M e = 0) →
  MomentLeadingConclusions K n q d b z M

/-- The first anti-diagonal consists of H; subsequent blocks are arbitrary. -/
def AntiDiagonalBlockTheorem : Prop :=
  ∀ (r q : ℕ) (H : CMatrix q)
    (A : Matrix (Fin r × Fin q) (Fin r × Fin q) ℂ),
  H.det ≠ 0 →
  (∀ (s t : Fin r) (i j : Fin q),
    s.val + t.val + 1 < r → A (s, i) (t, j) = 0) →
  (∀ (s t : Fin r) (i j : Fin q),
    s.val + t.val + 1 = r → A (s, i) (t, j) = H i j) →
  A.det ≠ 0

/-- Generic Gram assembly. Its orthogonality and local determinants are explicit hypotheses. -/
def OrthogonalGramAssembly : Prop :=
  ∀ (n B : ℕ) (m : Fin B → ℕ) (w : CVector n)
    (v : (b : Fin B) → Fin (m b) → CVector n),
  blocksOrthogonal m w v →
  (∀ b, (weightedGram w (v b)).det ≠ 0) →
  LinearIndependent ℂ (fun u : Sigma (fun b => Fin (m b)) => v u.1 u.2) ∧
  (∑ b, m b) ≤ n

/-- The all-k numerical lower count, conditional on the displayed Gram interface. -/
def TR29GramLowerBound : Prop :=
  ∀ (k n : ℕ), 1 ≤ k → ∀ d : Fin k → ℕ, (∀ i, 2 ≤ d i) →
  ∀ (w : CVector n)
    (v : (b : Fin (k + 1)) → Fin (wBlockSize k d b) → CVector n),
  blocksOrthogonal (wBlockSize k d) w v →
  (∀ b, (weightedGram w (v b)).det ≠ 0) →
  2 ^ (k - 1) * ((∑ i, d i) - 2 * k + 2) ≤ n

/-- Simultaneously avoid every coordinate pole and a finite list of nonzero polynomials. -/
def FiniteChartAvoidance : Prop :=
  ∀ (k n r : ℕ) (z : Fin k → Fin n → ℂ)
    (p : Fin r → MvPolynomial (Fin k) ℂ),
  (∀ j, p j ≠ 0) →
  ∃ t : Fin k → ℂ,
    (∀ i l, 1 + t i * z i l ≠ 0) ∧
    (∀ j, MvPolynomial.eval t (p j) ≠ 0)

/-- All seven targets are required; no one lemma alone completes this scope. -/
def CoreTheorems : Prop :=
  UnivariateMomentBound ∧ GeometricKernelIdentity ∧ MatrixMomentLeadingTheorem ∧
  AntiDiagonalBlockTheorem ∧ OrthogonalGramAssembly ∧ TR29GramLowerBound ∧
  FiniteChartAvoidance

end TR29
