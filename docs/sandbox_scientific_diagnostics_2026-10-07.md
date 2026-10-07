# Isolated sandbox and scientific diagnostics — implementation record, 2026-10-07

The approved local implementation is complete. All six sandbox sections pass with the original assertions preserved. Independent Symbolics, synthetic Turing, and Metal field checks passed in the new Biofilms worktree. These results assess **spatial protection under an assumed shielding rule** and numerical/synthetic diagnostics; they do not validate RNA-world chemistry or a historical origin scenario.

## Sandbox

[Completed sandbox](../bioenergy_toys_sandbox.jl) uses only Test, LinearAlgebra, Random, and Statistics in its own [Project](../analysis/sandbox/Project.toml) and pinned Manifest, Julia **1.13.1**, startup disabled, `JULIA_LOAD_PATH=@:@stdlib`. The environment inventory verified the four declared dependencies and refusal of Turing/Metal imports. Statistics 1.11.5 is the resolved upgradable stdlib.

**238 original assertions and 52 added controls passed.** The original runner/assertion region is copied verbatim and checked by [delivery verification](scientific_diagnostics_2026-10-07.json). All 36 exercise stubs have independent implementations in [sandbox_implementations.jl](../analysis/sandbox_implementations.jl).

Named controls cover eager missing-variable refusal, malformed/out-of-domain relations, four-entry cylindrical routine agreement, separate raw symmetry/column-sum/row-sum checks, pre-wrapper asymmetric-matrix refusal, finite real square input, zero operator, small positive spectrum, bounded Euler advancement, finite numeric floors, and independent calibration/evaluation streams. The zero operator returns Inf as a mathematical bound while the Euler driver advances through finite steps to the requested duration with unchanged state. Spectral positivity uses an operator-scaled eigensolver roundoff allowance; small positive operators cannot hide behind an absolute tolerance.

`has_private_disincentive`, `floor_from_sham`, and numeric-floor `false_detection_rate(...; contrast_sample_size)` are retained. `posthoc_floor` stays a labeled invalid demonstration with negative-floor refusal. The original probability-query assertion explicitly permits +Inf as a limit; this exception does not extend to decision/calibration floors. The cylindrical stability result belongs to the unguarded reference, distinct from the toy engine's downhill-only update.

Original `bioenergy_toys.jl` is byte-for-byte preserved, still ignored, SHA-256 **f2882c03f32a663997367d7896859347c550c834bff4e30b4c09110a3d52fcbf**. Re-execution preserves its historical result: **35 passes, 105 errors, 140 executed, `:incomplete`**. Completing the sandbox exercises more assertions because the original stub errors had interrupted those test paths. The earlier 42 independent numerical checks still pass, and the existing Python suite reports **37 passed**.

## Gaussian reference correction

[Numeric receipt](gaussian_diagnostics_2026-10-07.json) records analytical values plus an independent 300,000-draw estimated-SD diagnostic (observed 7.61267%). The decision unit remains an individual run-pair contrast. Across-run averages are descriptive.

| Threshold / case | False-detection probability |
|---|---:|
| Two known contrast SDs | 4.55003% |
| Two estimated SDs from ten independent Gaussian shams | 7.65528% |
| Historical 2 sigma, single-observation contrast | 15.72992% |
| Historical 2 sigma, difference of ten-observation means | 0.00077442% |

For independent observations with SD sigma, sd(X-Y)=sqrt(2)*sigma and sd(mean(X_n)-mean(Y_n))=sigma*sqrt(2/n). The old 2*sigma threshold is sqrt(n/2) times the correctly scaled two-SD threshold for differences of means. The t9 result applies to an **independent future Gaussian contrast divided by the corrected SD of ten independent shams, with known zero null mean**. Estimating and subtracting the sham mean changes the scaling. Finite sham calibration provides no universal error rate for actual observables. No new toy calibration or confirmation was performed.

## Biofilms diagnostics

Worktree: `/Users/aurascoper/Developer/Biofilms-symbolics-turing-mac`, branch `research/symbolics-turing-diagnostics`, base `5be2661b4625a5a33af00e0a6c101d7112e67ddd`. Final inference freeze: **d02040ffcddf077867a506d90e2fe62a9e7d026c**. [Full results and named controls](/Users/aurascoper/Developer/Biofilms-symbolics-turing-mac/diagnostics/RESULTS.md) identify final receipts, preserved failures, source hashes, seeds, exact versions, and commands.

Symbolics **7.44.1** passed **192 checks**, including AST sign and additive-constant mutants before Julia lowering, serial volume/adhesion/stencil/Monod agreement, dt-dependent consumption positivity, and AST budgets before/after simplification. Turing **0.49.0** passed **136 preflight checks** and **8 acceptance-detector checks**, then all seven frozen CPU Float64 fits. Metal **1.11.0** passed **57 checks** on Apple M4, using explicit Float32 device arrays against CPU Float64 references. Existing narrow Biofilms serial regression passed 20,019 checks; claims-ledger tests passed 41.

Every fit used four chains with 1,000 warmup and 2,000 retained draws each, target acceptance 0.9, max_depth=12. All had zero retained divergences and depth-limit hits. Maximum R-hat was 1.003652; minimum bulk/tail ESS exceeded 1,362; maximum marginal CDF error was 0.01543 against refinement-checked independent references. The one-observation shape posterior remains prior-dependent despite healthy mixing. All 56,000 retained rows and hashes passed independent readback.

Metal synchronized median stencil times were **0.31425 ms at N=40** and **0.82885 ms at N=80**, after three warmups and twenty timed repetitions. Separate preparation/readback medians and individual outliers are retained. Both domains passed exact constant-field preservation and normalized mass residual below 1e-6. These wall times include dispatch/synchronization overhead, and no speedup gate was imposed. Hardware: Apple M4, aarch64, 16 GiB, macOS 27.0.1 build 26A434.

## Preservation, limitations, and commands

The [input hash manifest](preserved_inputs_2026-10-07.json) and delivery receipt verify nine prior inputs plus the already-corrected workbook remain unchanged. Existing worktrees, engine physics, CPM scheduling, manuscript files, and toy reserved seeds 1–30 were preserved. Review/spec corrections are visibly dated; historical outputs remain historical. Release/manuscript gates remain in effect. Hosted CI and full Biofilms regression suites were not run; the new CPU CI workflow is configured only. GPU AD compatibility, GPU NUTS, Enzyme, LoopVectorization, and C/Rust compilation remain outside scope.

From `rna_biofilm_toy`:

```sh
JULIA_LOAD_PATH=@:@stdlib julia --startup-file=no --project=analysis/sandbox -e 'using Pkg; Pkg.instantiate()'
JULIA_LOAD_PATH=@:@stdlib julia --startup-file=no --project=analysis/sandbox analysis/sandbox/verify_environment.jl
JULIA_LOAD_PATH=@:@stdlib julia --startup-file=no --project=analysis/sandbox bioenergy_toys_sandbox.jl
python3 -m venv analysis/python_checks/.venv
analysis/python_checks/.venv/bin/python -m pip install -r analysis/python_checks/requirements.txt
analysis/python_checks/.venv/bin/python -m pytest -q
analysis/python_checks/.venv/bin/python analysis/gaussian_diagnostics.py NEW_GAUSSIAN_RECEIPT.json
python3 analysis/verify_scientific_delivery.py --worktree /Users/aurascoper/Developer/Biofilms-symbolics-turing-mac --output NEW_DELIVERY_RECEIPT.json
```

Use fresh receipt destinations. Reproduce the other lanes using the isolated worktree's [README](/Users/aurascoper/Developer/Biofilms-symbolics-turing-mac/diagnostics/README.md). Logs for this sandbox/environment/Python verification are retained under `logs/`; earlier failed environment inventory and development outputs are not presented as passes.
