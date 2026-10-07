@testset "sandbox additional independent controls" begin
    @testset "REL-DOMAIN: membership before relation properties" begin
        @test_throws ArgumentError equivalence_classes(Set([(1,1),(2,2)]),Set([1]))
        @test_throws ArgumentError equivalence_classes(Set([(1,1,1)]),Set([1]))
        @test_throws ArgumentError equivalence_classes(Set([1]),Set([1]))
        @test isempty(equivalence_classes(Set{Tuple{Int,Int}}(),Set{Int}()))
        @test_throws ArgumentError evaluate(q ∧ p,Dict(:q=>false))
        @test_throws ArgumentError evaluate(q ∨ p,Dict(:q=>true))
        @test_throws ArgumentError evaluate(p,Dict(:p=>1))
    end
    @testset "OPERATOR: each invariant is load-bearing" begin
        W,H,D = 5,4,.15; M = assemble_diff_cyl(W,H,D)
        @test maximum(abs,M-M') < 1e-15
        @test maximum(abs,sum(M;dims=1)) < 1e-15
        @test maximum(abs,sum(M;dims=2)) < 1e-15
        c = randn(MersenneTwister(77),W,H)
        @test M*vec(c) ≈ vec(diff_cyl_direct(c,D))
        # Reconstruct the actual pasted two-entry operator, not a guessed defect.
        bad = zeros(W*H,W*H); deg = deg_cyl(W,H)
        for y in 1:H,x in 1:W,(nx,ny) in nbrs_cyl(x,y,W,H)
            i,j = x+(y-1)*W,nx+(ny-1)*W
            bad[j,i] += D/deg[x,y]; bad[i,i] -= D/deg[x,y]
        end
        @test maximum(abs,sum(bad;dims=1)) < 1e-15
        @test maximum(abs,sum(bad;dims=2)) ≈ .03375
        @test maximum(abs,bad-bad') > .01
        @test_throws ArgumentError stability_bound(bad)
        @test_throws ArgumentError stability_bound([NaN 0.;0. 0.])
        @test_throws ArgumentError stability_bound(zeros(2,3))
        @test stability_bound(ones(1,1)) == 0
        @test stability_bound(fill(1e-20,1,1)) == 0
        @test stability_bound(fill(-1e-20,1,1)) ≈ 2e20
        @test stability_bound(zeros(1,1)) == Inf
        result = euler_reference(zeros(2,2),[2.,3.]; duration=1.,max_step=.3)
        @test result.times[end] == 1.
        @test all(isfinite,result.times)
        @test all(s -> s == [2.,3.],result.states)
        @test maximum(diff(result.times)) <= .3 + eps()
        @test length(result.times) == 5
        result = euler_reference([-1. 1.;1. -1.],[1.,0.];duration=.5,max_step=.1)
        @test sum(result.states[end]) ≈ 1
        @test norm(result.states[end] .- .5) < norm(result.states[1] .- .5)
        @test_throws ArgumentError euler_reference(ones(1,1),[1.];duration=1.,max_step=.1)
        @test_throws ArgumentError euler_reference(zeros(1,1),[1.];duration=Inf,max_step=.1)
        @test_throws ArgumentError euler_reference(zeros(1,1),[1.];duration=1.,max_step=Inf)
    end
    @testset "FLOOR: numeric threshold and independent streams" begin
        for bad in (NaN,Inf,-Inf)
            @test_throws ArgumentError decide(bad,1.)
            @test_throws ArgumentError decide(1.,bad)
            @test_throws ArgumentError floor_from_sham([1.,bad])
            @test_throws ArgumentError floor_from_sham([1.,2.];multiple=bad)
        end
        @test_throws ArgumentError floor_from_sham([1.,2.];multiple=0)
        @test_throws ArgumentError false_detection_rate(MersenneTwister(1),10,x->0.;contrast_sample_size=1)
        @test_throws ArgumentError false_detection_rate(MersenneTwister(1),0,1.;contrast_sample_size=1)
        @test_throws ArgumentError false_detection_rate(MersenneTwister(1),10,1.;contrast_sample_size=true)
        @test_throws ArgumentError decide(.1,posthoc_floor([0.]))
        calibration = MersenneTwister(2026100701); evaluation = MersenneTwister(2026100702)
        sham = sqrt(2)*NULL_SD*randn(calibration,10)
        floor = floor_from_sham(sham)
        @test floor == 2std(sham;corrected=true)
        @test 0 <= false_detection_rate(evaluation,1000,floor;contrast_sample_size=1) <= 1
        @test_throws ArgumentError best_response(NaN,1.)
        @test_throws ArgumentError has_private_disincentive(1.,Inf)
    end
end
