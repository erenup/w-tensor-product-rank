import TR29.Statement
import Mathlib.Tactic

noncomputable section
namespace TR29
open scoped BigOperators

variable {K : Type*} [Field K]

@[simp] theorem kernel_coeff (z : K) (e : ℕ) :
    PowerSeries.coeff e (geometricKernel z) = (-z⁻¹)^e := by
  simp [geometricKernel]

theorem geometric_kernel_identity : GeometricKernelIdentity := by
  intro K _ z
  ext e
  rw [add_mul, one_mul, mul_assoc]
  cases e with
  | zero => simp [geometricKernel, PowerSeries.constantCoeff_mk]
  | succ e =>
    simp only [map_add, PowerSeries.coeff_C_mul, PowerSeries.coeff_succ_X_mul,
      kernel_coeff, PowerSeries.coeff_one, Nat.succ_ne_zero, ite_false]
    rw [pow_succ]
    ring

@[simp] theorem momentSeries_coeff_zero {n q d : ℕ} (z : Fin n → K)
    (M : Fin n → Matrix (Fin q) (Fin q) K) (i j : Fin q) :
    PowerSeries.coeff 0 (momentSeries d z M i j) = 0 := by
  simp [momentSeries]

theorem momentSeries_coeff_succ {n q d : ℕ} (z : Fin n → K)
    (M : Fin n → Matrix (Fin q) (Fin q) K) (i j : Fin q) (e : ℕ) :
    PowerSeries.coeff (e+1) (momentSeries d z M i j) =
      ∑ l, M l i j * z l ^ d * (- (z l)⁻¹)^e := by
  change PowerSeries.coeff (e+1) ((PowerSeries.X : PowerSeries K) * _) = _
  rw [PowerSeries.coeff_succ_X_mul, map_sum]
  apply Finset.sum_congr rfl
  intro l _
  rw [PowerSeries.coeff_C_mul, kernel_coeff]

/-- The finite coefficient identity includes z=0 as long as the remaining power is positive. -/
theorem power_cancel_with_zero (z : K) (d e : ℕ) (he : e < d) :
    z^d * (-z⁻¹)^e = (-1 : K)^e * z^(d-e) := by
  by_cases hz : z = 0
  · subst z
    have hd : d ≠ 0 := by omega
    have hde : d-e ≠ 0 := by omega
    simp [hd, hde]
  · rw [neg_eq_neg_one_mul, mul_pow]
    have hd : d = e + (d-e) := by omega
    conv_lhs => rw [hd, pow_add]
    rw [show z^e * z^(d-e) * ((-1 : K)^e * z⁻¹^e) =
      (-1 : K)^e * z^(d-e) * (z^e * z⁻¹^e) by ring,
      ← mul_pow, mul_inv_cancel₀ hz, one_pow, mul_one]

/-- Entrywise vanishing to order D with an invertible leading matrix forces a nonzero determinant. -/
theorem det_ne_zero_of_leading {q : ℕ} (H : SeriesMatrix K q) (D : ℕ)
    (hlow : ∀ e, e < D → seriesCoeff H e = 0)
    (hlead : (seriesCoeff H D).det ≠ 0) : H.det ≠ 0 := by
  classical
  have hdiv : ∀ i j, ∃ f : PowerSeries K, H i j = PowerSeries.X^D * f := by
    intro i j
    apply PowerSeries.X_pow_dvd_iff.mpr
    intro e he
    exact congrFun (congrFun (hlow e he) i) j
  choose f hf using hdiv
  let F : SeriesMatrix K q := Matrix.of f
  have hF : ∀ i j, H i j = PowerSeries.X^D * F i j := hf
  have hmatrix : H = (PowerSeries.X^D : PowerSeries K) • F := by
    apply Matrix.ext
    intro i j
    exact hF i j
  have hconstant : F.map PowerSeries.constantCoeff = seriesCoeff H D := by
    ext i j
    change PowerSeries.constantCoeff (F i j) = PowerSeries.coeff D (H i j)
    rw [hF i j]
    simpa using (PowerSeries.coeff_X_pow_mul (F i j) D 0).symm
  have hdetF : F.det ≠ 0 := by
    intro hz
    apply hlead
    rw [← hconstant]
    change (PowerSeries.constantCoeff.mapMatrix F).det = 0
    rw [← RingHom.map_det, hz, map_zero]
  rw [hmatrix, Matrix.det_smul]
  exact mul_ne_zero (pow_ne_zero _ (pow_ne_zero _ PowerSeries.X_ne_zero)) hdetF

theorem momentSeries_coeff_small {n q d : ℕ} (z : Fin n → K)
    (M : Fin n → Matrix (Fin q) (Fin q) K) (e : ℕ) (he : e < d) :
    seriesCoeff (momentSeries d z M) (e+1) =
      (-1 : K)^e • matrixMoment z M (d-e) := by
  ext i j
  change PowerSeries.coeff (e+1) (momentSeries d z M i j) =
    (-1 : K)^e * (∑ l, M l i j * z l ^ (d-e))
  rw [momentSeries_coeff_succ, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro l _
  rw [mul_assoc, power_cancel_with_zero _ _ _ he]
  ring

theorem matrix_moment_leading : MatrixMomentLeadingTheorem := by
  intro K _ n q d b hb hbd z M hdet hvan
  have hlow : ∀ e, e < d-b+1 → seriesCoeff (momentSeries d z M) e = 0 := by
    intro e he
    cases e with
    | zero => ext i j; exact momentSeries_coeff_zero z M i j
    | succ e =>
      rw [momentSeries_coeff_small z M e (by omega), hvan (d-e) (by omega) (by omega)]
      simp
  have hfirst : seriesCoeff (momentSeries d z M) (d-b+1) =
      (-1 : K)^(d-b) • matrixMoment z M b := by
    rw [momentSeries_coeff_small z M (d-b) (by omega), Nat.sub_sub_self hbd]
  refine ⟨hlow, hfirst, det_ne_zero_of_leading _ _ hlow ?_⟩
  rw [hfirst, Matrix.det_smul]
  exact mul_ne_zero (pow_ne_zero _ (pow_ne_zero _ (neg_ne_zero.mpr one_ne_zero))) hdet

end TR29
