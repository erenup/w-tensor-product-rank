# Check of the applied corrections (Sections 1–7)

**Verdict: CORRECT.** All twelve corrections agreed by the two referees of Sections 1–7 are applied, every changed passage is one of them or one of the intended front-matter changes (author block, declarations), and nothing else changed. The unchanged files (`references.bib`, `00_introduction`, `03_generalized_moments`, `05_rank`, `A_block_entries`) are byte-identical to the reviewed version.

| Edited place | Correction | Check |
|---|---|---|
| 01_coordinates.tex:3-4, 25-30, 34-35 | item 1 | OK. A summand is zero iff c_l=0 or some (a_il,b_il)=(0,0); a+γb=0 iff γ=-a/b; hence every w_l≠0. |
| 02_moments.tex:21-24, 26-28 | item 2 | OK. binom(d,0)=1 and binom(d,1)=d give γ_i, 1/d_i, 0; the right side gives binom(d,e) z^e. |
| 04_gram.tex:5-6 | item 3 | OK. "Admissible" is used at 05:24 and 06:64, 86, 193. |
| 04_gram.tex:24-27 | item 4 | OK. The cross, basic and s+s'≤d_i entries all lie in P_d. |
| 06_test_functions.tex:30-31 | item 8 | OK. |
| 06_test_functions.tex:107-110 | item 5 | OK. Degree is d_j-1+ι_j ≤ d_j; the reference is to the correct display of Appendix A. |
| 06_test_functions.tex:197 | item 6 | OK. The leading term is invertible for every fixed t_j because det G_j = -β_j² ≠ 0. |
| 06_test_functions.tex:224-227 | item 7 | OK. A common denominator of the q×q matrix is ∏(1+t_i z)^q, so N_i ∈ C[t] and N_i ≠ 0. |
| 06_test_functions.tex:273-275 | item 8, optional remark | OK. k=1 (M=d, q=1, empty tensor product) and d_i=2 (B_i empty, G_i invertible) re-checked. |
| B_laurent.tex:11, 33-34, 41, 43 | item 9 | OK. The summation index is renamed consistently; the division identity telescopes correctly. |
| B_laurent.tex:61-64 | item 6 | OK. Denominators involve only t_i, so specializing the other t_j is a ring map. |
| main.tex (abstract, Lean sentence) | items 10, 12 | OK. Nothing beyond the formal scope is claimed. |
| sketch macros | item 11 | OK. Unused macros removed. |

**Build.** Both documents rebuilt out of tree with `latexmk`: exit 0, no undefined or multiply defined references, no citation or BibTeX warnings; the text of each rebuilt PDF equals the reviewed PDF.

**Optional improvements suggested and subsequently applied:** the Lean sentence names the identification of each block H_i with its formal expansion among the text-only steps; the sentence in `04_gram.tex` reads "Among the entries outside P_d, only those with s+s'=d_i+1 … are needed".
