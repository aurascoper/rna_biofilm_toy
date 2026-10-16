# Prompt 4 — PRRT Spatial CPM Audit

**Audit status:** PARTIAL; repository identity is locally established, but the requested prebiotic/Oklo interpretation is not supported. The protocol retains stale base text beside amendments; its stored verdict aligns with the latest amendments.  
**Inspected checkout:** `/Users/aurascoper/Developer/PRRT-spatial-CPM`; remote `git@github.com:aurascoper/PRRT-spatial-CPM.git`; branch `guards/kit-v1`; HEAD `81ff9af3efb690160a7aa3dfd30d85378b9163aa`; worktree has one modified tracked `.DS_Store`. No remote query/fetch.  
**Manuscript:** `preprint/closing_the_loop_prRT_spatial_cpm.tex`, SHA-256 `58c6708f7ce7ee6c6fd95b835ac1d3fd7fe0a0c187a96694081181bd17c07848`. Same title/versioned manuscript PDF exists. Manuscript describes a tumor-directed peptide receptor radionuclide therapy (PRRT) framework, not an Oklo prebiotic model.

## 1. Execution-state audit

| Study / claim ID | Local record | Stored result | Scope and status |
|---|---|---|---|
| **PRRT-001** Transport and cached dose-point kernel | `study1/PROTOCOL.md` v1.5–v1.6 and `study1/verdict.json`; runs in `study1/runs/`. | FAIL-DPK: at 40 µm pitch, 1 mm³ synthetic ROI, DPK-vs-reference cell residual p95 23.84% against predeclared 2%; 32M/128M reference ladder records and later h3-vs-h4 128M comparison are documented. | Executed synthetic transport comparison, not experimental validation. DPK cache is inadmissible at the stated boundary/endpoint/tolerance; protocol prescribes full MC re-transport. Earlier hand-built spectrum, truncated-kernel and source-position runs are explicitly invalidated in protocol v1.1–v1.4. |
| **PRRT-002** Open-loop response layer | `study2_response_layer/PROTOCOL.md`, `study2_run.py`, `verdict.json`. | Stored response-layer verdict; synthetic dose field, LQ survival function, declared α/β, time and dose scaling. | Executed numerical response layer on a synthetic geometry; not empirical tumor-response calibration. Full details and gate status are in the records; no new rerun performed. |
| **PRRT-003** Closed-loop selection | `study3_closed_loop/PROTOCOL.md`, `study3_run.py`, `verdict.json`, run logs/artifacts. | `verdict.json` says PASS-SELECTION, records `delta_ln_e_closed_mean=-0.48379`, `delta_ln_e_open_mean=-0.18862`, `delta_sel=+0.29517`. | Executed declared synthetic population loop. The protocol’s initial E1/E2 text is stale, but explicit v1.1/v1.2 amendments supersede it: v1.1 defines positive absolute-drift contrast; v1.2 removes rising survivor counts as a gate and keeps them diagnostic. The JSON keys (`E1a_closed_below_worst_open`, `E1b_contrast_positive`, `E2_sawtooth_capacity_refill`) are consistent with the amendments. Treat the stored PASS as the amended synthetic result, while retaining a versioning/documentation risk because the original criteria remain earlier in the same file. No rerun or independent code-level recomputation was performed. |
| **PRRT-004** Integrated Potts dynamics | `study3_closed_loop/PROTOCOL.md` §Purpose/Boundaries and study design. | Closed loop uses fixed-site bookkeeping, death/division/inheritance; full Potts Hamiltonian inactive. | No full geometry-evolving Potts loop was executed. Histology initialization is synthetic; measured histology input absent. Do not describe a fully histology-initialized closed-loop CPM as executed. |
| **PRRT-005** DPK cache failure | `study1/PROTOCOL.md` v1.5 and `final_analysis.py`; `verdict.json`. | Boundary shell explanation; dose-point kernel is infinite-medium convolution and misses escape; mean residual by depth and energy accounting are reported. | Actual tested condition is narrow: one 40 µm synthetic water/tissue-surrogate geometry, 1 mm³ ROI, Lu-177, fixed resolution, 128M reference. Do not generalize to all geometries or radionuclides without further evidence. |
| **PRRT-006** Study 2 planted-field divergence | `issues/0001-study2-pass-divergence-on-a-planted-field.md`. | A repinned lognormal dose field with σ=2, seed 3, viable-cell CV 7.08 and p95/mean 3.73 passes Study 2 gates. | Open issue: protocol thresholds do not bound departure from reference-field descriptors; verdict is not robust to out-of-domain planted inputs. Requires a predeclared input-domain bound from protocol owner; no threshold is set here. |

## 2. Failed/superseded approximations and contradictions

The Study 1 protocol preserves a valuable failure chain: (a) hand-built decay spectrum gave a mean-energy anchor mismatch (198 keV vs 133 keV) and was retired; (b) a kernel with inadequate support was refused; (c) shared RNG seeds made 32M and 128M “ladder” outputs strict subsets, not independent noise comparisons; (d) a source-coordinate algebra error placed sources in a positive octant and invalidated pre-amendment runs; (e) v1.5 inferred a noise figure, which v1.6 retired because the implemented measured-pair test had not passed. These are documented failures, not hidden by the later result.

The v1.5 transport result reports p95 DPK cell residual 23.84% vs the 2% criterion; this is a strong negative approximation result within the tested synthetic setup. It does not validate the reference transport against patient measurements. The protocol itself cites a 1.2–1.5% Geant4/EGSnrc agreement as an inherited literature floor and treats residuals below it as uninterpretable.

Study 3's versioned protocol retains superseded base text beside amendments; the latest amendments and JSON keys are directionally consistent, but the record should identify the effective criteria more clearly. Separately, Study 2 issue #0001 demonstrates that passing response criteria on a synthetic field does not establish robustness to arbitrary field shapes.

## 3. Reusable-method inventory and transferability

| Claim ID | Method | Original purpose/source | Classification for geochemical target | Target-domain requirements / prohibited assumptions |
|---|---|---|---|---|
| **PRRT-007** | Source-to-grid map, coordinate conventions, immutable input hashes, run sidecars. | Study 1 `PROTOCOL.md`, `geometry.py`, `ref_arm.cpp`; MeV/voxel, C-order. | Transferable with adaptation. | Specify physical coordinates, mesh cells and materials; verify mapping and integral conservation. CPM cell IDs are not chemical entities. |
| **PRRT-008** | Reference transport vs cached-kernel comparison with a tolerance and boundary controls. | Study 1, protocol §§criteria/controls and v1.5 verdict. | Mathematically reusable. | New radiation spectrum, material, geometry, source distribution and target dose endpoints; re-establish accuracy criteria for chemistry use. |
| **PRRT-009** | Layered transport → response → population architecture. | Manuscript §§3–4; Studies 1–3. | Conceptual architecture only / transferable with adaptation. | Replace Lu-177 transport, tumor response, SF, mitotic catastrophe, SSTR2 uptake, and receptor inheritance with distinct chemistry/thermodynamic/kinetic laws and target evidence. |
| **PRRT-010** | Dose-point kernel caching. | Study 1 FAIL-DPK at 23.84% p95. | Not transferable as validated approximation. | Full transport or separately validated boundary-aware correction required; cache failure is evidence against this specific shortcut. |
| **PRRT-011** | Cellular Potts state update / tumor-cell survival and proliferation. | Study 3 protocol explicitly says Hamiltonian inactive; response is LQ tumor survival and declared division rules. | Not transferable. | No tumor-cell SF, mitotic response, receptor uptake/inheritance, or growth law maps directly to a prebiotic chemical system. |
| **PRRT-012** | GPU / CPU architecture and deterministic outputs. | Repository contains Julia, Metal and CPU code paths. | Transferable with adaptation. | Numerical equivalence, conservation, boundary and reproducibility need target-specific tests. Software checks do not validate chemistry. |

## 4. Target-domain interface specification

| Module edge | Required symbols and units | Current status | Conditions for use |
|---|---|---|---|
| Radiation → named target energy | `D(x,t)` Gy = J kg⁻¹, target mass kg, deposited energy J; source spectrum and geometry. | PRRT work uses MeV/voxel then dose convention for tumor-like model; Oklo target dose unknown (`OKL-002`). | Do not convert dose field to chemistry without target material, mass and time basis. |
| Energy → chemical production | `G_i` molecules/100 eV or mol/J; source term `r_i` mol m⁻³ s⁻¹ / mol m⁻² s⁻¹. | Not implemented in PRRT; 2B.9 contains separate water-radiolysis scenario (`OKL-003/004`). | Need material-specific radiation chemistry and loss/competition evidence. |
| Chemistry → network state | Concentrations mol m⁻³; activities; stoichiometric matrix; rate laws mol m⁻³ s⁻¹. | No prebiotic chemistry module in PRRT. | Balanced reactions, kinetic data, phase/speciation, thermodynamic and conservation checks. |
| Network → compartment function | Permeability m s⁻¹; area m²; flux mol m⁻² s⁻¹; persistence s. | Absent. | Demonstrate compartment formation, exchange, coupling, persistence, growth/division or heredity separately. |

## 5. Manuscript clarification and red-team findings

The manuscript is a framework proposal. Its biological and clinical meaning is specific to PRRT and tumor response; it cannot support an Oklo or prebiotic claim by analogy. “Cell-resolved” in this project refers to declared computational cell/site conventions; Study 1 uses one voxel-scale site as a cell at a chosen pitch. The tumor biology and the model geometry are not generic spatial chemistry.

Clarify in any future manuscript revision: the exact scope of each study; the 2% criterion as a declared design tolerance rather than clinical standard; the single tested geometry/radionuclide boundary; the v1.1–v1.6 failures and changes; Study 2’s planted-field open issue; and Study 3’s stale base criteria beside superseding amendments. Do not call all loops fully integrated when Study 3 leaves Potts Hamiltonian inactive and uses fixed-site bookkeeping.

### Source ledger

- **S-PRRT-1:** `study1/PROTOCOL.md` v1.1–v1.6; failure history and predeclared criteria.
- **S-PRRT-2:** `study1/verdict.json`, `study1/final_analysis.py`, sidecars and run records; hashes: verdict `22a8bf810799366451b9b7b6424dbbe1459efdcdd03b3718a03f153dda1cc25a`.
- **S-PRRT-3:** `study2_response_layer/PROTOCOL.md`, `study2_run.py`, `verdict.json`; verdict hash `cafae743eb638d8cc2a7451ffe6a205e98d8693f4f4d32abe6ca9573b8a07a02`.
- **S-PRRT-4:** `study3_closed_loop/PROTOCOL.md`, `study3_run.py`, `verdict.json`; verdict hash `d47b57ae2ad32c85846eaaa960a71bdcbaa30130a257ff8f10faa10222231cc7`.
- **S-PRRT-5:** `issues/0001-study2-pass-divergence-on-a-planted-field.md`; open issue; no threshold selected.
- **S-PRRT-6:** `preprint/closing_the_loop_prRT_spatial_cpm.tex`, SHA-256 in header; source version on inspected branch/commit only.
- **S-PRRT-7:** Perrot et al. (2014), *Physics in Medicine & Biology* 59:2183, DOI 10.1088/0031-9155/59/9/2183, cited in Study 1 protocol for Geant4/EGSnrc comparison. Not independently re-audited in this bounded review.

### Ranked unresolved issues

| Rank | Issue | Consequence | Exact closure |
|---|---|---|---|
| P1 | Study 3 base criteria remain stale beside superseding amendments. | Readers can misread E1/E2; JSON is consistent with amendments but not every earlier paragraph. | Mark effective v1.1/v1.2 criteria explicitly in a future authorized documentation revision; preserve stored historical record. |
| P0 | Study 1 DPK fails declared 2% cell-level threshold in one synthetic case. | DPK shortcut cannot be claimed admissible generally. | Use full MC re-transport or separately qualify a boundary-aware method for each intended geometry/material. |
| P1 | Study 2 planted-field issue #0001. | Result is sensitive to field-domain choice. | Owner sets a protocol-based domain acceptance rule before future execution. |
| P1 | Study 3 full Potts dynamics/histology not executed. | “Fully integrated histology-initialized closed loop” would overstate execution. | Implement/validate those modules and provide measured inputs before making that claim. |
| P1 | PRRT tumor laws are out of domain. | No direct prebiotic biological inference. | Specify independent target-domain chemistry and validation. |
| P2 | Candidate records cite literature model-validation numbers. | Those numbers are not rechecked here. | Reopen primary methods and records if used in manuscript. |

Cross-report links: [Prompt 1 audit](PROMPT_1_MASTER_EVIDENCE_NOVELTY_AUDIT.md), [Biofilm CPM audit](PROMPT_3_BIOFILM_CPM_AUDIT.md), [Final Integration Report](FINAL_INTEGRATION_REPORT.md).
