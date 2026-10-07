"""Runner for both engines.

  python run.py --engine original --seed 1 --steps 100 --out out/original_s1.csv
  python run.py --engine fixed    --seed 1 --steps 100 --out out/fixed_s1.csv

original: 5 columns, the same as the recovered CSV (step, population_count,
          total_monomer_mass, mean_purine_ratio, mean_radiotropism).
fixed:    those 5 plus births, deaths, injected_gross, inject_clip, diffusion_clip,
          birth_sink, death_return (12 columns), and the ledger identity is asserted
          every step with abs_tol = 1e-8.
"""
import argparse
import csv
import math
import os
import random
import sys

import numpy as np

LEDGER_TOL = 1e-8
COLUMNS5 = ["step", "population_count", "total_monomer_mass", "mean_purine_ratio", "mean_radiotropism"]
LEDGER_COLS = ["births", "deaths", "injected_gross", "inject_clip", "diffusion_clip", "birth_sink", "death_return"]


def seed_all(seed):
    random.seed(seed)
    np.random.seed(seed)


def run_original(seed, steps, writer):
    import engine_original as E
    seed_all(seed)
    grid = np.empty((E.WIDTH, E.HEIGHT), dtype=object)
    mono = np.zeros((E.WIDTH, E.HEIGHT), dtype=np.float64)
    field = E.make_radiation_field()
    grid = E.initialize_defensive_population(grid, mono)
    deaths = 0
    for step in range(1, steps + 1):
        occupied_before = {(x, y) for x in range(E.WIDTH) for y in range(E.HEIGHT) if grid[x, y]["occupied"]}
        grid, mono = E.execute_system_timestep(grid, mono, field)
        # A cell occupied before and empty after can only be a lysis (births never vacate).
        deaths += sum(1 for (x, y) in occupied_before if not grid[x, y]["occupied"])
        n, purine, tropism = 0, 0.0, 0.0
        for x in range(E.WIDTH):
            for y in range(E.HEIGHT):
                if grid[x, y]["occupied"]:
                    n += 1
                    purine += grid[x, y]["organism"].purine_ratio
                    tropism += grid[x, y]["organism"].radiotropism
        writer.writerow([step, n, float(np.sum(mono)), purine / n if n else 0.0, tropism / n if n else 0.0])
        if n == 0:
            break
    healths = [grid[x, y]["organism"].core_health for x in range(E.WIDTH) for y in range(E.HEIGHT) if grid[x, y]["occupied"]]
    print(f"engine=original seed={seed} steps={steps} population={len(healths)} deaths={deaths} "
          f"survivor_health_min={min(healths):.6f} survivor_health_max={max(healths):.6f}")


def run_fixed(seed, steps, writer):
    import engine as E
    seed_all(seed)
    grid = np.empty((E.WIDTH, E.HEIGHT), dtype=object)
    mono = np.zeros((E.WIDTH, E.HEIGHT), dtype=np.float64)
    field = E.make_radiation_field()
    gx, gy = E.field_gradient(field)
    grid = E.initialize_defensive_population(grid, mono)   # injects once: M(0) = 2025
    m_prev = float(np.sum(mono))
    total_deaths = 0
    total_births = 0
    pops = []
    for step in range(1, steps + 1):
        grid, mono, L = E.step(grid, mono, field, gx, gy)
        n, m, purine, tropism = E.summarize(grid, mono)
        predicted = L["injected_gross"] - L["inject_clip"] - L["diffusion_clip"] - L["birth_sink"] + L["death_return"]
        assert math.isclose(m - m_prev, predicted, abs_tol=LEDGER_TOL), \
            f"ledger identity broken at step {step}: dM={m - m_prev!r} predicted={predicted!r}"
        m_prev = m
        total_deaths += L["deaths"]
        total_births += L["births"]
        pops.append(n)
        writer.writerow([step, n, m, purine, tropism] + [L[c] for c in LEDGER_COLS])
        if n == 0:
            break
    monotone = all(b >= a for a, b in zip(pops, pops[1:]))
    print(f"engine=fixed seed={seed} steps={steps} population={pops[-1]} births={total_births} deaths={total_deaths} "
          f"population_monotone={monotone} ledger_identity_held=True")


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--engine", choices=["original", "fixed"], required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--steps", type=int, default=100)
    p.add_argument("--out", required=True)
    a = p.parse_args(argv)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", newline="") as f:
        w = csv.writer(f)
        if a.engine == "original":
            w.writerow(COLUMNS5)
            run_original(a.seed, a.steps, w)
        else:
            w.writerow(COLUMNS5 + LEDGER_COLS)
            run_fixed(a.seed, a.steps, w)


if __name__ == "__main__":
    main()
