Turing.jl arm inference for the toy. Status: specification only; no package installed, inference run or predictive model trained in this repair. Gate: future calibration and Stage 2 preregistration in PREDICTION.md must be complete before confirmatory arms (seeds 21–30) and any analysis of them. Null calibration is seeds 1–20 paired `(i,i+10)`. Existing development CSVs cannot be reused as calibration or confirmation.

Its proposed job is to describe arm contrasts while accounting for population. Clustering at fixed shape depends strongly on N, so an unmatched arm comparison can manufacture the sign. A population-covariate model is a candidate adjustment, not automatically a valid matched-N comparison: common support, model adequacy and the resulting observable extraction must be declared before calibration, and applied identically to sham and tested contrasts. Interpolation is another candidate; the preregistration must choose before data are generated.

Candidate model, for seed s and arm a at a declared step:

    index[s,a] ~ Normal(mu[a] + gamma * (N[s,a] - N_ref) + seed_effect[s], sigma)
    seed_effect[s] ~ Normal(0, tau)

Priors and scales require written justification, prior/posterior predictive checks and diagnostics (Rhat, ESS, divergences). No API invocation or successful sampling is claimed here. Julia inference, if later authorized, belongs in analysis/ with its own Project.toml and Manifest.toml; the root remains numpy plus pytest.

The decision unit is the individual run-pair contrast. Posterior arm means, mean differences and intervals are descriptive; do **not** apply the run-pair floor to `mu[arm]-mu[null]` or issue a mean-level detection verdict. If a future analysis reports an exceedance probability, its draws must represent the declared individual run-pair contrast, including residual variation and pairing, rather than just uncertainty in its mean. It would require a separately declared loss before any decision.

Calibration is `2 × std(D; corrected=true)` for ten null sham run-pair contrasts with the same observable/matching operator as tested pairs. Independent observations have sd(X−Y)=√2 σ; differences of n-observation means have SD σ√(2/n). The old `2σ` floor differs from the correct two-SD mean-contrast threshold by √(n/2). It survives only as a historical diagnostic. Finite sham calibration gives no universal false-detection guarantee. Means across the ten confirmatory seeds are descriptive, never a way to change the decision unit after seeing effects.

Collapse analysis is a separate future question. An event not observed during a run is right-censored at its last observation; a countdown to that endpoint is not time to an observed collapse. Evaluation must split independent runs and include informative event outcomes. No neighboring-row train/test split or ML training belongs to this phase.
