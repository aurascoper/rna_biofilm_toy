Pre-registration for the first honest run of the fixed toy, in two stages. Not written yet. No run that is reported as a result may happen until the stage-2 floors and the prediction lines below are filled in and this file is committed, and the git log must show that commit before any arm output.

What is fixed: engine.py as committed, 50 by 50 cylinder (x periodic, y bounded), field (y/HEIGHT) times 2.5 before scaling, 100 steps per run, seeds 1 through 10.

Arms, all on the same seeds. Field ladder at decay 1: field_scale 0 (the null: every slot weight is exactly 1 and deaths are exactly 0, so this arm is random placement with no damage), 0.25, 1, 4. Attribution arm: field_scale 1, decay_scale 0 (gradient present at its normal strength, damage off). Filenames out/fixed_s{seed}_f{field}_d{decay}.csv.

Observables, by column of the 15-column CSV.

First, clustering_index read against population_count, as a curve over the run, compared between arms at shared populations. Never at step 100 alone: at fixed shape the index falls like 2499/N (an interior strip of height h has mean occupied degree 8 minus 6/h while the random expectation grows with N; 12.6, 7.3, 4.6, 2.4 for h = 3, 6, 10, 20), and radiation lowers N, so an unmatched comparison manufactures the predicted sign. The raw mean_occupied_degree is in the file for re-derivation. The matched comparison is implemented either by interpolating each arm's curve at the populations the arms share, or by the covariate model in specs/04_turing_arm_inference.md.

Second, mean_y at step 100 and as a trajectory. The field ladder moves it through two mechanisms at once (deaths concentrated at high y; births biased toward +y by 5 percent per birth at scale 1 and 22 percent at scale 4), so the attribution arm's shift from the null is the birth-bias contribution and is subtracted from each ladder arm's shift before any claim is made.

What is not an observable, and why. The genotype means mean_purine_ratio and mean_radiotropism: selection on purine is strong (d(ln survival time)/du = k S, a 16 percent gain per +0.05 mutation with eight neighbours) but the mutation supply is three or four events per run, so the columns cannot move and a prediction on them would fail for the wrong reason. Deaths and population against the null: zero by construction at field 0.

Stage 1, the pilot, null arm only: run field 0 / decay 0 on seeds 1 through 10, record the seed-to-seed standard deviation of mean_y at step 100 and of clustering_index at matched population (the development measurement after 30 steps gave sd 0.112 rows and 0.19 index units; the stage-1 values at 100 steps replace these), and commit this file with those numbers filled in:

  sd(mean_y, null, 100 steps) =
  sd(clustering_index at matched N, null) =

Stage 2, the floors and the predictions, committed before the ladder and attribution arms run. Floors are two times the stage-1 standard deviations:

  floor(mean_y) =
  floor(clustering_index) =

Prediction for clustering_index (direction and rough size of each arm's difference from the null at matched population, and the ordering across 0.25, 1, 4):

Prediction for mean_y (direction and rough size after the attribution arm's shift is subtracted, and the ordering across 0.25, 1, 4):

Reason each prediction could fail for the right reason (what in the mechanism would have to be false):

Author and date:

Measured fact about the birth bias, recorded 2026-10-07 before any stage runs, because it bounds what the attribution arm can show: at seed 1 over 100 steps, 178 births occur but only 50 of them have more than one empty slot (the colony is dense; most births have exactly one place to go), and at field 4 the per-choice probability shift is 2 to 5 percent, so the expected number of choices altered by the field in a whole run is about one; seed 1 produced zero, and its field 0, field 1 and field 4 runs at decay 0 are identical cell for cell (verified by tracing every birth's probabilities and choice: 43 births had different probabilities, none a different choice). So mean_y moves through deaths, not through the tropism bias, at this horizon; the attribution arm's shift is expected to be indistinguishable from the null, and a prediction that the ladder's mean_y shifts come from births would fail for the right reason.

Notes. The fixed CSV's first row is step 0, the seeded configuration, so the initial index is on record. The verification runs in out/ (round 1: seeds 1 and 2, both engines; round 2.1: seed 1 at field 1 / decay 1) were executed during development to check the fixes and the RNG path and are not stage 1 or stage 2; README says so.
