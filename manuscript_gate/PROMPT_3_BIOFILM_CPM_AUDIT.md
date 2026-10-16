# Prompt 3 — Biofilm CPM Audit

**Audit status:** PARTIAL; canonical manuscript/repository identity is blocked.  
**Work mode:** read-only inspection; no repository, code, test, manuscript, Git, or remote changes were made.  
**Master Work Order target manuscript:** “Does a Dose Gradient Move Biomass Parcels? A Seed Ensemble of a Multispecies Cellular-Potts Biofilm with an Executed One-Way OpenMC Interface.” This exact title was not located in accessible project files. The inspected `Biofilms` and `Biofilms-publish` checkouts are plausible but cannot be promoted to canonical without authoritative project linkage.

## 1. Authority and revision report

| Candidate | Canonical path / remote | Branch, commit, worktree | Manuscript evidence | Authority status |
|---|---|---|---|---|
| `Biofilms` | `/Users/aurascoper/Developer/Biofilms`; `https://github.com/ffinkdevs/Biofilms.git` | `private/geolocator-runtime`; `74f433933f594ce749fd700b10b1041776f1a0e9`; dirty: 5 modified tracked paths plus 4 untracked paths at inspection. | Contains biofilm CPM, coupling, calibration materials and manuscript artifacts. | Candidate; not established as Master Work Order target. |
| `Biofilms-publish` | `/Users/aurascoper/Developer/Biofilms-publish`; same remote URL | `publish/agri-overlay`; `c65434cc038c58cd7708af4e1908715daf17f269`; clean at inspection. | README names `preprint/modeling_radioresistance_and_radiotropic_fitness.tex` as source-of-record manuscript; SHA-256 `13349b4efa580e970242c3761fe6b393a17721a182773661976d68d587815b9b`. README describes draft as not submitted. | Strong candidate manuscript snapshot, but title does not match Master target. Not confirmed authoritative for this audit. |
| `rna_biofilm_toy` / `rna_biofilm_toy-energy-v2` | Same remote `https://github.com/aurascoper/rna_biofilm_toy.git`; both HEAD `b780a1a7f6113f3b8454cad5efbc7dd66b76a25a`. | Main toy branch `guards/kit-v1`, dirty; energy-v2 detached HEAD with untracked specs/output paths. | README describes a standalone 2D lattice sandbox; no RNA/chemistry; protocell CPM status “spec only, no code.” | Excluded as biofilm CPM manuscript candidate. It is not the seven-species 3D Biofilms CPM. |

No fetch or remote query was performed. Commit identities and status are local snapshots, not claims about current remote heads. Because the target title and authoritative linkage are missing, code-level findings below are explicitly tied to inspected candidate files, not asserted as findings about the Master-named manuscript.

## 2. Candidate implementation and execution-state audit

`Biofilms-publish/README.md` describes a 3D Cellular Potts model, radiodialysis transport, OpenMC coupling, calibration gates and an unsubmitted manuscript. It explicitly says the framework is uncalibrated; no lattice pitch, seconds/MCS, or material density is selected; no outputs are compared with target-system measurements; outputs remain dimensionless; and the model has no birth/death behavior. This is source documentation, not proof that every listed component ran in the inspected revision.

The historical `Biofilms-publish/docs/audit_biofilms_potts.md` records candidate-specific defects and a past branch’s fixes. Its line-numbered source references point to earlier revisions, so they are leads, not current-line citations. Its audit states that pairwise energy is computed only as a reporting statistic, not used in `compute_delta_H`; no division/growth exists; nutrient is not read by a biological response; radiation is static and dimensionless; the radial figure labels contradict the implementation; and physical-unit conversions are absent. It also describes a retained stop condition on dose-responsive membrane coupling. These claims require rechecking against the authoritative revision once identified.

| Component | Evidence in inspected tree | Status / limitation |
|---|---|---|
| CPM dynamics | README and `biofilms_potts.jl`; framework described as executable 3D CPM. | Candidate code exists. No fresh execution performed in this audit; no run record was used to claim a new execution. |
| Radiodialysis | README identifies R transport and a second implementation coupled inside CPM. | Described as implemented; no independent PDE verification or empirical calibration claimed here. |
| OpenMC transport/coupling | README identifies `coupling/`; prior audit describes one-way geometry-to-dose attribution. | Candidate capability; executed state for exact Master-named study is unknown because repository identity is unresolved. |
| Growth, division, survival | Candidate README explicitly says not represented; audit says no division/growth. | Not implemented in candidate snapshot; no biological growth inference allowed. |
| Calibration | README says parameters are literature priors, no physical scale selected, no target comparison. | No empirical calibration/validation demonstrated. |
| Manuscript | `Biofilms-publish` README names a different title and says not submitted. | Exact Master target version missing; manuscript claims cannot be adjudicated authoritatively. |

## 3. Reusable-method matrix

| Method / claim ID | Original implementation and source locator | Target use | Classification | Required changes and validation |
|---|---|---|---|---|
| **CPM-001** Provenance and refusal-by-default | `Biofilms-publish/README.md`, “What this repository cannot currently claim”; `docs/calibration/` contracts. | Track measured chemical identity, units, material basis and missing values. | Mathematically reusable. | Preserve typed provenance and fail-closed missingness; verify against the target’s own evidence and version. |
| **CPM-002** Geometry-to-transport interface | Candidate `coupling/` and OpenMC README description. | Export spatial compartments/material regions to a transport solver. | Transferable with adaptation. | Replace tumor/biofilm labels with geochemical materials; define coordinates, mesh pitch, density, elemental composition, boundary conditions; verify energy conservation and mapping. |
| **CPM-003** Deterministic replay / seed ensembles | Candidate run/test infrastructure, exact run record not identified for target manuscript. | Sensitivity/ensemble analysis. | Transferable with adaptation. | Record input hashes, model/code revision, random seeds, solver settings and output hashes; distinguish synthetic from empirical uncertainty. |
| **CPM-004** OpenMC dose attribution | Candidate `coupling/` path; README. | Map radiation to target material energy deposition. | Transferable with adaptation. | A distinct target material and chemistry source model is required; radiolytic yield and aqueous/mineral source terms must be independently specified and validated. Dose transport does not validate chemistry. |
| **CPM-005** Cell/parcel semantics | Candidate `docs/calibration/cpm_entity_semantics.md` and README. | Spatial chemical compartments. | Conceptual analogy only. | A biomass parcel is not a molecule, protocell, organism, or chemical compartment. Define state variables and transition laws from target evidence. |
| **CPM-006** CPM Hamiltonian and radiation-response coefficients | Candidate `biofilms_potts.jl`, README and candidate audit. | Prebiotic chemical dynamics. | Not transferable. | Organism-specific adhesion, melanin, growth, repair and survival laws have no direct chemical analogue; replace with independently justified chemistry and kinetics. |
| **CPM-007** CPM lattice pitch and MCS clock | README and calibration contract say unset. | Convert spatial/temporal model to physical units. | Unknown / blocked. | Supply target geometry and measured/justified clock conversion. No conversion can be inferred from lattice units. |
| **CPM-008** Energy/Metropolis acceptance | Candidate CPM README calls prior “energy gain” label a conflation with arbitrary Metropolis units. | Chemical free-energy accounting. | Not transferable. | Hamiltonian `ΔH` in model units is not joules or Gibbs energy; require thermodynamic activities and a validated reaction/free-energy coupling law. |

## 4. Non-transferable biological assumptions

| Assumption | Candidate state | Target-domain rule |
|---|---|---|
| Organism maintenance and radiation survival | Explicitly absent or unsupported in candidate framework; any tumor/biofilm survival law is organism-specific. | Do not reinterpret as chemical persistence or protocell maintenance. |
| Genome size, repair and dose response | Not a state variable in the inspected CPM description. | DNA damage/repair terms do not represent abiotic reaction networks. |
| Growth, division and inheritance | Candidate README says absent; no division or lineage. | A CPM copy event cannot stand for reaction autocatalysis, compartment division, or heredity. |
| Species-specific adhesion/melanin | Explicit biological materials/coefficients. | Replace only with measured surface energies, mineral affinities, or amphiphile properties, with new validation. |
| CPM cells/voxels | Computational biomass parcels; lattice pitch not calibrated. | No molecular concentration, pore size, or protocell dimensions can be inferred. |
| Tumor cell death/repopulation | Not applicable to abiotic systems. | Do not map tumor survival fraction or receptor expression to chemical transition probabilities. |

## 5. Cross-domain interfaces and evidence requirements

| Interface | Symbol / units required | Candidate status | Validation needed before target use |
|---|---|---|---|
| Radiation → chemistry | `D(x,t)` in Gy (J kg⁻¹) for named material; `G_i` in molecules/100 eV or mol/J; source rate in mol m⁻³ s⁻¹ or mol m⁻² s⁻¹. | No verified Oklo field; CPM source is dimensionless unless calibrated. | Target geometry, composition, transport, dose rate/history, material-specific yield and product/loss measurement. |
| Chemistry → transport | Concentration `c_i` mol m⁻³; diffusivity `D_i` m² s⁻¹; velocity m s⁻¹; reaction source/sink mol m⁻³ s⁻¹. | Not established as a target-domain interface. | Species, speciation, activity, phase and boundary condition; conservation tests and empirical transport parameters. |
| Reaction → free energy | Balanced stoichiometry `ν_i`; `ΔG = ΔG° + RT ln Q` J mol⁻¹ reaction. | No target reaction law/admissible activities supplied. | Temperature, pressure, standard state, activities and kinetics. Negative ΔG does not imply rate or coupling. |
| Compartment → function | Permeability m s⁻¹, area m², volume m³, flux mol m⁻² s⁻¹, persistence time s. | Unknown for an Oklo-informed compartment. | Direct evidence for formation, selective exchange, leakage, coupling, persistence and any growth/division. |

## 6. Manuscript clarification, recommendations and blockers

Required before any manuscript-specific acceptance: (1) identify the exact repository URL/path, branch/commit, manuscript title/version/hash, and execution receipts for the Master-named study; (2) provide the approved study protocol and source-to-claim mapping; (3) distinguish the “Modeling Radioresistance and Radiotropic Fitness” source-of-record manuscript from the Master-named dose-gradient/one-way-OpenMC manuscript; (4) identify which tests/runs and outputs correspond to each manuscript claim; (5) document physical units and calibration state; and (6) disclose failed tests, withdrawn claims and historical fixes in their actual revision context.

Prioritized recommendation: first resolve identity (P0); then audit exact claims against immutable revision/run records; then document units and transfer interfaces; only after that consider a target-domain architecture. Do not treat this candidate audit as manuscript approval.

### Source ledger

- **S-CPM-1:** `Biofilms-publish/README.md`, sections “What this is,” “Which radiation phenotype,” “What this repository cannot currently claim,” “Selected structure.” Candidate revision `c65434cc038c58cd7708af4e1908715daf17f269`; README describes uncalibrated status and names a different manuscript.
- **S-CPM-2:** `Biofilms-publish/docs/audit_biofilms_potts.md`, §§1–7. Historical candidate audit with line-specific references to prior code revision; revalidation required against target revision.
- **S-CPM-3:** `Biofilms-publish/preprint/modeling_radioresistance_and_radiotropic_fitness.tex`, SHA-256 `13349b4efa580e970242c3761fe6b393a17721a182773661976d68d587815b9b`; candidate text only, not proven to be Master manuscript.
- **S-CPM-4:** `Biofilms` local Git identity/status as in §1; dirty worktree. Read-only candidate, no source claim established as canonical.
- **S-CPM-5:** `rna_biofilm_toy-energy-v2/README.md` and `specs/13_energy_governed_v2_amendment.md`, local detached snapshot with untracked specs; separate design lane, simulation disabled.

### Ranked unresolved issues

| Rank | Issue | Consequence | Closure condition |
|---|---|---|---|
| P0 | Master-named manuscript and canonical CPM checkout not found/linked. | Cannot state which implementation or manuscript was audited. | Owner identifies exact remote, branch, commit, manuscript version and receipts. |
| P0 | Candidate worktrees are dirty/divergent and have different manuscript identity. | Results may not match source-of-record claims. | Provide authoritative clean revision or designate exact dirty snapshot and inventory. |
| P1 | Executed state of exact OpenMC-coupled manuscript study unknown. | Cannot assert execution or one-way coupling. | Matching run records and artifact hashes. |
| P1 | Physical calibration and biological model limits. | No physical scale or empirical validation. | Target-specific calibration and independent evidence. |
| P2 | Candidate historical audit line numbers refer to an earlier revision. | Misattribution risk. | Re-audit exact source at resolved commit. |

Cross-report links: [Prompt 1 audit](PROMPT_1_MASTER_EVIDENCE_NOVELTY_AUDIT.md), [PRRT audit](PROMPT_4_PRRT_SPATIAL_CPM_AUDIT.md), [Final Integration Report](FINAL_INTEGRATION_REPORT.md).
