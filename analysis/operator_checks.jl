# SPDX-License-Identifier: MIT
module ArtifactOperatorChecks
using LinearAlgebra
export checked_symmetric

"""Validate the assembled operator before choosing a triangle for spectral analysis."""
function checked_symmetric(M::AbstractMatrix; atol=1e-12)
    isfinite(atol) && atol >= 0 || throw(ArgumentError("invalid symmetry tolerance"))
    size(M, 1) == size(M, 2) || throw(ArgumentError("operator must be square"))
    all(x -> x isa Real && isfinite(x), M) || throw(ArgumentError("operator must be finite and real"))
    isapprox(M, transpose(M); atol=atol, rtol=0) ||
        throw(ArgumentError("asymmetric assembled operator; refusing Symmetric wrapper"))
    return Symmetric(M)
end
end
