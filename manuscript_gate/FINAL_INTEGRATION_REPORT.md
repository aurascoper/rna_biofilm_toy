# Final Integration Report — Manuscript Gate

**Report status:** BOUNDED INTEGRATION COMPLETE; closeout review accepted.  
**Recommended disposition:** **NO-GO YET** for the integrated Oklo–prebiotic–protocell manuscript.  
**Approval status:** The closeout reviewer endorses NO-GO YET; separate project-owner gate acceptance remains pending.  
**Authorization:** No manuscript drafting, repository changes, simulations, experiments, commits, pushes, or publication are authorized by these reports.

## 1. Input authority register

| Input | Identity / provenance | Status and limitation |
|---|---|---|
| Master Work Order | Supplied attachment `Pasted text.txt`, SHA-256 `b3bebab07808530c27696e28d03b17a2e6907207dfbd32303263962944dc7880`. | Governing scope; exact attached contents inspected. |
| Prior Prompt 1 assessment | Supplied assessment attachment SHA-256 `6467179564fccc95933f4db649ab6fc4b9d9d3b919629f13b9885cc89ae64d46`. | Historical NO-GO YET; not a recovered complete evidence audit. |
| Prior Prompt 1.5 assessment | Supplied attachment SHA-256 `94913187d830cb80844b4e88dba65217d52625009452d32bcd49ded9c0cec53f`. | Historical Track A NARROW AND GO / Track B NO-GO YET recommendation; not independently completed here. |
| Prompt 1 audit | [PROMPT_1_MASTER_EVIDENCE_NOVELTY_AUDIT.md](PROMPT_1_MASTER_EVIDENCE_NOVELTY_AUDIT.md). | Reconstructed, partial; major primary-literature screening remains incomplete. |
| Biofilm audit | [PROMPT_3_BIOFILM_CPM_AUDIT.md](PROMPT_3_BIOFILM_CPM_AUDIT.md). | Partial; canonical CPM repository and Master-named manuscript not identified. Two candidate Biofilms snapshots are dirty/divergent or have a different manuscript title. |
| PRRT audit | [PROMPT_4_PRRT_SPATIAL_CPM_AUDIT.md](PROMPT_4_PRRT_SPATIAL_CPM_AUDIT.md). | Partial integration audit; local repository identity/version established, with a versioned protocol-text hazard and open planted-field issue. |
| PRRT source revision | `PRRT-spatial-CPM`, branch `guards/kit-v1`, commit `81ff9af3efb690160a7aa3dfd30d85378b9163aa`; manuscript SHA-256 `58c6708f7ce7ee6c6fd95b835ac1d3fd7fe0a0c187a96694081181bd17c07848`. | Local state only; no remote query/fetch. |
| Biofilms candidates | `Biofilms` `74f433933f594ce749fd700b10b1041776f1a0e9` dirty; `Biofilms-publish` `c65434cc038c58cd7708af4e1908715daf17f269` clean, same remote URL. | Neither proved to match the exact Master-named manuscript. |
| Oklo local state | `rna_biofilm_toy-energy-v2` detached at `b780a1a7f6113f3b8454cad5efbc7dd66b76a25a`, with untracked design/evidence artifacts; separate `oklo_heartbeat` local records outside Git. | Design lane and model records do not establish source measurements or a calibrated Oklo model. |

## 2. Shared claim-to-source ledger

| Claim ID | Integrated claim | Evidence class/status | Source and quantitative basis | Limitation / falsification condition |
|---|---|---|---|---|
| **OKL-001** | Oklo reactor cycling is inferred from fission-gas isotope evidence. | SOURCE-REPORTED + author interpretation; partly verified. | Meshik et al. (2004), DOI 10.1103/PhysRevLett.93.182302; 30-min active/2.5-h dormant pattern in source abstract. | Does not specify aqueous target dose or chemical production flux. Full method review needed for quantitative use. |
| **OKL-002** | A target-specific Oklo absorbed dose/energy is not established by accessible local records. | UNKNOWN / BLOCKED. | Local evidence-level note (2026-10-14) leaves dose-rate null. | Need target material, geometry, spectrum, history and transport. |
| **OKL-003/004** | Lin water-radiolysis values and nominal H₂ calculation are not Oklo measurements. | SOURCE-REPORTED / CALCULATED. | Lin et al. values are separated from predictions; 0.020 kg × 952–3450 Gy at G=0.40 gives 0.789–2.861 µmol; conditional gas estimate 350–1,250 ppmv at 67 mL, 80°C and 1 bar. | No transfer, recovery, total uncertainty or target equivalence. The table-predicted values (18.6/60.2 µM) differ from both measurements and independent calculation. |
| **OKL-006/007/008** | Biological reaction energetics, known protocell work, and reactor-geyser concepts do not close a prebiotic pathway at Oklo or establish novelty. | INFERRED; novelty incomplete. | Prior assessment plus Master Work Order; candidate comparator papers in Prompt 1 ledger. | Full primary source screening and target-specific catalytic/kinetic/coupling evidence could refine a narrower claim; none currently supports historical occurrence. |
| **CPM-001/002** | Biofilm provenance/unit/geometry methods may be reusable, but implementation claims are blocked by repository/manuscript identity ambiguity. | PARTLY VERIFIED / BLOCKED. | Candidate Biofilms snapshots and README/audit; none match Master title. | Owner must identify authoritative checkout, manuscript revision and execution receipts. |
| **CPM-006/008** | Biological CPM Hamiltonian and arbitrary Metropolis units cannot be treated as chemical free energy or prebiotic laws. | INFERRED with source support. | `Biofilms-publish/README.md`, “Which radiation phenotype” and “What this repository cannot currently claim”; candidate audit. | Any proposed target use needs new target-domain equations and validation; no direct coefficient conversion exists. |
| **PRRT-001/005** | Cached DPK failed the declared 2% criterion in the tested synthetic 40-µm Lu-177 case. | SOURCE-REPORTED local run record; not empirical validation. | Study 1: cell residual p95 23.84%; noise/failed-run history in protocol v1.1–v1.6. | Applies to one synthetic setup; does not generalize to every transport domain. |
| **PRRT-003** | Closed-loop selection verdict is a stored PASS under the latest amendments, with stale earlier criteria retained in the protocol file. | PARTLY VERIFIED; versioning/documentation risk. | Stored JSON says PASS-SELECTION and `delta_sel=+0.29517`; v1.1 defines positive absolute-drift contrast and v1.2 makes survivor-count direction diagnostic rather than gated. JSON criterion keys align with amendments. | Future documentation should identify effective criteria clearly; no new execution or independent recomputation was authorized here. |
| **PRRT-004/011** | Full histology-initialized Potts dynamics were not executed in Study 3; tumor survival and SSTR2 laws do not transfer directly to chemistry. | SOURCE-REPORTED protocol boundary; transfer INFERRED prohibited. | Study 3 protocol says Hamiltonian inactive and uses fixed-site bookkeeping; synthetic geometry. | No claim of a fully integrated closed loop or prebiotic model is admissible. |
| **PRRT-006** | Study 2 has a planted-field pass-divergence issue. | SOURCE-REPORTED open issue. | `issues/0001...`: σ=2, seed 3, viable CV 7.08, p95/mean 3.73, passes after repinning. | Requires a predeclared protocol-domain bound before future verdict. |

## 3. Quantitative and dimensional report

The only reproduced dimensional calculation in this integration is the conditional Lin-based radiolytic inventory recorded as `OKL-004`; formula and units are in Prompt 1 §4. It converts absorbed energy in joules to moles by dividing molecules/100 eV by energy per 100 eV and Avogadro’s constant. Result: 0.789–2.861 µmol for the assumed 20 g water and 952–3450 Gy. This is a planning scenario, not a delivered resource.

The source-to-resource chain is incomplete: dose to named Oklo target (missing) → target energy (missing) → target-specific yield (missing) → product flux (missing) → losses/transport (missing) → reaction extent/kinetics (missing) → available free energy (activities/conditions missing) → coupled compartment function (mechanism and measurements missing). No unsupported ΔG, reaction extent, natural retention, or protocell-energy value is manufactured here.

For computational audits, PRRT Study 1 uses MeV/voxel records and a declared cell/site mapping. Its 23.84% cell p95 DPK residual exceeds the protocol threshold 2.0% by 21.84 percentage points (11.92 times threshold); this arithmetic compares a recorded result with its declared criterion, not a biological measurement. The Study 3 stored contrasts and effective amended criteria are reported without recomputing. Biofilm candidate outputs remain dimensionless/unscaled per README; no Gy, seconds, concentration, or physical cell-size conversion is admitted.

## 4. Module dependency graph and execution status

```text
[Oklo reactor history] --inferred--> [target dose/energy: BLOCKED]
          |                                      |
          v                                      v
[local synthetic reactor calculations]      [radiolytic source: analogue only]
                                                 |
                                                 v
[transport / reaction / loss: unspecified] --> [chemical resource: BLOCKED]
                                                 |
                                                 v
[compartment functions / coupling: unsupported] --> [historical origin claim: BLOCKED]

[Biofilm CPM candidate: identity blocked] --methods only--> [target chemistry: new model required]

[PRRT Study 1: executed synthetic transport, DPK FAIL] --> [Study 2: executed synthetic response]
                 --> [Study 3: stored PASS under latest amendments; stale base text]
                 --> [full Potts/histology integrated loop: not executed]
```

Status labels: Study 1 transport and Study 2 response were executed in isolation on synthetic PRRT inputs; Study 3 has stored run artifacts and a PASS consistent with latest amendments, while earlier protocol text remains stale; full Potts dynamics, measured histology initialization, target-domain chemical source/reaction modules and Oklo-specific dose are specified, absent, or blocked. The v2 energy-governed ecosystem is design-only with simulation disabled. No simulation or experiment was run for this audit.

## 5. Cross-repository transferability matrix

| Source method | Original use / state | Potential target use | Unit change and required evidence | Prohibited transfer |
|---|---|---|---|---|
| CPM-001–004 provenance, hashes, spatial maps | Biofilm candidate; exact manuscript identity unresolved. | Track chemical-state provenance and spatial fields. | Map lattice sites to meters and physical species/concentrations; validate conservation, interfaces and replay. | Biological parcel IDs as protocells or molecules. |
| PRRT-007/008 transport, source-to-grid mapping, reference-vs-cache tests | Executed tumor radiophysics; one cache failure. | Architecture for spatial radiation-energy deposition and boundary tests. | MeV/voxel → J/kg requires voxel mass/material; chemistry source rate requires target yield and time. | Tumor dose/response is not radiolysis yield, chemical reaction, or prebiotic selection. |
| PRRT-009/011 staged response/population loop | Synthetic tumor response; Potts Hamiltonian inactive in Study 3. | Conceptual module separation only. | New equations, parameters, units, and empirical evidence for chemistry and compartments. | LQ survival, SSTR2 uptake, mitotic catastrophe, receptor inheritance as chemical laws. |
| Oklo evidence note / energy-governed v2 | Local design/evidence scoping; no simulation run. | Preserve evidence classes and null/blocked state. | Require authoritative source/dose, material chemistry and operational measurands. | Synthetic DSB counts, visualization fields, or analogues as physical measurements. |

## 6. Novelty challenge and permitted thesis

The broad historical thesis is unsupported by the available evidence and unresolved by this audit; missing evidence does not establish that the scenario is false. Ebisuzaki & Maruyama (2017) propose a natural-reactor-driven nuclear geyser as an origin-of-life setting, and Adam (2016) models reactor-associated temperature oscillations as potentially relevant to prebiotic oligomer synthesis (see Prompt 1 audit, claim OKL-007 and source S9). These papers challenge novelty based solely on joining reactor/geyser settings with prebiotic chemistry, but neither proves nor disproves that life originated at Oklo. Hydrothermal-vent and protocell literature also provides prior context for geochemical gradients, pores and compartments. A systems diagram joining these topics is not, by itself, a demonstrated new mechanism.

A narrow framework/synthesis could be considered later if it contributes a source-checked, unit-complete comparison and explicit tests that are not already in prior work. Current evidence does not establish that novelty increment. Biofilm CPM and PRRT repositories contribute methodological architecture only, not empirical validation of prebiotic chemistry.

**Permitted outline at this gate:** none authorized for drafting. A future conditional-feasibility framework could include (i) Oklo observations vs inferred history (`OKL-001/002`), (ii) analogue radiolysis values and conditional calculation (`OKL-003/004`), (iii) blocked source-to-reaction chain (`OKL-006`), and (iv) explicit computational-method limitations (`CPM-*`, `PRRT-*`). Exclude historical life/protocell claims, unverified dose/rate, unsupported ΔG/kinetics, and claims of an executed unified simulator.

## 7. Ranked blockers

| Rank | Blocker | Evidence and consequence | Owner input / closure condition | Gate |
|---|---|---|---|---|
| P0 | No recovered complete Prompt 1 audit and incomplete novelty search. | Historical assessment alone cannot establish evidence completeness or novelty. | Supply original audit or authorize/complete full source-led reconstruction and primary comparator screening. | Scientific scope and manuscript gate. |
| P0 | No Oklo target-specific absorbed dose/source flux. | Cannot quantify radiolytic production in a named target. | Primary dose/geometry/spectrum/target evidence with uncertainty. | Any Oklo-specific resource claim. |
| P0 | Biofilm CPM target identity unresolved. | Cannot attribute candidate implementation to Master-named study. | Exact repository, branch, commit, manuscript path/version/hash and run receipts. | Prompt 3 claims. |
| P1 | PRRT Study 3 protocol retains stale pre-amendment E1/E2 wording. | The latest amendments and stored JSON align, but the effective rule is easy to misread. | Clearly identify the effective amended criteria in any future authorized report; retain amendment history. | Cross-domain interpretation. |
| P0 | No complete source → reaction → compartment evidence chain. | Integrated thesis is unsupported. | Independently supported kinetics, transport/loss, target materials and coupling; no substitution from biological CPM/PRRT. | Manuscript disposition. |
| P1 | Study 2 accepts planted extreme field; domain bound missing. | Response-layer inference is input-domain sensitive. | Predeclare field admissibility based on protocol/reference descriptors. | PRRT robustness. |
| P1 | Full Potts and measured histology modules absent from PRRT closed-loop run. | “Fully integrated” claims overstate execution. | Matching executed implementation/records, or narrow claims to fixed-site synthetic loop. | PRRT manuscript accuracy. |
| P1 | Track A/Track B chemistry and novelty not independently resolved. | A biological reaction cannot stand in for an abiotic pathway. | Select one track, reaction and compartment endpoint; audit primary chemistry evidence. | Scope. |
| P2 | Local simulations/records not independently rerun. | Local reported numbers remain source-reported computational artifacts. | Independent reproduction only after authorization and exact environment/version selection. | Reproducibility. |

## 8. Prioritized work plan

1. **Source retrieval:** recover the original Prompt 1 audit and its exact primary-source set; screen nuclear-geyser, Oklo, radiolysis, abiotic chemistry and compartment comparators.
2. **Owner decisions:** resolve the biofilm repository/manuscript identity and clarify the effective PRRT Study 3 criteria; define whether Track A or Track B is in scope.
3. **Desk analysis:** complete source-level claim ledger, reaction classification, unit/stoichiometric checks and uncertainty/identifiability review.
4. **Quantitative specification:** only with admissible inputs, specify target-material dose, radiolytic source, transport/loss, rate and energy accounting. Keep unknowns blocked.
5. **Method development, simulations, and experiments:** these are separate future work orders requiring explicit scope and authorization. None is authorized by this gate report.
6. **Independent review:** review all four reports and any revisions; user explicitly accepts or rejects the final disposition before drafting.

## 9. Final manuscript-gate disposition

### **NO-GO YET**

The proposed integrated thesis depends on an unresolved Oklo dose/source chain, unverified reaction kinetics and transport, absent compartment coupling, incomplete novelty screening, ambiguous biofilm CPM authority, and a PRRT protocol-versioning hazard plus the Study 2 planted-field issue. The repositories provide methodological ideas and synthetic computational records; they do not establish an Oklo-to-prebiotic pathway. The earlier NO-GO YET disposition is independently consistent with these blockers, but was not used as a substitute for this assessment.

Reconsider only after the P0 conditions in §7 are closed or the thesis is narrowed to a separately supported contribution. The bounded remediation has passed closeout review, and the reviewer endorses this NO-GO YET recommendation. Separate project-owner acceptance of the manuscript gate remains pending. This review is not self-approval and does not authorize manuscript drafting.

## 10. Artifact and hash register

Hashes below are post-write SHA-256 values for the three audit inputs used by this report. The final report's own SHA-256 is necessarily reported in the delivery message because including an ordinary SHA-256 inside the same file changes that hash.

| Artifact | SHA-256 |
|---|---|
| `PROMPT_1_MASTER_EVIDENCE_NOVELTY_AUDIT.md` | `6d8b0eaab9ed7c3841b451e5fdfa53fbd901f96245b2a0ec16225e67b8fbd1d6` |
| `PROMPT_3_BIOFILM_CPM_AUDIT.md` | `57c9d5051ab4a089d2d78e5eb4aad97c7efec6202b2a17d13fe94e85e9b6eb40` |
| `PROMPT_4_PRRT_SPATIAL_CPM_AUDIT.md` | `a0a9072e758f24cccae418a945bcddea8faf65993fdd57b3585475c12e9f6e55` |
| `FINAL_INTEGRATION_REPORT.md` | Calculated after write; recorded in delivery message. |

Cross-report links: [Prompt 1 audit](PROMPT_1_MASTER_EVIDENCE_NOVELTY_AUDIT.md), [Biofilm CPM audit](PROMPT_3_BIOFILM_CPM_AUDIT.md), [PRRT spatial CPM audit](PROMPT_4_PRRT_SPATIAL_CPM_AUDIT.md).
