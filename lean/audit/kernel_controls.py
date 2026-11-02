#!/usr/bin/env python3
"""Check one valid example file and seven false moment/Gram claims."""
from pathlib import Path
import json
import subprocess
import tempfile
import time
ROOT = Path(__file__).resolve().parents[1]
SOURCES = {'MissingMoments': 'import TR29\nimport Mathlib.Tactic\n-- n=1,d=2,b=1,z=w=1 has a nonzero first moment but no vanishing second moment.\nexample : 2 - 1 + 1 ≤ (1 : ℕ) := by norm_num\n', 'MissingOrthogonality': 'import TR29\nimport Mathlib.Tactic\n-- Two identical unit vectors each have nonsingular 1x1 Gram matrix in dimension one.\n-- Their cross pairing is 1, so the claimed combined dimension is false.\nexample : (∑ _ : Fin 2, (1 : ℕ)) ≤ 1 := by norm_num\n', 'Positive': 'import TR29\nimport Mathlib.Tactic\n\nopen scoped BigOperators\nopen TR29\n\n-- Repeated nodes, a zero node and arbitrary (signed) weights are permitted.\nexample : 2 ≤ 4 := by\n  apply univariate_moment_bound 4 2 1 (by decide) (by decide)\n    ![1,-1,0,1] ![1,-1,7,0]\n  · norm_num [scalarMoment, Fin.sum_univ_succ]\n  · intro e h₁ h₂\n    have : e = 2 := by omega\n    subst e\n    norm_num [scalarMoment, Fin.sum_univ_succ]\n\nexample : (1 + PowerSeries.C (0 : ℚ)⁻¹ * PowerSeries.X) * geometricKernel 0 = 1 :=\n  geometric_kernel_identity ℚ 0\n\nexample : (momentSeries 1 (fun _ : Fin 0 => (0 : ℚ))\n    (fun _ => (0 : Matrix (Fin 0) (Fin 0) ℚ))).det ≠ 0 :=\n  (matrix_moment_leading ℚ 0 0 1 1 (by decide) (by decide) _ _\n    (by simp) (by intro e h₁ h₂; omega)).determinant_nonzero\n\nexample (H : CMatrix 2) (hH : H.det ≠ 0)\n    (A : Matrix (Fin 0 × Fin 2) (Fin 0 × Fin 2) ℂ) : A.det ≠ 0 :=\n  anti_diagonal_blocks 0 2 H A hH (by intro s; exact Fin.elim0 s)\n    (by intro s; exact Fin.elim0 s)\n\nexample : ∃ t : Fin 0 → ℂ, (∀ i _l : Fin 0, 1+t i*(0:ℂ) ≠ 0) ∧\n    (∀ _j : Fin 0, MvPolynomial.eval t (0 : MvPolynomial (Fin 0) ℂ) ≠ 0) :=\n  finite_chart_avoidance 0 0 0 (fun _ _ => 0) (fun _ => 0)\n    (by intro j; exact Fin.elim0 j)\n\nexample : (∑ b, wBlockSize 3 (fun _ => 3) b) = 20 := by decide\nexample : (∑ b, wBlockSize 1 (fun _ => 2) b) = 2 := by decide\n\n-- The small data used by the negative controls really have the advertised moments/Grams.\nexample : scalarMoment (fun _ : Fin 1 => 1) (fun _ => 1) 1 ≠ 0 := by\n  norm_num [scalarMoment]\nexample : scalarMoment (fun _ : Fin 1 => 1) (fun _ => 1) 2 = 1 := by\n  norm_num [scalarMoment]\nexample : (weightedGram (fun _ : Fin 1 => 1)\n    (fun _ : Fin 1 => fun _ => 1)).det = 1 := by\n  norm_num [weightedGram, Matrix.det_fin_one]\nexample : ¬ blocksOrthogonal (fun _ : Fin 2 => 1) (fun _ : Fin 1 => 1)\n    (fun _ _ _ => 1) := by\n  intro h\n  have hf := h 0 1 (by decide) 0 0\n  norm_num at hf\n', 'WrongBound': 'import TR29\nimport Mathlib.Tactic\n-- n=d=b=1, z=w=1 satisfies the moment assumptions; adding one to the bound is false.\nexample : 1 - 1 + 2 ≤ (1 : ℕ) := by norm_num\n', 'WrongCount': 'import TR29\nimport Mathlib.Tactic\n-- k=1,d=2 gives count 2; replacing the final +2 by +3 overstates it.\nexample : 2^(1-1) * (2-2*1+3) ≤ (2 : ℕ) := by norm_num\n', 'WrongSign': 'import TR29\nimport Mathlib.Tactic\n-- For z=M=1 the X^2 coefficient is -1, not +1.\nexample : PowerSeries.coeff 2\n    (TR29.momentSeries 1 (fun _ : Fin 1 => (1 : ℚ))\n      (fun _ => (1 : Matrix (Fin 1) (Fin 1) ℚ)) 0 0) = 1 := by\n  norm_num [TR29.momentSeries_coeff_succ]\n', 'ZeroLeading': 'import TR29\nimport Mathlib.Tactic\n-- The leading determinant assumption cannot be removed: all weights zero, q=1.\nexample : (TR29.momentSeries 1 (fun _ : Fin 1 => (1 : ℚ))\n    (fun _ => (0 : Matrix (Fin 1) (Fin 1) ℚ))).det ≠ 0 := by\n  norm_num [TR29.momentSeries]\n', 'ZeroPolynomial': 'import TR29\nimport Mathlib.Tactic\n-- A zero polynomial cannot be included in the avoidance list.\nexample : ∃ t : Fin 1 → ℂ, MvPolynomial.eval t (0 : MvPolynomial (Fin 1) ℂ) ≠ 0 := by\n  simp\n'}

def main():
    parent = ROOT / ".lake"; parent.mkdir(exist_ok=True)
    results = []
    order = ['Positive', 'WrongBound', 'MissingMoments', 'ZeroLeading', 'WrongSign', 'MissingOrthogonality', 'WrongCount', 'ZeroPolynomial']
    with tempfile.TemporaryDirectory(prefix="kernel-controls-", dir=parent) as temp:
        for name in order:
            path = Path(temp) / (name + ".lean"); path.write_text(SOURCES[name])
            start = time.monotonic()
            result = subprocess.run(["lake", "env", "lean", "-j2", str(path.relative_to(ROOT))],
                                    cwd=ROOT, capture_output=True, text=True, timeout=120)
            output = result.stdout + result.stderr
            if name == 'Positive':
                if result.returncode != 0 or 'error:' in output or 'warning:' in output:
                    raise SystemExit('FAIL: valid control rejected\n' + output)
            else:
                if result.returncode != 1 or 'unsolved goals' not in output or '⊢ False' not in output:
                    raise SystemExit('FAIL: wrong mathematical rejection: ' + name + '\n' + output)
                if any(s in output for s in ['unknown module', 'file not found', 'Unknown constant',
                        'maximum recursion', 'maximum heartbeats', 'failed to synthesize']):
                    raise SystemExit('FAIL: infrastructure error: ' + name + '\n' + output)
            results.append({'control': name, 'returncode': result.returncode,
                            'seconds': time.monotonic()-start, 'output': output})
            print(('ACCEPTED ' if name == 'Positive' else 'REJECTED ') + name, flush=True)
    (ROOT/'.lake/kernel-controls.json').write_text(json.dumps(results, indent=2)+'\n')
    print('PASS: valid algebraic controls and seven intended mathematical rejections')

if __name__ == '__main__':
    main()
