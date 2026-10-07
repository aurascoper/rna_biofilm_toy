"""Synthetic Gaussian references; never reads or calibrates an engine output."""
import argparse
import json
import math
from pathlib import Path

import numpy as np


def ten_sham_probability():
    # Student t_9 tail via x=3*tan(theta) and the exact cos^8 recurrence.
    theta = math.atan(2 / 3)
    integral = math.pi / 2 - theta
    for power in (2, 4, 6, 8):
        integral = ((power - 1) * integral - math.sin(theta) * math.cos(theta) ** (power - 1)) / power
    normalizer = math.gamma(5) / (3 * math.sqrt(math.pi) * math.gamma(4.5))
    return 6 * normalizer * integral


def diagnostics():
    references = {
        "known_contrast_sd": math.erfc(math.sqrt(2)),
        "ten_independent_shams_known_zero_mean": ten_sham_probability(),
        "historical_individual_sd_n1": math.erfc(1),
        "historical_individual_sd_n10": math.erfc(math.sqrt(10)),
    }
    expected = [0.045500263896358396, 0.07655282377070101, 0.15729920705028516, 7.744216431044074e-6]
    assert all(math.isclose(x, y, rel_tol=1e-12, abs_tol=1e-14) for x, y in zip(references.values(), expected))
    calibration_rng = np.random.default_rng(2026100706)
    evaluation_rng = np.random.default_rng(2026100707)
    s = calibration_rng.normal(size=(300_000, 10)).std(axis=1, ddof=1)
    future = evaluation_rng.normal(size=len(s))
    estimated_rate = float(np.mean(np.abs(future) > 2 * s))
    assert abs(estimated_rate - references["ten_independent_shams_known_zero_mean"]) < 0.002
    assert float(np.mean(np.abs(future) > 2)) < estimated_rate
    return {
        "purpose": "synthetic Gaussian diagnostic, not toy calibration",
        "references": references,
        "estimated_sd_monte_carlo": estimated_rate,
        "draws": len(s),
        "calibration_seed": 2026100706,
        "evaluation_seed": 2026100707,
        "assumptions": "independent Gaussian future contrast, known zero mean, corrected SD of ten independent shams",
        "finite_sham_general_guarantee": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = diagnostics()
    with args.output.open("x") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    print(json.dumps(result, indent=2))
