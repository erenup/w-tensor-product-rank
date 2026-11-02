import TR29.Statement
import Mathlib.Tactic

noncomputable section
namespace TR29
open scoped BigOperators

theorem exists_evaluation_ne_zero {k : ℕ} {p : MvPolynomial (Fin k) ℂ}
    (hp : p ≠ 0) : ∃ t : Fin k → ℂ, MvPolynomial.eval t p ≠ 0 := by
  classical
  by_contra h
  push Not at h
  apply hp
  apply MvPolynomial.funext
  intro t
  simpa using h t

theorem finite_chart_avoidance : FiniteChartAvoidance := by
  classical
  intro k n r z p hp
  let P : Fin r ⊕ (Fin k × Fin n) → MvPolynomial (Fin k) ℂ :=
    Sum.elim p (fun u => 1 + MvPolynomial.C (z u.1 u.2) * MvPolynomial.X u.1)
  have hP : ∀ a, P a ≠ 0 := by
    intro a
    cases a with
    | inl j => exact hp j
    | inr u =>
      intro h
      have he := congrArg (MvPolynomial.eval (fun _ : Fin k => (0 : ℂ))) h
      simp [P] at he
  have hprod : (∏ a, P a) ≠ 0 := Finset.prod_ne_zero_iff.mpr (by simp [hP])
  obtain ⟨t, ht⟩ := exists_evaluation_ne_zero hprod
  have hall : ∀ a, MvPolynomial.eval t (P a) ≠ 0 := by
    rw [map_prod] at ht
    exact fun a => Finset.prod_ne_zero_iff.mp ht a (Finset.mem_univ a)
  refine ⟨t, ?_, ?_⟩
  · intro i l
    simpa [P, mul_comm] using hall (Sum.inr (i, l))
  · intro j
    exact hall (Sum.inl j)

end TR29
