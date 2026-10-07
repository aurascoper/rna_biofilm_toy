# Included inside BioenergyToysSandbox; the original exercise stays untouched.
finite_real(x, label) = x isa Real && isfinite(x) ? x : throw(ArgumentError("$label must be finite and real"))
function nonnegative(x, label)
    finite_real(x, label) >= 0 || throw(ArgumentError("$label must be nonnegative"))
    x
end
function positive_int(n, label)
    n isa Integer && !(n isa Bool) && n > 0 || throw(ArgumentError("$label must be a positive integer"))
    n
end
function finite_samples(xs)
    isempty(xs) && throw(ArgumentError("empty sample"))
    all(x -> x isa Real && isfinite(x), xs) || throw(ArgumentError("sample must be finite and real"))
    xs
end

vars(v::Var) = [v.name]
vars(f::Not) = vars(f.a)
vars(f::Union{And,Or,Implies,Iff}) = sort!(unique(vcat(vars(f.a), vars(f.b))))
function evaluate(v::Var, a::AbstractDict)
    haskey(a, v.name) || throw(ArgumentError("missing variable $(v.name)"))
    a[v.name] isa Bool || throw(ArgumentError("assignment must be Boolean"))
    a[v.name]
end
evaluate(f::Not, a::AbstractDict) = !evaluate(f.a, a)
# Eager Boolean operators validate both operands, including missing variables.
evaluate(f::And, a::AbstractDict) = evaluate(f.a, a) & evaluate(f.b, a)
evaluate(f::Or, a::AbstractDict) = evaluate(f.a, a) | evaluate(f.b, a)
evaluate(f::Implies, a::AbstractDict) = !evaluate(f.a, a) | evaluate(f.b, a)
evaluate(f::Iff, a::AbstractDict) = evaluate(f.a, a) == evaluate(f.b, a)
function truth_table(f::Formula)
    vs = vars(f); n = length(vs)
    n <= MAX_TRUTH_TABLE_VARS || throw(ArgumentError("truth table exceeds declared variable bound"))
    map(0:((1 << n)-1)) do bits
        a = Dict{Symbol,Bool}(vs[j] => !iszero(bits & (1 << (j-1))) for j in 1:n)
        a => evaluate(f, a)
    end
end
is_tautology(f::Formula) = all(last, truth_table(f))
is_contradiction(f::Formula) = !any(last, truth_table(f))
is_satisfiable(f::Formula) = any(last, truth_table(f))
equivalent(f::Formula, g::Formula) = is_tautology(Iff(f, g))

dedup_isequal(xs) = unique(xs)
function dedup_equals(xs)
    out = empty(xs)
    for x in xs
        any(y -> y == x, out) || push!(out, x)
    end
    out
end
function powerset(S::Set{T}) where T
    elems = collect(S); n = length(elems)
    n <= MAX_TRUTH_TABLE_VARS || throw(ArgumentError("powerset exceeds declared enumeration bound"))
    [Set{T}(elems[j] for j in 1:n if !iszero(bits & (1 << (j-1)))) for bits in 0:((1 << n)-1)]
end
is_reflexive(R, S) = all((x,x) in R for x in S)
is_symmetric(R) = all((b,a) in R for (a,b) in R)
is_transitive(R) = all((a,d) in R for (a,b) in R for (c,d) in R if b == c)
function equivalence_classes(R, S)
    # Domain validation precedes every relation-property evaluation.
    for edge in R
        edge isa Tuple && length(edge) == 2 || throw(ArgumentError("relation entries must be pairs"))
        all(x -> x in S, edge) || throw(ArgumentError("relation endpoint outside ground set"))
    end
    is_reflexive(R,S) && is_symmetric(R) && is_transitive(R) || throw(ArgumentError("not an equivalence relation"))
    unique([Set(y for y in S if (x,y) in R) for x in S])
end

function assemble_lap6(N)
    positive_int(N, "N")
    M = zeros(N^3,N^3); idx(x,y,z) = x+(y-1)*N+(z-1)*N^2
    for z in 1:N, y in 1:N, x in 1:N, (dx,dy,dz) in NB6
        nx,ny,nz = x+dx,y+dy,z+dz
        if 1 <= nx <= N && 1 <= ny <= N && 1 <= nz <= N
            i,j = idx(x,y,z),idx(nx,ny,nz)
            M[i,j] += 1; M[i,i] -= 1
        end
    end
    M
end
function assemble_diff_cyl(W,H,D)
    positive_int(W,"width"); positive_int(H,"height"); nonnegative(D,"diffusivity")
    M = zeros(W*H,W*H); deg = deg_cyl(W,H); idx(x,y) = x+(y-1)*W
    for y in 1:H, x in 1:W, (nx,ny) in nbrs_cyl(x,y,W,H)
        i,j,q = idx(x,y),idx(nx,ny),D/deg[x,y]
        M[j,i] += q; M[j,j] -= q; M[i,i] -= q; M[i,j] += q
    end
    M
end
function stability_bound(M)
    A = checked_symmetric(M) # Validates BEFORE the wrapper.
    isempty(A) && throw(ArgumentError("empty operator"))
    λ = eigvals(A); ρ = maximum(abs,λ)
    iszero(ρ) && return Inf
    # Scale the eigensolver roundoff allowance to the operator itself. An
    # absolute floor would incorrectly accept a small positive operator.
    spectral_roundoff = 8eps(Float64)*size(M,1)*ρ
    maximum(λ) > spectral_roundoff && return 0.0
    2/ρ
end
function euler_reference(M,c0; duration,max_step)
    nonnegative(duration,"duration")
    finite_real(max_step,"maximum step") > 0 || throw(ArgumentError("maximum step must be positive"))
    all(isfinite,c0) || throw(ArgumentError("nonfinite initial state"))
    size(M,2) == length(c0) || throw(ArgumentError("state/operator dimension mismatch"))
    bound = stability_bound(M)
    bound > 0 || throw(ArgumentError("operator has no positive stable Euler step"))
    times = [0.0]; states = [Float64.(c0)]; t = 0.0
    while t < duration
        remaining = duration-t
        dt = isinf(bound) ? min(max_step,remaining) : min(max_step,remaining,bound)
        isfinite(dt) && dt > 0 && t+dt > t || throw(ArgumentError("nonadvancing time"))
        next = states[end] + dt*(M*states[end])
        all(isfinite,next) || throw(ArgumentError("nonfinite Euler state"))
        t = dt == remaining ? Float64(duration) : t+dt
        push!(times,t); push!(states,next)
    end
    (; times, states)
end

function l2_norm(f,dx)
    finite_real(dx,"measure") > 0 || throw(ArgumentError("measure must be positive"))
    all(isfinite,f) || throw(ArgumentError("nonfinite function"))
    sqrt(sum(abs2,f)*dx)
end
function inner(u,v,dx)
    finite_real(dx,"measure") > 0 || throw(ArgumentError("measure must be positive"))
    all(isfinite,u) && all(isfinite,v) || throw(ArgumentError("nonfinite functions"))
    dot(u,v)*dx
end
adjoint_holds(A,x,y) = isapprox(dot(A*x,y),dot(x,A'*y))
function is_selfadjoint(M; atol=1e-10)
    nonnegative(atol,"tolerance")
    size(M,1) == size(M,2) && all(isfinite,M) && isapprox(M,M'; atol,rtol=0)
end
function opnorm_lower_bound(M,nsamples)
    positive_int(nsamples,"samples"); all(isfinite,M) || throw(ArgumentError("nonfinite matrix"))
    best = 0.0
    for _ in 1:nsamples
        v = randn(size(M,2)); nv = norm(v)
        nv > 0 && (best = max(best,norm(M*v)/nv))
    end
    best
end
function rayleigh(M,v)
    all(isfinite,M) && all(isfinite,v) || throw(ArgumentError("nonfinite Rayleigh input"))
    nv2 = sum(abs2,v); nv2 > 0 || throw(ArgumentError("zero vector"))
    real(dot(v,M*v)/nv2)
end

function private_benefit(u_i,S_i)
    nonnegative(u_i,"purine"); nonnegative(S_i,"neighbor sum"); K_SHIELD*S_i
end
function public_benefit(u_i,u_j)
    nonnegative(u_i,"purine"); nonnegative(u_j,"neighbor purine"); K_SHIELD*u_j
end
function payoff(u_i,S_i,c)
    nonnegative(c,"cost"); u_i*private_benefit(u_i,S_i)-c*u_i
end
function has_private_disincentive(S_i,c)
    nonnegative(S_i,"neighbor sum"); nonnegative(c,"cost"); c > K_SHIELD*S_i
end
function best_response(S_i,c)
    nonnegative(S_i,"neighbor sum"); nonnegative(c,"cost")
    b = K_SHIELD*S_i; b == c && throw(ArgumentError("flat payoff: declared tie refusal"))
    b > c ? PURINE_MAX : PURINE_MIN
end
function mutation_events(births,rate)
    nonnegative(births,"births"); nonnegative(rate,"rate")
    rate <= 1 || throw(ArgumentError("mutation probability exceeds one")); births*rate
end
max_drift(events,step) = nonnegative(events,"events")*nonnegative(step,"step")

function floor_from_sham(sham_contrasts; multiple=FLOOR_MULTIPLE)
    finite_samples(sham_contrasts)
    length(sham_contrasts) >= 2 || throw(ArgumentError("at least two sham contrasts required"))
    finite_real(multiple,"multiple") > 0 || throw(ArgumentError("multiple must be positive"))
    s = std(sham_contrasts; corrected=true)
    isfinite(s) && s > 0 || throw(ArgumentError("invalid sham spread"))
    result = multiple*s; finite_real(result,"floor")
end
function decide(effect,floor)
    finite_real(effect,"effect"); nonnegative(floor,"floor")
    abs(effect) > floor ? :detected : :below_floor
end
# INVALID, intentionally retained to demonstrate in-sample threshold leakage.
function posthoc_floor(effects; eps=1e-9)
    finite_samples(effects); nonnegative(eps,"epsilon"); minimum(abs,effects)-eps
end
function false_detection_rate(rng,n_draws,floor; contrast_sample_size)
    nonnegative(floor,"floor"); positive_int(n_draws,"draws")
    n = positive_int(contrast_sample_size,"contrast sample size")
    detected = 0
    for _ in 1:n_draws
        contrast = NULL_SD*(sum(randn(rng,n))-sum(randn(rng,n)))/n
        detected += decide(contrast,floor) === :detected
    end
    detected/n_draws
end
function prob_exceeds(samples,floor)
    finite_samples(samples)
    # Original exercise explicitly allows +Inf as a probability-query limit;
    # decision/calibration APIs continue to refuse nonfinite floors.
    floor isa Real && !isnan(floor) && floor >= 0 || throw(ArgumentError("invalid probability threshold"))
    count(x -> abs(x)>floor,samples)/length(samples)
end
function expected_loss(samples,floor,loss)
    finite_samples(samples); nonnegative(floor,"floor")
    loss === nothing && throw(ArgumentError("declared loss required"))
    values = [loss(x,floor) for x in samples]; finite_samples(values); mean(values)
end
