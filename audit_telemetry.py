"""Audit the recovered telemetry CSV against the arithmetic the engine implies.

  python -I audit_telemetry.py data/simulation_telemetry.csv

No engine import. Facts used: 81 vent sites x 25 = 2025 injected per step; each birth
deducts 15; initial population 120; M(0) = 2025 (the initializer injects once).
"""
import csv
import sys

import numpy as np

INJECT = 81 * 25.0
BIRTH_COST = 15.0
INITIAL_POP = 120
M0 = 2025.0


def main(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    step = np.array([int(r["step"]) for r in rows])
    pop = np.array([int(r["population_count"]) for r in rows])
    mass = np.array([float(r["total_monomer_mass"]) for r in rows])
    purine = np.array([float(r["mean_purine_ratio"]) for r in rows])
    d_mass = np.diff(np.concatenate([[M0], mass]))
    d_pop = np.diff(np.concatenate([[INITIAL_POP], pop]))
    inferred_births = (INJECT - d_mass) / BIRTH_COST

    print(f"rows={len(rows)} steps {step[0]}..{step[-1]}")
    print("step  dM        births_from_mass  births_from_pop")
    for i in range(min(5, len(rows))):
        print(f"{step[i]:<5} {d_mass[i]:<9.3f} {inferred_births[i]:<17.4f} {d_pop[i]}")

    break_step = None
    for i in range(len(rows)):
        if not np.isclose(inferred_births[i], round(inferred_births[i]), atol=1e-6) or \
           int(round(inferred_births[i])) != d_pop[i]:
            break_step = step[i]
            clipped = INJECT - BIRTH_COST * d_pop[i] - d_mass[i]
            break
    print(f"identity dM == 2025 - 15*births holds through step {break_step - 1 if break_step else step[-1]}; "
          f"first break at step {break_step} (implied clip {clipped:.3f} monomers)" if break_step
          else "identity holds for every step")

    monotone = bool(np.all(np.diff(pop) >= 0))
    print(f"population monotone non-decreasing: {monotone} (min dPop = {np.diff(pop).min()})")
    print(f"total births (from population, no deaths possible): {pop[-1] - INITIAL_POP}")
    print(f"mean purine range: {purine.min():.5f} .. {purine.max():.5f}  "
          f"(mutation supply ~ {(pop[-1] - INITIAL_POP) * 0.02:.1f} events at +-0.05; nothing selected)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/simulation_telemetry.csv")
