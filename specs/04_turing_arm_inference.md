Turing.jl arm inference for the toy. Status: spec only, no code; no package was installed or run for this page, and API names are split into confident and verify. Gate: after stage 1 of PREDICTION.md (the null-arm pilot) and after the graded arms have run. Reads the fixed-engine CSVs in out/ and nothing else.

Its job is to close two defects of the arm comparison at once. First, the clustering index at fixed shape falls like 2499/N (see specs/05 and README), and radiation lowers N, so an unmatched comparison between arms manufactures the predicted sign; a regression with population as a covariate is a matched-N comparison by construction. Second, with ten seeds and an effect under one row there is no honest threshold to invent; a posterior for the magnitude of each contrast reports what the data say and narrows with more seeds rather than drifting toward a verdict, which is the point White 2014 makes about purchasable significance in simulation studies.

Model, for seed s and arm a, with index read at a declared step and N the population at that step:

    index[s, a] ~ Normal(mu[a] + gamma * (N[s, a] - Nbar) + u[s], sigma)
    u[s] ~ Normal(0, tau)

Report, for each arm against the null (field 0, decay 0): the posterior of mu[a] - mu[null], its 95 percent interval, and P(|mu[a] - mu[null]| > floor) where floor is the stage-2 value declared in PREDICTION.md. The same model is fitted to mean_y with the attribution arm (field 1, decay 0) as a second reference, since its shift is the birth-bias contribution that must be subtracted from the full arm.

Reporting requirements, none optional. The prior predictive is sampled and its interval recorded next to the posterior's before any posterior is reported; a prior predictive already concentrated on the observed values means the data did no work. Rhat and ESS for every parameter. The divergence count. The priors written out with one sentence each on why the bounds were chosen (sigma and tau non-negative; gamma unbounded; mu weakly informative on the measured scale of the index). A posterior that equals its prior is the honest outcome if it happens, and with ten seeds it may.

Where it lives: Julia reading Python CSVs does not belong in the repository root, which stays numpy plus pytest with no further dependency. Either analysis/ with its own Project.toml and Manifest.toml, or a sibling repository. The stage-2 floor in PREDICTION.md is declared without any of this.

Confident API names: the @model function block, the tilde sampling statement, sample, NUTS, the returned MCMCChains.Chains object. Verify before use, none of these were executed here: how to draw from the prior predictive (a Prior() sampler versus conditioning the observation on missing); the accessor names for Rhat, ESS and the divergence count on a Chains object, and whether divergences are in the chain internals rather than its summary; whether the arm contrast is read off the chain or needs cor and subtraction on extracted arrays; how a bounded prior is declared (truncated(Normal(...), 0, Inf) versus a distribution with built-in support).
