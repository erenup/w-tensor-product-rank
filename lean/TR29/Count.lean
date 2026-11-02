import TR29.Blocks
import Mathlib.Tactic

noncomputable section
namespace TR29
open scoped BigOperators

theorem sum_wBlockSize (k : ℕ) (hk : 1 ≤ k) (d : Fin k → ℕ)
    (hd : ∀ i, 2 ≤ d i) :
    (∑ b, wBlockSize k d b) = 2^(k-1) * ((∑ i, d i) - 2*k + 2) := by
  have hsum : (∑ i, d i) = (∑ i, (d i - 2)) + 2*k := by
    calc
      (∑ i, d i) = ∑ i, ((d i-2)+2) := by
        apply Finset.sum_congr rfl
        intro i _
        exact (Nat.sub_add_cancel (hd i)).symm
      _ = _ := by simp [Finset.sum_add_distrib, Nat.mul_comm]
  have hpow : 2^k = 2 * 2^(k-1) := by
    conv_lhs => rw [show k = (k-1)+1 by omega]
    rw [pow_succ, Nat.mul_comm]
  rw [Fin.sum_univ_succ]
  simp only [wBlockSize, Fin.cases_zero, Fin.cases_succ]
  rw [← Finset.sum_mul, hpow, hsum, Nat.add_sub_cancel]
  ring

theorem tr29_gram_lower_bound : TR29GramLowerBound := by
  intro k n hk d hd w v horth hdet
  have h := (orthogonal_gram_assembly n (k+1) (wBlockSize k d) w v horth hdet).2
  rwa [sum_wBlockSize k hk d hd] at h

end TR29
