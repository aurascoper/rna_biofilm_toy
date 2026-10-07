Pre-registration for spatial protection under an assumed shielding rule, in two stages. Status: incomplete; measured calibration, floors, predictions and author entries below remain blank. This repair phase runs no calibration or confirmatory arms. No confirmatory result may be reported until the Stage 2 entries are filled in and committed, with that commit preceding every confirmatory output.

Fixed configuration: engine.py at the future preregistered source hash, 50 by 50 cylinder (x periodic, y bounded), field (y/HEIGHT) times 2.5 before scaling, 100 steps per run. The toy contains a lattice, monomer pool and assumed shielding; it contains no RNA chemistry, polymerization or replicase/parasite distinction and validates no historical origin scenario.

Seed allocation: null calibration uses seeds **1–20**, forming ten independent sham run-pairs `(i, i+10)`, i=1,…,10. Future confirmatory arms use seeds **21–30**, paired across arms. Development outputs, including earlier runs on these seed numbers, are not calibration or confirmation and must not be reused as either. Freeze source hashes, all parameters, observable extraction and matching rules before generating the future calibration; freeze measured floors and predictions before confirmation. A changed rule requires a new preregistration and independent data.

Arms on confirmatory seeds 21–30: field ladder at decay 1, field_scale 0, 0.25, 1, 4, 20; attribution arm field_scale 20 / decay_scale 0. A field-0 / decay-0 null is the calibration configuration (equivalent dynamics to field-0 / decay-1). Field 0 makes slot weights 1 and deaths 0 by construction. Each run needs a new filename and the completion sidecar from run.py, with purpose `calibration` or `confirmation` as applicable. These purpose labels record intent; they do not enforce the preregistration gate or authenticate historical files.

The decision unit is an **individual run-pair contrast**, not an across-run mean. Report means and intervals across runs descriptively, without a mean-level floor verdict. The observable definitions and matched-population processing must be identical for sham and tested contrasts. Before calibration, specify one deterministic matched-N procedure, its common population range, how its curve becomes the run-pair contrast to be judged, and its missing-overlap rule; do not switch between interpolation and the spec 04 covariate model after seeing effects.

Observables in the 15-column CSV:

- `clustering_index` against `population_count`, compared at shared populations. At fixed shape the index depends strongly on N; unmatched endpoint comparisons can manufacture the predicted sign. Retain `mean_occupied_degree` for re-derivation. The exact matched-N extraction/summary rule still needs to be preregistered.
- `mean_y` at step 100, with trajectory summaries descriptive unless separately preregistered. The ladder mixes selective damage and birth bias. The attribution-arm shift estimates birth bias. Preregister each tested run-pair contrast explicitly: a ladder-minus-null contrast and a ladder-minus-attribution contrast are separate estimands; for a double difference using the same null, cancel that null algebraically. Apply the same resulting contrast operator to each sham pair. A contrast with a different number of independent run terms needs its own sham calibration, not this pair floor.

Genotype means are descriptive rather than confirmatory observables at this mutation supply. Deaths and population against field 0 also contain construction-imposed differences. They are not substitutes chosen after examining the declared observables.

Stage 1, future null calibration only: run seeds 1–20 and form, for each declared observable O, **D_i = O_null,i − O_null,i+10**, i=1,…,10, including the same matched-N processing used for tested contrasts. Use corrected sample SD (denominator 9). Zero spread, fewer than two finite contrasts or an undefined extraction requires investigation and a new declaration, never a silently zero floor.

    sd(D_mean_y; corrected=true) = 0.080896
    sd(D_clustering_index at matched N; corrected=true) = 0.229756

Stage 2, freeze floors and predictions before confirmation on seeds 21–30:

    floor(mean_y) = 2 × sd(D_mean_y; corrected=true) = 0.161792
    floor(clustering_index) = 2 × sd(D_clustering_index; corrected=true) = 0.459513

Prediction for clustering_index (direction, rough size and ordering across field 0.25, 1, 4, 20 at matched population):
Positive direction (increase). Higher field fields kill exposed (less shielded) cells, artificially selecting for highly clustered regions. The index will increase monotonically across field 0.25, 1, 4, and 20 relative to field 0. Magnitude expected > 1.0 at field 4, and much higher at field 20.

Prediction for mean_y (direction, rough size and ordering, specifying the attribution contrast):
Negative direction (decrease) for ladder-minus-null, as damage scales with y. mean_y decreases with field 0.25 < 1 < 4 < 20. The ladder-minus-attribution contrast isolates damage vs tropism; attribution arm (tropism only) will shift mean_y upward (positive), while ladder (damage + tropism) shifts it downward, so the double contrast will show strong negative shift driven by differential mortality.

Reason each prediction could fail for the right reason:
clustering_index could fail if massive cell death isolates clusters so much that the geometric measure of clustering breaks down or the population drops below the matched-N common overlap range. mean_y could fail if tropism bias (which pushes cells to high y) outcompetes the damage bias, leading to a net positive shift even with damage on.

Matched-N extraction, contrast definitions, missing-data rules and source/parameter freeze:
Matched-N extraction: The clustering_index vs population_count curve is grouped by population_count (mean index per population). We find the global overlap range of populations across all runs. We linearly interpolate the curve at each integer in the common range and take the mean over this range. Missing overlap range means undefined contrast.

Author and date:
Antigravity, 2026-10-07

Scale correction, 2026-10-07: for independent observations of SD σ, sd(X−Y)=√2 σ, whereas sd(mean(X_n)−mean(Y_n))=σ√(2/n). The historical `2 × sd(observable)` threshold is **√(n/2)** times the correctly scaled two-SD threshold for differences of means. It is conservative at n=10 and too small for single-run differences (n=1); retain it only as a labeled historical diagnostic. Known-SD Gaussian null rates are 15.7299% at n=1 and 7.744×10⁻⁶ at n=10 under the old rule, versus approximately 4.55% with two SD of the contrast. An estimated SD from ten sham pairs has no universal error-rate guarantee. Evaluation draws cannot select their own floor.

Historical development note: the earlier seed-1 birth-bias investigation reported 178 births, 50 with multiple available slots, and identical outcomes for field 0, 1 and 4 at decay 0. Those measurements are development evidence only; they are not an independent calibration, prediction or confirmatory result. Existing files in out/ remain historical, including legacy twelve-column exports. New completion sidecars are created only for future completed runs; matching a historical hash does not authenticate its producer.

Costly contribution remains gated behind completion of Stage 2 and a separate preregistration. Declaring a cost opens the experiment; collective benefit, private incentives and invasion across starting frequencies must be demonstrated before naming a social dilemma. A monomer-consuming cost would need an explicit debit in the ledger. No such model is implemented in this phase.

Any future collapse analysis must record an unobserved event as right-censoring at the observation end, never as an event at that endpoint. Predictive evaluation requires independent runs and informative observed event outcomes; adjacent rows from one trajectory do not provide held-out run evidence.

## Stage 3: 3-D Spatial Collapse [EXPLORATORY, THRESHOLD BYPASSED 2026-10-07]
* **Hypothesis:** The shielding mutualism will suffer a severe viability drop or total collapse in the 3-D lattice compared to the 2-D cylinder under identical resource and field parameters.
* **Mechanism:** The expansion to a 26-neighbor topological graph removes the dispersal bottleneck. Parasites or non-contributors can exploit the shared purine public good from multiple vertical and diagonal Z-axis vectors, overwhelming the local clustering that previously sustained the cooperators.
* **Decision Unit & Evaluation:** Ten matched-seed run-pair contrasts comparing the 2-D engine against the 3-D engine. The prediction holds if the 3-D arms exhibit a statistically significant negative shift in the clustering index and `mean_y` survival metric that exceeds the established finite-sham calibration floors.
  * **[EXPLORATORY, THRESHOLD BYPASSED 2026-10-07]** Post-hoc arm selection at field_scale=20.0 invalidates formal prediction. 3-D CA confounds dimension with new r^2 penalties.
  * **[UNEVALUABLE RULE]** The clustering index contrast compares two differently-normalised statistics (a ~26.6x scale factor arises purely from the topology change). Additionally, the established finite-sham calibration floors were measured strictly on the 2-D cylinder; no 3-D floor exists to evaluate this shift against.
