import TR29.Univariate
import TR29.Series
import TR29.Blocks
import TR29.Count
import TR29.Avoidance

namespace TR29

/-- All seven universal algebraic targets, with their literal definitions. -/
theorem core_theorems : CoreTheorems :=
  ⟨univariate_moment_bound, geometric_kernel_identity, matrix_moment_leading,
    anti_diagonal_blocks, orthogonal_gram_assembly, tr29_gram_lower_bound,
    finite_chart_avoidance⟩

end TR29
