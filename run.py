# SPDX-License-Identifier: MIT
"""Runner for both engines.

  python run.py --engine original --seed 1 --steps 100 --out out/original_s1.csv
  python run.py --engine fixed    --seed 1 --steps 100 --out out/fixed_s1.csv

original: 5 columns, the same as the recovered CSV (step, population_count,
          total_monomer_mass, mean_purine_ratio, mean_radiotropism).
fixed:    those 5 plus births, deaths, injected_gross, inject_clip, diffusion_clip,
          birth_sink, death_return, mean_occupied_degree, clustering_index, mean_y
          (15 columns), a step-0 row recording the seeded configuration (ledger
          columns 0), and the ledger identity asserted every step with abs_tol = 1e-8.
          --field-scale F multiplies the radiation field (damage AND tropism bias);
          --decay-scale S multiplies the decay constant only (damage alone), so
          field 1 / decay 0 is the attribution arm: gradient on, damage off.
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
SPATIAL_COLS = ["mean_occupied_degree", "clustering_index", "mean_y"]


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


def run_fixed(seed, steps, writer, field_scale=1.0, decay_scale=1.0):
    import engine as E
    seed_all(seed)
    grid = np.empty((E.WIDTH, E.HEIGHT), dtype=object)
    mono = np.zeros((E.WIDTH, E.HEIGHT), dtype=np.float64)
    field = E.make_radiation_field() * field_scale
    gx, gy = E.field_gradient(field)
    decay = E.DECAY_CONSTANT * decay_scale
    grid = E.initialize_defensive_population(grid, mono)   # injects once: M(0) = 2025
    m_prev = float(np.sum(mono))
    n0, m0, p0, t0, d0, i0, y0 = E.summarize(grid, mono)
    writer.writerow([0, n0, m0, p0, t0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, d0, i0, y0])   # seeded configuration
    total_deaths = 0
    total_births = 0
    pops = []
    for step in range(1, steps + 1):
        grid, mono, L = E.step(grid, mono, field, gx, gy, decay=decay)
        n, m, purine, tropism, mean_occ, index, mean_y = E.summarize(grid, mono)
        predicted = L["injected_gross"] - L["inject_clip"] - L["diffusion_clip"] - L["birth_sink"] + L["death_return"]
        assert math.isclose(m - m_prev, predicted, abs_tol=LEDGER_TOL), \
            f"ledger identity broken at step {step}: dM={m - m_prev!r} predicted={predicted!r}"
        m_prev = m
        total_deaths += L["deaths"]
        total_births += L["births"]
        pops.append(n)
        writer.writerow([step, n, m, purine, tropism] + [L[c] for c in LEDGER_COLS] + [mean_occ, index, mean_y])
        if n == 0:
            break
    monotone = all(b >= a for a, b in zip(pops, pops[1:]))
    print(f"engine=fixed seed={seed} steps={steps} field_scale={field_scale} decay_scale={decay_scale} "
          f"population={pops[-1]} births={total_births} deaths={total_deaths} "
          f"population_monotone={monotone} ledger_identity_held=True "
          f"mean_occupied_degree={mean_occ:.4f} clustering_index={index:.4f} mean_y={mean_y:.4f}")


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--engine", choices=["original", "fixed"], required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--steps", type=int, default=100)
    p.add_argument("--out", required=True)
    p.add_argument("--field-scale", type=float, default=1.0, help="multiplies the radiation field (damage and tropism bias)")
    p.add_argument("--decay-scale", type=float, default=1.0, help="multiplies DECAY_CONSTANT only (damage alone)")
    a = p.parse_args(argv)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", newline="") as f:
        w = csv.writer(f)
        if a.engine == "original":
            if a.field_scale != 1.0 or a.decay_scale != 1.0:
                sys.exit("--field-scale and --decay-scale apply to the fixed engine only")
            w.writerow(COLUMNS5)
            run_original(a.seed, a.steps, w)
        else:
            w.writerow(COLUMNS5 + LEDGER_COLS + SPATIAL_COLS)
            run_fixed(a.seed, a.steps, w, a.field_scale, a.decay_scale)


if __name__ == "__main__":
    main()
