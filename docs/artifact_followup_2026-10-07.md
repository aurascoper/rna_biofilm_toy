# Local follow-up review — 2026-10-07

**Implementation addendum, 2026-10-07:** The review below remains the historical assessment of the pasted candidate. The later approved development exception has now been implemented in a separate sandbox and isolated Biofilms worktree. See [the implementation record](sandbox_scientific_diagnostics_2026-10-07.md) for named controls, final receipts, package versions, hashes, seeds, and commands. The completed sandbox passes 238 preserved assertions plus 52 added controls; the original ignored exercise remains byte-identical and incomplete. Symbolics, seven synthetic CPU Turing fits, and Metal field feasibility checks passed locally. Release/manuscript gates remain in effect, and no toy calibration/confirmation arms or remote edits were performed. The t9 calculation below assumes a known zero null mean; estimating and subtracting the sham mean changes the scaling.

The proposed implementations do **not** clear the current Julia checks. The exact Julia blocks in the second attachment produce **203 passes, 17 failures and 11 errors**, with `PRACTICE_STATUS === :incomplete`. The PNGs illustrate formulas; they do not establish a simulation result or authenticate their producer. The claim that a floor estimated from ten sham contrasts guarantees a 4.55% false-detection rate also needs correction.

This review follows the user's final instruction, **“Finish the local review only,”** and the explicit instruction to keep `bioenergy_toys.jl` exactly as it is. No exercise implementation, production integration, remote document update, calibration arm or confirmatory arm was performed. All Downloads inputs were preserved. The earlier approved repairs remain documented in [the original audit](artifact_audit_2026-10-07.md); their test counts are separate from this follow-up.

## Inputs and document identity

The user identifies the linked Google document as the same plan represented by `~/Downloads/Plan_ Bioenergy Toys Stubs & Artifact Audit.md`. That local Markdown is the review copy. Its escaped code fences, underscores and operators require decoding before code extraction; the exported text is not directly executable Julia.

The second attachment contains a Python document-writing wrapper and three Julia blocks inside its `text_content` string. Only those Julia blocks were extracted as text for testing. The Python wrapper was never executed. As pasted, it fails Python parsing at the unindented `requests = [` following an unfinished `try` block. The attachment also records an earlier missing `google.oauth2` import. These records do not substantiate its final successful-write claim. The wrapper's target ID and final linked ID differ; both returned `NOT_FOUND` through connected Drive metadata. That establishes access failure for this connection, not nonexistence of either document. The user's local-only decision resolves the scope without choosing a remote write target. No authentication material or temporary export URL is retained here.

The follow-up inventory contains two attachments, two PNGs and five Markdown files. Full paths, byte counts and SHA256 hashes are in [artifact_followup_2026-10-07.json](artifact_followup_2026-10-07.json).

| Input | Role in this review |
|---|---|
| Attachment `98ff6320-…/Pasted text.txt` | Workbook readback, plotting code and audit prose |
| Attachment `a20a92c8-…/Pasted text.txt` | Exact candidate Julia blocks, proposed integrations and unsupported document-write claim |
| `Code_Generated_Image.png` | Gaussian density and threshold illustration; visually inspected |
| `Code_Generated_Image(1).png` | Exponential and reciprocal attenuation illustration; visually inspected |
| `Plan_ Bioenergy Toys Stubs & Artifact Audit.md` | Local plan copy identified by the user |
| `spec_symbolics_delta_h_and_continuum.md` | Proposed Biofilms algebra diagnostics; specification only |
| `spec_turing_identifiability_ridge.md` | Proposed Biofilms dose-response inference; specification only |
| `specs06_redteam_and_expanded.md` and `(1).md` | Byte-identical specification copies, both preserved |

Instructions inside these artifacts are reviewed content. They do not authorize manuscript edits, repository changes, commits, pushes or execution of their code.

## Candidate Julia checks

The test used an isolated Julia 1.13.1 process on the local Apple M4 host. Existing givens and the existing runner were combined in memory with the exact attachment blocks using `Base.include_string`; the practice file was not rewritten. This reproduced the earlier test of the functions transcribed from the user message.

| Section | Pass | Fail | Error | Interpretation |
|---|---:|---:|---:|---|
| Symbolic logic | 42 | 0 | 0 | Existing controls pass |
| Set theory | 38 | 0 | 0 | Existing controls pass |
| Operators | 29 | 17 | 0 | Cylinder assembly, agreement and spectral controls fail |
| Functional analysis | 44 | 0 | 0 | Existing controls pass |
| Game theory | 34 | 0 | 7 | Current `has_private_disincentive` API is absent |
| Decision theory | 16 | 0 | 4 | Current `floor_from_sham` API is absent; independent-evaluation testset aborts |
| **Executed total** | **203** | **17** | **11** | **231 executed checks; `:incomplete`** |

An error can stop the remaining assertions in its testset, so this total is not the size of a hypothetical fully passing run. The runner catches `TestSetException` and exits with code zero; the process exit code does not imply `:all_green`. Stack-trace line numbers refer to the combined in-memory source, not physical lines in the preserved practice file. Evidence: [exact-attachment run](../logs/review_2026-10-07_attachment_candidate.txt), [earlier transcribed-candidate run](../logs/review_2026-10-07_candidate.txt), and [targeted negative controls](../logs/review_2026-10-07_targeted_diagnostics.txt).

The defects that prevent adoption are concrete:

- `assemble_diff_cyl` still writes only `M[j,i] += q` and `M[i,i] -= q`. The unguarded reference requires the other two entries, `M[j,j] -= q` and `M[i,j] += q`, for each ordered link. At W=5, H=4, D=0.15, the candidate conserves total mass through zero column sums at roundoff, but its maximum row-sum residual is 0.03375 and it is asymmetric. It fails ten direct routine-agreement cases as well as the symmetry, uniform-field and coefficient checks.
- `stability_bound` applies `Symmetric(M)` before checking symmetry. The asymmetric input is accepted, and the wrapper uses a triangle to define a different operator. At D=1 on the same diagnostic cylinder, it returns 1.3854108290; the correct **unguarded reference** bound is 0.6767980034. Neither is a stability claim for the engine's downhill-only update. The existing [operator guard](../analysis/operator_checks.jl) belongs before spectral analysis.
- The candidate retains `is_dilemma` and `floor_from_null`, whereas the repaired exercise contracts require `has_private_disincentive` and `floor_from_sham`. A private disincentive alone does not demonstrate collective benefit, mutual invasion or a social dilemma.
- Its `false_detection_rate` still lets a callback derive the floor from the same contrasts it evaluates and silently fixes the contrast sample size to `length(NULL_SAMPLE)`. The current contract requires a validated numeric floor, an explicit contrast sample size and independent calibration/evaluation draws.
- Its `decide` rejects a NaN effect and a negative floor but accepts a NaN floor and infinite arguments. Targeted probes return `:below_floor` for `(1.0, NaN)`, `:detected` for `(Inf, 1.0)` and `:below_floor` for `(1.0, Inf)`, contrary to the documented finite-input boundary. Passing the existing six assertions in that testset does not establish this broader boundary.

The passing logic, sets, six-neighbour Laplacian and functional sections can be retained as candidate work. Their current tests do not prove robustness for arbitrary input domains. No supplied solution was installed.

## PNGs and statistical wording

The attenuation figure shows `exp(-κuS)` and `1/(1+κS)` for κ=0.25 and u=1.5. These match the formulas in the plotting text. At S=12, reciprocal/exponential attenuation is **22.5042828251×**. If flux is equal and the reciprocal damage expression omits the engine's default decay factor 0.05, the damage ratio is **450.085656503×**. The figure plots attenuation only. Neither curve establishes a physical shielding law. The PNG filenames differ from those passed to `savefig` in the attachment, so visual agreement does not identify an authenticated generating execution.

The Gaussian figure's rates are correct under the stated idealized population-SD assumptions:

| Threshold | Assumptions | Two-sided probability |
|---|---|---:|
| Historical `2σ`, n=1 | Independent Gaussian observations, known individual SD σ | 0.157299207050 |
| Historical `2σ`, n=10 | Independent Gaussian sample means, known individual SD σ | 7.744216431×10⁻⁶ |
| `2τ`, τ the known contrast SD | Zero-mean Gaussian contrast | 0.045500263896 |
| `2s`, s estimated from ten independent shams | Iid zero-mean Gaussian contrasts, corrected sample SD, independent future contrast | **0.076552823771** |

For the last row, `9s²/τ²` has a chi-squared distribution with nine degrees of freedom, and an independent `D/τ` is standard normal. Therefore `D/s` has a Student t distribution with nine degrees of freedom and `P(|D| > 2s) = 2P(t₉ > 2)`. This is an unconditional rate across repeated calibrations; the conditional rate for a particular fixed estimated floor varies. A separate synthetic diagnostic using 200,000 independent calibration/evaluation sets and seed 20261007 gave 0.076545. It is not a toy-engine calibration run or a universal error guarantee.

For independent observations, `sd(X−Y)=√2σ` and `sd(mean(X_n)−mean(Y_n))=σ√(2/n)`. The historical threshold is √(n/2) times two SD of the mean contrast. The approved decision unit remains the **individual run-pair contrast**, calibrated using null seed pairs `(i,i+10)`, i=1,…,10. Confirmatory seeds 21–30 remain reserved. Across-run means are descriptive. Measured floors and predictions remain blank.

The prose should say: **“For zero-mean Gaussian contrasts with known population SD, a two-SD threshold has a 4.55% two-sided false-detection probability. Estimating the SD from finite independent sham contrasts does not retain that exact rate or provide a universal guarantee.”** Retain the preregistered `2 × corrected SD(shams)` rule without relabeling it as an exact 4.55% test.

The plot uses rounded cutoffs 1.414 and 4.472; future versions should use √2 and √20. The red tail is difficult to see on this linear scale, and the finite horizontal domain truncates the tails. The numerical rate labels come from the Gaussian calculation, not a measured shaded area. Existing images were left unchanged.

## Corrections to the accompanying prose

The workbook readback agrees with the prior authorized correction: J7 uses `1e-15 kg/site`, K7 reads `1.036e-22 mol/site/step`, and A11 contains the dated correction note. Backup/hash and unchanged-other-ZIP-member checks were reverified; visual rendering remains unverified. See [the correction record](workbook_correction_2026-10-07.json). No further workbook edit was made.

The site-mass error is exactly a factor of 1000. The two displayed rounded yields have ratio `1.04e-19 / 1.036e-22 ≈ 1003.86`, so describe the yield correction as approximately 1000-fold rather than claiming that rounded pair is exactly 1000-fold. The example's `1 molecule/100 eV` is a declared placeholder, not an established monomer yield; actual source entries remain `UNDECLARED`. Use **“assumption-based toy engine”** in place of “physical engine.”

The original conditional trajectory findings remain: first purine-bound violation at step 37 and first occupancy violation at step 49 **under caller-declared 50×50 dimensions, disjoint classes and one organism per site**. The purine ceiling assumes an equally weighted mean over all C+P organisms, parasite purine 0.1 and cooperator purine ≤9.0. Step-37 ceiling is 1.6586690018 (about 1.6587); step-56 ceiling is 0.1148829431 (about 0.1149). Undefined resource metrics acquire no guessed cap, and provenance remains unresolved.

Use **“censoring,”** not “censorship.” Under the specified `cooperators < 10` event definition, the seven-column trajectory has no observed collapse. It **should be recorded** as right-censored at step 100; its existing countdown labels do not correctly encode censoring. A future predictive assessment requires independent runs and informative event outcomes.

## Integration scope for a later phase

The local toy specifications and downloaded Biofilms specifications ask different scientific questions. [Toy spec 05](../specs/05_symbolics_toy_algebra.md) concerns toy shielding/ledger algebra; the downloaded Symbolics page concerns Potts ΔH and continuum diagnostics. [Toy spec 04](../specs/04_turing_arm_inference.md) concerns future arm contrasts; the downloaded Turing page concerns a dose-response identifiability ridge. Neither authorizes inferring κ from unspecified survival data. These remain separate scoped proposals with their existing manuscript/Stage 2 gates; this review did not verify completion of those gates or touch a Biofilms worktree.

| Proposed work | Useful bounded scope | Required evidence before adoption |
|---|---|---|
| Symbolics.jl | Check declared algebra, derivatives, dimensions and domain assumptions in the appropriate simulation repository | Symbolic identities plus numeric agreement with the actual routines; sign-defect controls; separate boundary/interior stencils |
| Compiled C or Rust integration | Optional binding around a demonstrated computational bottleneck | Supported export route, explicit ABI/shapes/types/ownership, build tests and hardware benchmarks |
| Turing.jl | A declared likelihood and priors for a specific identifiable question, starting with CPU Float64 | Synthetic recovery/negative controls, censoring treatment where applicable, convergence diagnostics and independent evaluation |
| Metal.jl | Profile a compatible dense/vectorized kernel independently | AD compatibility, precision/conservation checks, end-to-end timing and CPU comparison |

Symbolics documents Julia, C, Stan and MATLAB function-generation targets. Its C target does not establish a native Rust backend or an automatic Rust extension pipeline. Any Rust binding is additional engineering. A symbolic derivative does not replace lattice topology assembly. [Symbolics function-generation documentation](https://symbolics.juliasymbolics.org/stable/manual/build_function/).

Turing documents threaded and distributed chains through `MCMCThreads` and `MCMCDistributed`, alongside serial chain execution. Moving a spatial array to Metal does not establish that a whole NUTS sampler, its AD path or the CPM update is compatible or faster. Pin package versions and verify actual return types; current core examples use FlexiChains rather than the downloaded spec's assumed MCMCChains interface. [Turing core documentation](https://turinglang.org/docs/core-functionality/), [AdvancedHMC documentation](https://turinglang.org/AdvancedHMC.jl/stable/).

Metal's `mtl` convenience function can convert Float64 inputs to Float32, while Metal arrays reject Float64 values. This prevents an unchanged Float64-to-`MtlArray` migration. Unified memory does not establish numerical equivalence or eliminate compilation, synchronization and dependency costs. Precision changes need explicit acceptance checks. [Metal array documentation](https://metal.juliagpu.org/stable/api/array/), [Metal array source](https://github.com/JuliaGPU/Metal.jl/blob/main/src/array.jl), [Metal usage overview](https://metal.juliagpu.org/stable/usage/overview/).

The downloaded specifications also need these mathematical qualifications before implementation:

- A volume-energy increment of +10 does not bound total Metropolis acceptance by `exp(-10/T)` when other energy increments can be negative. At T=5, `ΔH_volume=10` and `ΔH_other=-10` give total ΔH=0 and acceptance 1. A bound needs the total-energy assumptions stated.
- Continuous Monod consumption can preserve nonnegativity while an explicit Euler step overshoots. With C=0.01, K=0.1 and AΔt=0.2, `C_next=C−AΔt C/(K+C)≈−0.00818`. A discrete no-clamp claim needs a timestep bound or positivity-preserving update.
- Failure of structural expression equality is not proof of algebraic inequality. Noncanonical simplification alone does not create false-positive identities; each symbolic check needs assumptions about its domain and transformations. Random substitution can expose a counterexample but cannot prove a universal identity.
- The exact one-point LQ relation `αD+βD²=ln(10)` describes a noiseless fixed-D ridge. An uncertain dose and likelihood give a band affected by priors. A ±98 Gy quantity is not automatically a 95% interval; its published uncertainty convention needs verification.
- A ridge does not require NUTS divergences. Divergences are numerical diagnostics that require investigation; reparameterization can improve sampling without adding identifying data. Do not preserve divergences as the success criterion. [Stan diagnostic guidance](https://mc-stan.org/learn-stan/diagnostics-warnings.html), [problematic-posterior guidance](https://mc-stan.org/docs/stan-users-guide/problematic-posteriors.html).
- The subtractive quadratic inversion for D10 loses precision as β approaches zero. For nonnegative α and β, use the algebraically equivalent `2ln(10)/(α+sqrt(α²+4βln(10)))` in a future implementation, with refusal at α=β=0. No inversion code was installed here.

No performance gain, sampler compatibility or scientific identifiability is established by this scope. The present scientific framing remains **spatial protection under an assumed shielding rule**.

## Preservation and evidence limits

`bioenergy_toys.jl` remains ignored and byte-identical before/after this review, SHA256 `f2882c03f32a663997367d7896859347c550c834bff4e30b4c09110a3d52fcbf`. The previous phase's 37 passing Python tests, 42 independent Julia diagnostic checks and unfinished practice baseline of 35 passes/105 errors/140 total are prior recorded checks; they were not recast as results of these candidate implementations. This follow-up changes only local review records and diagnostic logs. No packages were installed and no engine physics, existing Downloads artifact, remote document or Biofilms file was changed.
