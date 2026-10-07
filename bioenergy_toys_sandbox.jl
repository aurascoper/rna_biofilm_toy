# Completed isolated counterpart of the preserved practice script.
# Run: JULIA_LOAD_PATH=@:@stdlib julia --startup-file=no --project=analysis/sandbox bioenergy_toys_sandbox.jl
module BioenergyToysSandbox
VERSION == v"1.13.1" || error("sandbox requires Julia 1.13.1")
Base.active_project() == joinpath(@__DIR__, "analysis", "sandbox", "Project.toml") || error("wrong sandbox project")
get(ENV, "JULIA_LOAD_PATH", "") == "@:@stdlib" || error("sandbox LOAD_PATH must exclude shared environments")
# ═══════════════════════════════════════════════════════════════════════════════
#  GIVEN SCAFFOLDING — shared by the reference and the practice file.
# ═══════════════════════════════════════════════════════════════════════════════
using Test, LinearAlgebra, Random, Statistics
include(joinpath(@__DIR__, "analysis", "operator_checks.jl"))
using .ArtifactOperatorChecks: checked_symmetric

# ── Section 1: a formula type and the four connectives ───────────────────────
abstract type Formula end
struct Var     <: Formula; name::Symbol end
struct Not     <: Formula; a::Formula end
struct And     <: Formula; a::Formula; b::Formula end
struct Or      <: Formula; a::Formula; b::Formula end
struct Implies <: Formula; a::Formula; b::Formula end
struct Iff     <: Formula; a::Formula; b::Formula end

¬(a::Formula)            = Not(a)
∧(a::Formula, b::Formula) = And(a, b)
∨(a::Formula, b::Formula) = Or(a, b)
→(a::Formula, b::Formula) = Implies(a, b)
↔(a::Formula, b::Formula) = Iff(a, b)
Base.show(io::IO, v::Var) = print(io, v.name)
Base.show(io::IO, f::Not) = print(io, "¬", f.a)
for (T, s) in ((And,"∧"), (Or,"∨"), (Implies,"→"), (Iff,"↔"))
    @eval Base.show(io::IO, f::$T) = print(io, "(", f.a, " ", $s, " ", f.b, ")")
end
const MAX_TRUTH_TABLE_VARS = 16   # declared refusal bound: 2^16 = 65536 rows

# ── Section 3: the two real routines, transcribed. These are GIVEN; the
#    exercise is to assemble each as a matrix and make it agree with these.
const NB6 = ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))

"biofilms_potts.jl laplacian_3d: 6-neighbour, out-of-lattice contributes 0 (Neumann)."
function lap6_direct(field::Array{Float64,3}, x, y, z, N)
    val = field[x, y, z]; L = 0.0
    for (dx, dy, dz) in NB6
        nx, ny, nz = x + dx, y + dy, z + dz
        if 1 <= nx <= N && 1 <= ny <= N && 1 <= nz <= N
            L += field[nx, ny, nz] - val
        end
    end
    L
end
"Apply lap6_direct at every site."
function lap6_apply(field::Array{Float64,3})
    N = size(field, 1); out = similar(field)
    for z in 1:N, y in 1:N, x in 1:N; out[x,y,z] = lap6_direct(field, x, y, z, N); end
    out
end

"Moore neighbours on a cylinder: x periodic, y bounded. 5 on rows 1 and H, 8 inside."
nbrs_cyl(x, y, W, H) = [(mod(x - 1 + dx, W) + 1, y + dy) for dx in -1:1, dy in -1:1
                        if !(dx == 0 && dy == 0) && 1 <= y + dy <= H]
deg_cyl(W, H) = [length(nbrs_cyl(x, y, W, H)) for x in 1:W, y in 1:H]

"""
UNGUARDED reference: removing `if c_i > c_j` makes every ordered link fire.
This is a different operator, not a linearisation of the engine's downhill-only
update. Returns the per-step delta, divided by the GIVER's degree.
"""
function diff_cyl_direct(c::Matrix{Float64}, D::Float64)
    W, H = size(c); fd = zeros(W, H); deg = deg_cyl(W, H)
    for y in 1:H, x in 1:W, (nx, ny) in nbrs_cyl(x, y, W, H)
        f = D * (c[x, y] - c[nx, ny]) / deg[x, y]
        fd[nx, ny] += f; fd[x, y] -= f
    end
    fd
end

# Two DEFECTIVE assemblies, given so section 3 can ask which test catches which.
function assemble_diff_cyl_const8(W, H, D)           # forgets that edge rows have 5
    idx(x, y) = x + (y - 1) * W; M = zeros(W * H, W * H)
    for y in 1:H, x in 1:W, (nx, ny) in nbrs_cyl(x, y, W, H)
        i, j, q = idx(x, y), idx(nx, ny), D / 8
        M[j,i] += q; M[j,j] -= q; M[i,i] -= q; M[i,j] += q
    end
    M
end
function assemble_diff_cyl_mismatch(W, H, D)         # takes with the receiver's degree
    idx(x, y) = x + (y - 1) * W; d = deg_cyl(W, H); M = zeros(W * H, W * H)
    for y in 1:H, x in 1:W, (nx, ny) in nbrs_cyl(x, y, W, H)
        i, j = idx(x, y), idx(nx, ny)
        give, take = D / d[x, y], D / d[nx, ny]
        M[j,i] += give; M[j,j] -= give; M[i,i] -= take; M[i,j] += take
    end
    M
end

# Three variables, pre-made, so you can poke at formulas in the REPL.
const p, q, r = Var(:p), Var(:q), Var(:r)

# ── Section 5: the toy's shielding law, transcribed from engine.py. GIVEN. ────
const K_SHIELD = 0.25                                   # engine.py: kappa = purine_ratio * 0.25
"Attenuation factor on local flux: own purine u, neighbours' purine sum S (engine.py)."
shield(u, S) = exp(-K_SHIELD * u * S)
"ln of the survival time of an organism that never replicates: t = exp(kuS)/(flux*decay)."
log_survival_time(u, S, flux, decay) = K_SHIELD * u * S - log(flux * decay)
const PURINE_MIN, PURINE_MAX, PURINE_STEP = 0.1, 9.0, 0.05   # engine.py clamps and mutation step

# ── Section 6: the pre-registration rule, transcribed from PREDICTION.md. GIVEN. ─
const FLOOR_MULTIPLE = 2.0                              # stage 2: 2 x corrected SD of sham contrasts
# Synthetic observable fixture ONLY, not a measured pilot; and a planted effect
# sample with the same spread and a mean shifted by 3 sd. Written in, not drawn, so
# every expected value below is arithmetic on numbers you can see.
const NULL_SAMPLE   = [24.91, 25.07, 24.98, 25.12, 24.87, 25.03, 24.95, 25.09, 24.99, 25.01]
const NULL_SD       = std(NULL_SAMPLE)                  # corrected (n-1) by default; 6.0 pins this
const EFFECT_SAMPLE = NULL_SAMPLE .+ 3 * NULL_SD
# Synthetic run-pair contrast fixture, not calibration output.
const SHAM_CONTRASTS = [-0.12, 0.08, -0.03, 0.11, -0.15, 0.04, 0.07, -0.09, 0.02, 0.06]

# ═══════════════════════════════════════════════════════════════════════════════

include(joinpath(@__DIR__, "analysis", "sandbox_implementations.jl"))

const PRACTICE_STATUS = try
@testset "bioenergy_toys" begin
# ═══════════════════════════════════════════════════════════════════════════════
#  THE TESTS ARE THE SPEC. Lines marked CONTROL exist so a degenerate
#  implementation (one that returns a constant, or that never looks at its input)
#  fails rather than passes. If you weaken an exercise, its CONTROL must go red.
# ═══════════════════════════════════════════════════════════════════════════════

@testset "1 · symbolic logic" begin
    @testset "1.0 Julia's own precedence (no exercise — a fact to know)" begin
        # ∧ (12) binds tighter than ∨ (11); ¬ is unary and tighter than both.
        @test Meta.parse("a ∨ b ∧ c").args[1] === :∨
        @test Meta.parse("a ∧ b ∨ c").args[1] === :∨
        # → and ↔ SHARE precedence 4 and are right-associative. Convention puts ↔
        # loosest, so Julia disagrees here and you must parenthesise:
        @test Meta.parse("a → b ↔ c").args[1] === :→      # convention wants :↔
        @test Base.operator_precedence(:→) == Base.operator_precedence(:↔)
        # && is control flow, not a value you can pass around; & is a function.
        @test_throws Exception Meta.parse("(&&)")
        @test (&) isa Function
    end
    @testset "1.1 vars" begin
        @test vars(p) == [:p]
        @test vars((p ∧ q) ∨ ¬p) == [:p, :q]              # sorted and deduplicated
        @test vars(¬(r → (p ↔ q))) == [:p, :q, :r]
        @test vars(p ∧ p) == [:p]
    end
    @testset "1.2 evaluate — and its refusal" begin
        a = Dict(:p => true, :q => false)
        @test evaluate(p, a) == true
        @test evaluate(¬p, a) == false
        @test evaluate(p ∧ q, a) == false
        @test evaluate(p ∨ q, a) == true
        @test evaluate(p → q, a) == false
        @test evaluate(q → p, a) == true
        @test evaluate(p ↔ q, a) == false
        @test evaluate(q ↔ q, a) == true
        # REFUSAL: a missing variable is an error, never a silent `false`.
        @test_throws Exception evaluate(p ∧ r, a)
        # CONTROL: if evaluate ignored the assignment this would pass anyway, so
        # check it responds to a flipped input.
        @test evaluate(p, Dict(:p => false)) == false
    end
    @testset "1.3 truth_table — and its declared bound" begin
        t = truth_table(p ∧ q)
        @test length(t) == 4
        @test all(x -> x isa Pair, t)
        @test count(last, t) == 1                          # only (T,T)
        @test length(truth_table(p)) == 2
        @test length(truth_table((p ∧ q) ∨ r)) == 8
        big = foldl(∧, [Var(Symbol("v", i)) for i in 1:MAX_TRUTH_TABLE_VARS+1])
        @test_throws Exception truth_table(big)            # refuses, does not hang
    end
    @testset "1.4 tautology / contradiction / satisfiability" begin
        @test is_tautology(p ∨ ¬p)
        @test is_tautology(p → p)
        @test is_contradiction(p ∧ ¬p)
        @test is_satisfiable(p ∧ q)
        # CONTROLS: a contingency is none of the absolutes.
        @test !is_tautology(p)                             # catches `always true`
        @test !is_contradiction(p)                         # catches `always true`
        @test !is_tautology(p ∧ ¬p)
        @test !is_contradiction(p ∨ ¬p)
        @test !is_satisfiable(p ∧ ¬p)                      # catches `always true`
        @test is_satisfiable(p)
    end
    @testset "1.5 equivalence, and three laws" begin
        @test equivalent(¬(p ∧ q), ¬p ∨ ¬q)                # De Morgan
        @test equivalent(p ∧ (q ∨ r), (p ∧ q) ∨ (p ∧ r))   # distribution
        @test equivalent(p → q, ¬q → ¬p)                   # contraposition
        @test equivalent(p → q, ¬p ∨ q)                    # material implication
        # CONTROL: equivalent must be able to say no.
        @test !equivalent(p → q, q → p)
        @test !equivalent(p, ¬p)
    end
end

@testset "2 · set theory" begin
    @testset "2.0 isequal vs == (no exercise — the trap)" begin
        # Set and Dict key on isequal/hash; `in` on an array keys on ==.
        @test 0.0 == -0.0 && !isequal(0.0, -0.0)
        @test length(Set([0.0, -0.0])) == 2
        @test !(0.0 in Set([-0.0]))      # false
        @test   0.0 in [-0.0]            # true  — the exact opposite
        @test isequal(NaN, NaN) && !(NaN == NaN)
        @test length(Set([NaN, NaN])) == 1
        @test   NaN in Set([NaN])        # true
        @test !(NaN in [NaN])            # false — opposite again
    end
    @testset "2.1 deduplication under the two equalities" begin
        xs = [0.0, -0.0, 1.0, NaN, NaN, 1.0]
        a, b = dedup_isequal(xs), dedup_equals(xs)
        # Same count, different contents — the two equalities disagree in both
        # directions at once, and neither is "the" right answer.
        @test length(a) == 4 && length(b) == 4
        @test count(iszero, a) == 2        # isequal keeps 0.0 and -0.0 apart
        @test count(iszero, b) == 1        # ==  collapses them
        @test count(isnan, a) == 1         # isequal(NaN, NaN) is true: NaNs collapse
        @test count(isnan, b) == 2         # ==  never matches a NaN: NaNs accumulate
        # CONTROL: on a collection with neither trap the two agree.
        @test length(dedup_isequal([1,2,2,3])) == length(dedup_equals([1,2,2,3])) == 3
    end
    @testset "2.2 power set" begin
        P = powerset(Set([1,2,3]))
        @test length(P) == 8
        @test Set{Int}() in P                         # the empty set is a subset
        @test Set([1,2,3]) in P                       # so is the whole set
        @test length(unique(P)) == 8                  # all distinct
        @test all(s -> s ⊆ Set([1,2,3]), P)
        @test length(powerset(Set{Int}())) == 1       # P(∅) = {∅}
        for n in 1:5
            @test length(powerset(Set(1:n))) == 2^n
        end
    end
    @testset "2.3 relations — and the vacuous-transitivity trap" begin
        S = Set([1,2,3])
        eqr  = Set([(1,1),(2,2),(3,3)])
        sym  = Set([(1,2),(2,1)])
        chain = Set([(1,2),(2,3)])                    # has a 2-chain, lacks (1,3)
        nochain = Set([(1,2)])                        # NO 2-chain at all
        @test is_reflexive(eqr, S)
        @test !is_reflexive(sym, S)
        @test is_symmetric(sym)
        @test !is_symmetric(chain)
        @test is_transitive(Set([(1,2),(2,3),(1,3)]))
        @test !is_transitive(chain)                   # THE test that bites
        # CONTROL: nochain passes transitivity VACUOUSLY — true, but it proves
        # nothing about the implementation, which is why `chain` is above it.
        @test is_transitive(nochain)
        @test is_transitive(Set{Tuple{Int,Int}}())    # empty relation, also vacuous
    end
    @testset "2.4 equivalence classes partition the set" begin
        S = Set(1:6)
        mod3 = Set((i,j) for i in 1:6, j in 1:6 if (i - j) % 3 == 0)
        C = equivalence_classes(mod3, S)
        @test length(C) == 3
        @test union(C...) == S                        # covers
        @test sum(length, C) == length(S)             # and is disjoint
        @test all(c -> length(c) == 2, C)
        @test_throws Exception equivalence_classes(Set([(1,2)]), S)  # not an equivalence
    end
end

@testset "3 · operator theory on the two real lattices" begin
    N = 4
    @testset "3.1 assemble the Biofilms 6-neighbour Neumann Laplacian" begin
        L = assemble_lap6(N)
        @test size(L) == (N^3, N^3)
        # AGREEMENT WITH THE CODE — the only test that is sensitive to the stencil.
        Random.seed!(1)
        for _ in 1:10
            f = rand(N, N, N)
            @test reshape(L * vec(f), N, N, N) ≈ lap6_apply(f) atol=1e-12
        end
        @test issymmetric(L)                          # self-adjoint
        @test maximum(abs, sum(L, dims = 2)) < 1e-12  # uniform-field preservation (row sums)
        @test maximum(abs, sum(L, dims = 1)) < 1e-12  # mass conservation (column sums)
        @test norm(L * ones(N^3)) < 1e-12             # constants in the kernel
        @test maximum(eigvals(checked_symmetric(L))) < 1e-10  # negative semidefinite
    end
    @testset "3.2 assemble the unguarded cylinder reference" begin
        W, H, D = 5, 4, 0.15
        M = assemble_diff_cyl(W, H, D)
        Random.seed!(2)
        for _ in 1:10
            c = rand(W, H)
            @test reshape(M * vec(c), W, H) ≈ diff_cyl_direct(c, D) atol=1e-12
        end
        @test issymmetric(M)
        @test maximum(abs, sum(M, dims = 2)) < 1e-12   # uniform field
        @test maximum(abs, sum(M, dims = 1)) < 1e-12   # total mass
        d = deg_cyl(W, H)
        @test sort(unique(vec(d))) == [5, 8]          # cylinder: edge rows have 5
        # Each link carries D*(1/n_i + 1/n_j), which is symmetric in i and j.
        i, j = 1, 1 + W                               # (1,1) and (1,2)
        @test M[i, j] ≈ D * (1/d[1,1] + 1/d[1,2])
    end
    @testset "3.3 which detector catches which defect" begin
        W, H, D = 5, 4, 0.15
        good = assemble_diff_cyl(W, H, D)
        c8   = assemble_diff_cyl_const8(W, H, D)      # divisor hardcoded to 8
        mm   = assemble_diff_cyl_mismatch(W, H, D)    # takes with receiver's degree
        agrees(M) = all(1:5) do _
            c = rand(W, H)
            maximum(abs, reshape(M * vec(c), W, H) .- diff_cyl_direct(c, D)) < 1e-12
        end
        Random.seed!(3)
        @test agrees(good)
        # THE LESSON: symmetry and conservation both MISS the const-8 defect.
        @test issymmetric(c8)
        @test maximum(abs, sum(c8, dims = 2)) < 1e-12
        @test maximum(abs, sum(c8, dims = 1)) < 1e-12
        @test !agrees(c8)                             # only agreement catches it
        # This mismatch preserves a uniform field but FAILS total mass conservation.
        @test !issymmetric(mm)
        @test maximum(abs, sum(mm, dims = 2)) < 1e-12
        @test maximum(abs, sum(mm, dims = 1)) > 1e-3
        @test !agrees(mm)
    end
    @testset "3.4 the stability bound is the spectrum" begin
        # Explicit Euler on dc/dt = M c is stable iff dt*|λ| ≤ 2 for every λ.
        L = assemble_lap6(6)
        @test stability_bound(L) ≈ 2 / maximum(abs, eigvals(checked_symmetric(L)))
        @test 0.17 < stability_bound(L) < 0.18        # N=6; → 1/6 as N grows
        # Biofilms ships D_C * dt_field = 0.2 * 0.5 = 0.1, inside that bound.
        @test 0.2 * 0.5 < stability_bound(L)
        M1 = assemble_diff_cyl(5, 4, 1.0)
        @test 0.67 < stability_bound(M1) < 0.68
        # Reference only: do not transfer this result to engine.py's guarded update.
        @test stability_bound(M1) < 1.0
        bad = copy(M1); bad[1, 2] += 0.01
        @test_throws ArgumentError stability_bound(bad) # before any Symmetric wrapper
    end
end

@testset "4 · functional analysis on a discretisation" begin
    grid(n) = [(i - 0.5) / n for i in 1:n]            # midpoints of [0,1]
    f(x) = sinpi(x)
    @testset "4.1 the discrete L2 norm needs its measure weight" begin
        exact = 1 / sqrt(2)                           # ‖sin πx‖_L²[0,1]
        for n in (50, 200, 800)
            @test l2_norm(f.(grid(n)), 1 / n) ≈ exact atol=1e-3
        end
        # CONTROL: the unweighted version is not a norm of the function at all —
        # it grows like √n, so it cannot be stable under refinement.
        raw(n) = sqrt(sum(abs2, f.(grid(n))))
        @test raw(800) / raw(50) > 3.5                # ≈ √16 = 4
        @test !isapprox(raw(200), exact; atol = 1e-3)
    end
    @testset "4.2 inner-product laws" begin
        n = 400; dx = 1 / n; x = grid(n)
        u, v = f.(x), cospi.(x)
        @test inner(u, v, dx) ≈ inner(v, u, dx)                        # symmetry
        @test inner(u, u, dx) ≈ l2_norm(u, dx)^2                       # induces the norm
        @test abs(inner(u, v, dx)) <= l2_norm(u, dx) * l2_norm(v, dx) + 1e-12   # Cauchy–Schwarz
        @test l2_norm(u .+ v, dx) <= l2_norm(u, dx) + l2_norm(v, dx) + 1e-12    # triangle
        @test inner(u, v, dx) ≈ 0 atol=1e-3           # sin ⟂ cos on [0,1]
        @test l2_norm(2 .* u, dx) ≈ 2 * l2_norm(u, dx)                 # homogeneity
    end
    @testset "4.3 adjoint is not transpose" begin
        Random.seed!(4); A = randn(ComplexF64, 6, 6); x = randn(ComplexF64, 6); y = randn(ComplexF64, 6)
        @test adjoint_holds(A, x, y)                  # ⟨Ax, y⟩ == ⟨x, A*y⟩
        @test dot(A * x, y) ≈ dot(x, A' * y)
        @test !isapprox(dot(A * x, y), dot(x, transpose(A) * y))   # transpose is wrong here
        S = A + A'
        @test is_selfadjoint(S)
        @test !is_selfadjoint(A)
        # Floating point: an assembled matrix can be mathematically symmetric and
        # not bitwise symmetric, so is_selfadjoint must carry a tolerance.
        T = copy(S); T[1,2] += 1e-14
        @test !issymmetric(T)                         # exact test says no
        @test is_selfadjoint(T)                       # tolerant test says yes
    end
    @testset "4.4 sampling gives a LOWER bound on the operator norm" begin
        Random.seed!(5); A = randn(20, 20); A = A + A'
        truth = opnorm(A, 2)                          # the largest singular value
        Random.seed!(6); lb50   = opnorm_lower_bound(A, 50)
        Random.seed!(7); lb5000 = opnorm_lower_bound(A, 5_000)
        @test lb50   <= truth + 1e-12                 # a lower bound never exceeds
        @test lb5000 <= truth + 1e-12
        # CONTROL: it is strictly BELOW, so reporting the sampled maximum as "the
        # operator norm" reports a bound as a value. Measured here: 0.72 of truth.
        @test lb50 < 0.9 * truth
        # And 100x the samples does not rescue it — measured 0.83 of truth. The
        # cost is DIMENSION, not sample count: a random direction in 20-space is
        # nearly orthogonal to the top singular vector.
        @test lb5000 < 0.95 * truth
        # In 5 dimensions the same 50 samples land within a few percent.
        Random.seed!(8); B = randn(5, 5); B = B + B'
        Random.seed!(9)
        @test opnorm_lower_bound(B, 50) > 0.9 * opnorm(B, 2)
        # For a self-adjoint operator the Rayleigh quotient is bounded by λ_max.
        λmax = maximum(eigvals(checked_symmetric(A)))
        for _ in 1:20
            v = randn(20)
            @test rayleigh(A, v) <= λmax + 1e-9
        end
        @test_throws Exception rayleigh(A, zeros(20))  # refuses the zero vector
    end
end

@testset "5 · game theory on the toy's shielding term" begin
    @testset "5.0 the shielding law (no exercise — a fact to know)" begin
        @test shield(1.5, 0.0) == 1.0                   # isolated: no attenuation at all
        @test shield(1.5, 12.0) ≈ exp(-4.5)             # eight neighbours at 1.5: factor 90
        @test exp(K_SHIELD * 12.0 * 0.05) - 1 ≈ 0.162 atol=1e-3   # specs/05 table, last row
        # Survival time is monotone in S at fixed flux: more neighbours, longer life.
        @test log_survival_time(1.5, 12.0, 2.45, 0.05) > log_survival_time(1.5, 0.0, 2.45, 0.05)
    end
    @testset "5.1 private benefit is k·S, independent of flux" begin
        for S in (0.0, 3.0, 6.0, 12.0)
            @test private_benefit(1.5, S) == K_SHIELD * S
        end
        # Finite difference of the given log_survival_time at two fluxes agrees.
        h = 1e-6
        fd(flux) = (log_survival_time(1.5 + h, 6.0, flux, 0.05) - log_survival_time(1.5 - h, 6.0, flux, 0.05)) / (2h)
        @test private_benefit(1.5, 6.0) ≈ fd(2.45) atol=1e-6
        @test private_benefit(1.5, 6.0) ≈ fd(0.10) atol=1e-6          # flux independence
        # The specs/05 table: 0 / 3.8 / 7.8 / 16.2 percent per +0.05 purine.
        for (nb, pct) in ((0, 0.0), (2, 0.038), (4, 0.078), (8, 0.162))
            @test exp(private_benefit(1.5, 1.5 * nb) * PURINE_STEP) - 1 ≈ pct atol=5e-4
        end
        # CONTROL: worth exactly nothing when alone.
        @test private_benefit(9.0, 0.0) == 0.0
    end
    @testset "5.2 public benefit is k·u_j, and eight of them equal the private half" begin
        @test public_benefit(1.5, 1.5) == K_SHIELD * 1.5
        @test public_benefit(1.5, 3.0) == K_SHIELD * 3.0                # CONTROL: reads u_j
        @test public_benefit(1.5, 3.0) != public_benefit(1.5, 1.5)
        # Finite difference on the neighbour's own log survival time, S_j containing u_i.
        h = 1e-6
        S_j(u_i) = u_i + 7 * 1.5
        fd = (log_survival_time(1.5, S_j(1.5 + h), 2.45, 0.05) - log_survival_time(1.5, S_j(1.5 - h), 2.45, 0.05)) / (2h)
        @test public_benefit(1.5, 1.5) ≈ fd atol=1e-6
        # Eight neighbours at the seeding value: public half == private half.
        @test 8 * public_benefit(1.5, 1.5) ≈ private_benefit(1.5, 12.0)
    end
    @testset "5.3 private disincentive alone does not establish a dilemma" begin
        @test payoff(1.5, 12.0, 0.0) == K_SHIELD * 1.5 * 12.0
        @test payoff(1.5, 12.0, 2.0) == K_SHIELD * 1.5 * 12.0 - 3.0
        # CONTROL: with no cost there is no private disincentive at any neighbour sum.
        for S in (0.0, 3.0, 6.0, 12.0)
            @test !has_private_disincentive(S, 0.0)
        end
        @test has_private_disincentive(0.0, 0.01)                     # alone, any cost is a pure loss
        @test !has_private_disincentive(12.0, 2.0)                    # threshold is c = k·S = 3.0
        @test has_private_disincentive(12.0, 4.0)
        @test_throws Exception has_private_disincentive(6.0, -1.0)    # a negative cost is a refusal
    end
    @testset "5.4 best response is bang-bang, and a tie is a refusal" begin
        @test best_response(3.9, 1.0) == PURINE_MIN      # S* = c/k = 4
        @test best_response(4.1, 1.0) == PURINE_MAX
        @test_throws Exception best_response(4.0, 1.0)  # exact tie: throw, do not pick
        for S in (0.5, 3.0, 12.0)
            @test best_response(S, 0.0) == PURINE_MAX    # no cost: always max
        end
        # CONTROL: a flat payoff is a tie, not a free MAX.
        @test_throws Exception best_response(0.0, 0.0)
    end
    @testset "5.5 frozen by supply, not by weak selection" begin
        @test mutation_events(184, 0.02) ≈ 3.68
        @test max_drift(3.68, PURINE_STEP) ≈ 0.184
        @test (1.50035 - 1.49983) < max_drift(mutation_events(184, 0.02), PURINE_STEP)
        @test mutation_events(0, 0.02) == 0.0            # CONTROL
    end
end

@testset "6 · decision theory on the pre-registration" begin
    @testset "6.0 the sd convention (no exercise — a fact to know)" begin
        @test std([1, 2, 3, 4]) == std([1, 2, 3, 4]; corrected = true)    # n-1 by default
        @test NULL_SD > 0
        @test mean(EFFECT_SAMPLE) - mean(NULL_SAMPLE) ≈ 3 * NULL_SD
    end
    @testset "6.1 the floor comes from independent sham run-pair contrasts" begin
        @test floor_from_sham(SHAM_CONTRASTS) == FLOOR_MULTIPLE * std(SHAM_CONTRASTS; corrected=true)
        @test floor_from_sham(SHAM_CONTRASTS; multiple = 3.0) == 3.0 * std(SHAM_CONTRASTS; corrected=true)
        @test floor_from_sham(10 .* SHAM_CONTRASTS) ≈ 10 * floor_from_sham(SHAM_CONTRASTS)   # CONTROL: scales
        @test_throws Exception floor_from_sham([1.0])          # one seed is not a pilot
        @test_throws Exception floor_from_sham(fill(3.0, 10))  # zero spread is a broken pilot
    end
    @testset "6.2 decide is sign-blind and refuses NaN" begin
        floor = FLOOR_MULTIPLE * NULL_SD
        @test decide(3 * NULL_SD, floor) == :detected
        @test decide(-3 * NULL_SD, floor) == :detected          # CONTROL: sign-blind
        @test decide(0.5 * NULL_SD, floor) == :below_floor
        @test decide(mean(EFFECT_SAMPLE) - mean(NULL_SAMPLE), floor) == :detected
        @test_throws Exception decide(NaN, floor)
        @test_throws Exception decide(1.0, -1.0)
    end
    @testset "6.3 independent calibration and evaluation; invalid posthoc demo" begin
        calibration_rng = Random.MersenneTwister(99)
        sham = NULL_SD .* (randn(calibration_rng, 10) .- randn(calibration_rng, 10))
        floor = floor_from_sham(sham)
        rate = false_detection_rate(Random.MersenneTwister(1), 400, floor; contrast_sample_size=1)
        @test 0 <= rate <= 1 # estimated sham floor has no universal 10% guarantee
        # Known-SD two-contrast-SD threshold: Gaussian rate about 4.55%.
        for n in (1, 10)
            r = false_detection_rate(Random.MersenneTwister(2), 100_000,
                                     2NULL_SD*sqrt(2/n); contrast_sample_size=n)
            @test abs(r - 0.0455) < 0.004
        end
        @test_throws ArgumentError false_detection_rate(Random.MersenneTwister(1), 50, -1.0; contrast_sample_size=1)
        @test_throws ArgumentError false_detection_rate(Random.MersenneTwister(1), 50, NaN; contrast_sample_size=1)
        @test_throws ArgumentError false_detection_rate(Random.MersenneTwister(1), 50, 1.0; contrast_sample_size=0)
        effects = [0.2, -0.3, 0.4] # in-sample leakage demo, explicitly invalid
        bad_floor = posthoc_floor(effects)
        @test all(decide(e, bad_floor) == :detected for e in effects)
        @test_throws ArgumentError decide(1.0, posthoc_floor(effects; eps=1e9))
    end
    @testset "6.4 no decision without a declared loss" begin
        x = randn(Random.MersenneTwister(7), 200_000)
        @test prob_exceeds(x, 1.96) ≈ 0.05 atol=0.01
        @test prob_exceeds(x, 0.0) == 1.0                 # CONTROL
        @test prob_exceeds(x, Inf) == 0.0                 # CONTROL
        zero_one(v, f) = abs(v) > f ? 1.0 : 0.0
        @test expected_loss(x, 1.0, zero_one) == prob_exceeds(x, 1.0)
        @test_throws Exception expected_loss(x, 1.0, nothing)
    end
end
end
:all_green
catch err
    err isa Test.TestSetException || rethrow()
    :incomplete
end

println()
if PRACTICE_STATUS === :all_green
    println("All green. Every CONTROL held, which is the part that matters.")
else
    println("The summary above is the map: Error = an unimplemented stub, Fail = an")
    println("implementation the spec disagrees with. Fill the next stub and re-include.")
end
PRACTICE_STATUS === :all_green || error("sandbox exercises incomplete")
include(joinpath(@__DIR__, "analysis", "sandbox_controls.jl"))
end # module
