import math
import os
import random
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import engine as E            # noqa: E402
import engine_original as O   # noqa: E402


def seed_all(s):
    random.seed(s)
    np.random.seed(s)


def test_neighbor_counts():
    assert len(E.cylinder_neighbors(10, 0)) == 5
    assert len(E.cylinder_neighbors(10, E.HEIGHT - 1)) == 5
    assert len(E.cylinder_neighbors(10, 25)) == 8
    assert len(E.cylinder_neighbors(0, 25)) == 8      # x wraps: no corners
    assert (E.WIDTH - 1, 25) in E.cylinder_neighbors(0, 25)


def test_dx_unwrap():
    assert E.unwrap_dx(0, 49) == -1
    assert E.unwrap_dx(49, 0) == 1
    assert E.unwrap_dx(10, 11) == 1
    assert E.unwrap_dx(10, 9) == -1


def test_death_reachable():
    # Lone organism on the top row (flux 2.45). Its five neighbours (x wraps, y does not)
    # are all unoccupied, so shielding is zero. Row 49 is 24 rows from the plume: nonzero
    # monomer support grows one row per step, so it sees no monomer and cannot replicate.
    # Damage per step 2.45 * 0.05 = 0.1225: alive after step 8 (0.02), dead at step 9.
    seed_all(0)
    grid = E.empty_grid()
    mono = np.zeros((E.WIDTH, E.HEIGHT))
    field = E.make_radiation_field()
    gx, gy = E.field_gradient(field)
    grid[10, 49] = {"occupied": True, "organism": E.Organism()}
    for step in range(1, 9):
        grid, mono, L = E.step(grid, mono, field, gx, gy)
        assert grid[10, 49]["occupied"], f"died early at step {step}"
        assert L["deaths"] == 0 and L["births"] == 0
    assert grid[10, 49]["organism"].core_health == pytest.approx(0.02, abs=1e-9)
    grid, mono, L = E.step(grid, mono, field, gx, gy)
    assert not grid[10, 49]["occupied"]
    assert L["deaths"] == 1
    assert L["death_return"] == 5.0
    assert E.summarize(grid, mono)[0] == 0


def test_ledger_identity():
    seed_all(7)
    grid = np.empty((E.WIDTH, E.HEIGHT), dtype=object)
    mono = np.zeros((E.WIDTH, E.HEIGHT))
    field = E.make_radiation_field()
    gx, gy = E.field_gradient(field)
    grid = E.initialize_defensive_population(grid, mono)
    m_prev = mono.sum()
    for step in range(1, 51):
        grid, mono, L = E.step(grid, mono, field, gx, gy)
        m = mono.sum()
        predicted = L["injected_gross"] - L["inject_clip"] - L["diffusion_clip"] - L["birth_sink"] + L["death_return"]
        assert math.isclose(m - m_prev, predicted, abs_tol=1e-8), step
        assert L["diffusion_clip"] == 0.0          # provable for this scheme, so exact
        assert L["birth_sink"] == 15.0 * L["births"]
        assert L["death_return"] <= 5.0 * L["deaths"]
        m_prev = m


def test_alignment_is_gradient():
    field = E.make_radiation_field()
    gx, gy = E.field_gradient(field)
    org = E.Organism(radiotropism=5.0)
    x, y = 25, 25
    slots = E.cylinder_neighbors(x, y)
    w = dict(zip(slots, E.slot_weights(org, x, y, slots, gx, gy)))
    assert w[(25, 26)] > w[(25, 24)]
    assert w[(26, 25)] == 1.0 and w[(24, 25)] == 1.0          # exponent exactly 0.0
    assert math.isclose(w[(25, 26)], math.exp(0.25), rel_tol=1e-12)
    assert math.isclose(w[(26, 26)], math.exp(0.25 / math.sqrt(2)), rel_tol=1e-12)
    assert math.isclose(w[(24, 26)], w[(26, 26)], rel_tol=1e-12)


def test_seam_unwrap():
    field = E.make_radiation_field()
    gx, gy = E.field_gradient(field)
    org = E.Organism(radiotropism=5.0)
    x, y = 0, 25
    slots = E.cylinder_neighbors(x, y)
    w = dict(zip(slots, E.slot_weights(org, x, y, slots, gx, gy)))
    assert w[(49, 25)] == w[(1, 25)] == 1.0
    assert w[(49, 26)] == w[(1, 26)]
    assert math.isclose(w[(49, 26)], math.exp(0.25 / math.sqrt(2)), rel_tol=1e-12)


def test_original_never_dies():
    seed_all(1)
    grid = np.empty((O.WIDTH, O.HEIGHT), dtype=object)
    mono = np.zeros((O.WIDTH, O.HEIGHT))
    field = O.make_radiation_field()
    grid = O.initialize_defensive_population(grid, mono)
    pops = []
    for _ in range(100):
        grid, mono = O.execute_system_timestep(grid, mono, field)
        pops.append(sum(1 for x in range(O.WIDTH) for y in range(O.HEIGHT) if grid[x, y]["occupied"]))
    healths = [grid[x, y]["organism"].core_health for x in range(O.WIDTH) for y in range(O.HEIGHT) if grid[x, y]["occupied"]]
    assert all(h == 1.0 for h in healths)
    assert all(b >= a for a, b in zip(pops, pops[1:]))
