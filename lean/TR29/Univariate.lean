import TR29.Statement
import Mathlib.Tactic

noncomputable section
namespace TR29
open scoped BigOperators
open Polynomial

/-- The annihilator of the nonzero nodes extracts the first nonzero moment. -/
theorem univariate_moment_bound : UnivariateMomentBound := by
  classical
  intro n d b hb hbd z w hnon hvan
  by_contra hbound
  have hn : n ≤ d-b := by omega
  let s : Finset (Fin n) := Finset.univ.filter (fun l => z l ≠ 0)
  let Q : Polynomial ℂ := ∏ l ∈ s, (X - C (z l))
  have hdeg : Q.natDegree ≤ n := by
    calc
      Q.natDegree ≤ ∑ l ∈ s, (X - C (z l)).natDegree := natDegree_prod_le _ _
      _ = s.card := by simp
      _ ≤ n := by simpa using Finset.card_le_card (Finset.filter_subset (fun l => z l ≠ 0) Finset.univ)
  have hQ0 : Q.coeff 0 ≠ 0 := by
    rw [coeff_zero_eq_eval_zero]
    change (eval 0 (∏ l ∈ s, (X - C (z l)))) ≠ 0
    simp only [eval_prod, eval_sub, eval_X, eval_C, zero_sub]
    apply Finset.prod_ne_zero_iff.mpr
    intro l hl
    exact neg_ne_zero.mpr (Finset.mem_filter.mp hl).2
  have hQz : ∀ l, z l ^ b * Q.eval (z l) = 0 := by
    intro l
    by_cases hz : z l = 0
    · simp [hz, show b ≠ 0 by omega]
    · have hl : l ∈ s := Finset.mem_filter.mpr ⟨Finset.mem_univ _, hz⟩
      have hroot : Q.eval (z l) = 0 := by
        dsimp [Q]
        rw [eval_prod]
        apply Finset.prod_eq_zero hl
        simp
      rw [hroot, mul_zero]
  have hsum : (∑ l, w l * z l ^ b * Q.eval (z l)) = 0 := by
    apply Finset.sum_eq_zero
    intro l _
    rw [mul_assoc, hQz, mul_zero]
  have hexpand : (∑ l, w l * z l ^ b * Q.eval (z l)) =
      ∑ e ∈ Finset.range (n+1), Q.coeff e * scalarMoment z w (b+e) := by
    simp_rw [Q.eval_eq_sum_range' (show Q.natDegree < n+1 by omega), Finset.mul_sum]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro e _
    simp only [scalarMoment, Finset.mul_sum, pow_add]
    apply Finset.sum_congr rfl
    intro l _
    ring
  have hextract : (∑ e ∈ Finset.range (n+1), Q.coeff e * scalarMoment z w (b+e)) =
      Q.coeff 0 * scalarMoment z w b := by
    rw [Finset.sum_eq_single 0]
    · simp
    · intro e he hne
      rw [hvan (b+e) (by omega) (by have := Finset.mem_range.mp he; omega), mul_zero]
    · simp
  rw [hexpand, hextract] at hsum
  exact mul_ne_zero hQ0 hnon hsum

end TR29
