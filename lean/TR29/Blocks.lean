import TR29.Statement
import Mathlib.Tactic

noncomputable section
namespace TR29
open scoped BigOperators

/-- Reversal of the first block coordinate converts the anti-diagonal into a diagonal. -/
theorem anti_diagonal_blocks : AntiDiagonalBlockTheorem := by
  classical
  intro r q H A hH hzero hanti
  let rev : Equiv.Perm (Fin r × Fin q) := Equiv.prodCongr Fin.revPerm (Equiv.refl _)
  let B := A.submatrix rev id
  have ht : B.BlockTriangular Prod.fst := by
    intro u v huv
    apply hzero
    change v.1.val < u.1.val at huv
    simp only [Fin.revPerm_apply, Fin.val_rev]
    omega
  have hd : ∀ s : Fin r, (B.toSquareBlock Prod.fst s).det ≠ 0 := by
    intro s
    let e : Fin q ≃ {u : Fin r × Fin q // u.1 = s} :=
      { toFun := fun i => ⟨(s,i), rfl⟩
        invFun := fun u => u.1.2
        left_inv := fun _ => rfl
        right_inv := by intro u; apply Subtype.ext; exact Prod.ext u.2.symm rfl }
    have he : (B.toSquareBlock Prod.fst s).submatrix e e = H := by
      ext i j
      change A (Fin.rev s,i) (s,j) = H i j
      apply hanti
      simp only [Fin.val_rev]
      omega
    rw [← Matrix.det_submatrix_equiv_self e, he]
    exact hH
  have hB : B.det ≠ 0 := by
    rw [ht.det_fintype]
    exact Finset.prod_ne_zero_iff.mpr (fun s _ => hd s)
  intro hA
  apply hB
  change (A.submatrix rev id).det = 0
  rw [Matrix.det_permute, hA, mul_zero]

/-- Orthogonal nonsingular bilinear Gram blocks give independence of the actual vectors. -/
theorem orthogonal_gram_assembly : OrthogonalGramAssembly := by
  classical
  intro n B m w v horth hblock
  let I := Sigma (fun b => Fin (m b))
  let G : Matrix I I ℂ := fun u t => ∑ l, w l * v u.1 u.2 l * v t.1 t.2 l
  have htri : G.BlockTriangular Sigma.fst := by
    intro u t hut
    exact horth _ _ (ne_of_gt hut) _ _
  have hdiag : ∀ b : Fin B, (G.toSquareBlock Sigma.fst b).det ≠ 0 := by
    intro b
    let e : Fin (m b) ≃ {u : I // u.1 = b} :=
      { toFun := fun i => ⟨⟨b,i⟩, rfl⟩
        invFun := fun u => u.2 ▸ u.1.2
        left_inv := fun _ => rfl
        right_inv := by
          rintro ⟨⟨c,j⟩,h⟩
          dsimp only at h
          subst c
          rfl }
    have he : (G.toSquareBlock Sigma.fst b).submatrix e e = weightedGram w (v b) := by
      ext i j
      rfl
    rw [← Matrix.det_submatrix_equiv_self e, he]
    exact hblock b
  have hG : G.det ≠ 0 := by
    rw [htri.det_fintype]
    exact Finset.prod_ne_zero_iff.mpr (fun b _ => hdiag b)
  let L : CVector n →ₗ[ℂ] (I → ℂ) :=
    { toFun := fun x t => ∑ l, w l * x l * v t.1 t.2 l
      map_add' := by
        intro x y; ext t
        simp [mul_add, add_mul, Finset.sum_add_distrib]
      map_smul' := by
        intro c x; ext t
        simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro l _
        ring }
  have hlin : LinearIndependent ℂ (fun u : I => v u.1 u.2) :=
    (Matrix.linearIndependent_rows_of_det_ne_zero hG).of_comp L
  refine ⟨hlin, ?_⟩
  simpa [I, Module.finrank_fintype_fun_eq_card] using hlin.fintype_card_le_finrank

end TR29
