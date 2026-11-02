import Mathlib.LinearAlgebra.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.Dimension.Finite
import Mathlib.RingTheory.PowerSeries.Inverse
import Mathlib.Algebra.MvPolynomial.Funext
import Mathlib.Data.Complex.Basic

/-! Literal algebraic operations for the universal TR-29 proof core. -/

noncomputable section

namespace TR29

open scoped BigOperators

abbrev CVector (n : ℕ) := Fin n → ℂ
abbrev CMatrix (q : ℕ) := Matrix (Fin q) (Fin q) ℂ
abbrev SeriesMatrix (K : Type*) (q : ℕ) := Matrix (Fin q) (Fin q) (PowerSeries K)

/-- The actual weighted scalar moment, with no assumptions on nodes or weights. -/
def scalarMoment {n : ℕ} (z w : CVector n) (e : ℕ) : ℂ :=
  ∑ l, w l * z l ^ e

/-- An actual matrix-valued moment; M may absorb other-coordinate factors. -/
def matrixMoment {K : Type*} [Field K] {n q : ℕ}
    (z : Fin n → K) (M : Fin n → Matrix (Fin q) (Fin q) K)
    (e : ℕ) : Matrix (Fin q) (Fin q) K :=
  Matrix.of fun i j => ∑ l, M l i j * z l ^ e

/-- Formal expansion of (1+X/z)^(-1); its inverse identity is a target. -/
def geometricKernel {K : Type*} [Field K] (z : K) : PowerSeries K :=
  PowerSeries.mk fun e => (-z⁻¹) ^ e

/-- The literal formal expansion of sum M_l z_l^(d+1)/(1+t z_l), X=t^(-1).
At a zero node the z^d factor vanishes whenever d>=1. -/
def momentSeries {K : Type*} [Field K] {n q : ℕ} (d : ℕ) (z : Fin n → K)
    (M : Fin n → Matrix (Fin q) (Fin q) K) : SeriesMatrix K q :=
  Matrix.of fun i j => PowerSeries.X *
    ∑ l, PowerSeries.C (M l i j * z l ^ d) * geometricKernel (z l)

/-- Coefficient extraction from every entry; not a coefficient of the determinant. -/
def seriesCoeff {K : Type*} [Field K] {q : ℕ} (H : SeriesMatrix K q) (e : ℕ) :
    Matrix (Fin q) (Fin q) K :=
  Matrix.of fun i j => PowerSeries.coeff e (H i j)

/-- Weighted bilinear Gram matrix, not a Hermitian matrix. -/
def weightedGram {n q : ℕ} (w : CVector n) (v : Fin q → CVector n) : CMatrix q :=
  Matrix.of fun i j => ∑ l, w l * v i l * v j l

/-- Actual cross-block pairing; no assertion of dimension additivity is built in. -/
def blocksOrthogonal {n B : ℕ} (m : Fin B → ℕ) (w : CVector n)
    (v : (b : Fin B) → Fin (m b) → CVector n) : Prop :=
  ∀ b c, b ≠ c → ∀ (i : Fin (m b)) (j : Fin (m c)),
    ∑ l, w l * v b i l * v c j l = 0

/-- Label 0 is U; label i+1 is V_i. Zero-sized V blocks are retained. -/
def wBlockSize (k : ℕ) (d : Fin k → ℕ) : Fin (k + 1) → ℕ :=
  Fin.cases (2 ^ k) (fun i => (d i - 2) * 2 ^ (k - 1))

end TR29
