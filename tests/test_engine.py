# SPDX-License-Identifier: MIT
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


# ---- round 2.1: spatial observables, scales. Every numeric band below was MEASURED on
# 2026-10-06 with the code as committed, not chosen; the measurement script is described in
# README.md. A band is mean +- 4 sd of the measured distribution.


def grid_from(pred):
    g = E.empty_grid()
    for x in range(E.WIDTH):
        for y in range(E.HEIGHT):
            if pred(x, y):
                g[x, y] = {"occupied": True, "organism": E.Organism()}
    return g


def observables(g):
    return E.summarize(g, np.zeros((E.WIDTH, E.HEIGHT)))[4:]   # mean_occ, index, mean_y


def test_clustering_index_random_scatter():
    rng = random.Random(12345)
    cells = set(rng.sample(range(E.WIDTH * E.HEIGHT), 300))
    mean_occ, index, mean_y = observables(grid_from(lambda x, y: (x * E.HEIGHT + y) in cells))
    assert mean_occ == 0.98
    assert math.isclose(index, 1.0420740892031966, rel_tol=1e-9)          # this seed's value
    # 200 replicates measured: mean 0.996150, sd 0.071780, min 0.825206, max 1.169675
    assert 0.7090 < index < 1.2833                                         # mean +- 4 sd
    # CONTROL: a solid 20x15 block of the same 300 is far outside that band.
    mean_occ, index, mean_y = observables(grid_from(lambda x, y: 10 <= x < 30 and 20 <= y < 35))
    assert math.isclose(index, 7.640476588628763, rel_tol=1e-9)
    assert index > 5.0 and mean_y == 27.0


def test_index_is_N_dependent():
    # At fixed shape the index falls like ~2499/N: this is the confound that makes an
    # unmatched comparison between arms manufacture the predicted sign.
    expected = {3: 12.578859060402685, 6: 7.313127090301004, 10: 4.632414829659319, 20: 2.4076951951951955}
    for h, exp_index in expected.items():
        mean_occ, index, _ = observables(grid_from(lambda x, y, h=h: 20 <= y < 20 + h))
        assert mean_occ == 8 - 6 / h
        assert math.isclose(index, exp_index, rel_tol=1e-9)
    assert expected[3] > 5 * expected[20]                                  # factor >5, no shape change


def test_clustering_index_edge_rows():
    # The expectation uses each occupied site's own available degree, so a block on the
    # edge rows and the same block inside differ only through which rows are occupied:
    # the ratio is 1.03896 for a 50-column block AND for a 20-column block.
    pairs = {}
    for xs in ((0, 50), (0, 20)):
        a = observables(grid_from(lambda x, y, xs=xs: xs[0] <= x < xs[1] and 0 <= y < 10))[1]
        b = observables(grid_from(lambda x, y, xs=xs: xs[0] <= x < xs[1] and 20 <= y < 30))[1]
        pairs[xs] = a / b
    assert math.isclose(pairs[(0, 50)], 1.0389610389610389, rel_tol=1e-9)
    assert math.isclose(pairs[(0, 20)], pairs[(0, 50)], rel_tol=1e-9)
    mean_occ, index, mean_y = observables(grid_from(lambda x, y: (x, y) == (5, 5)))
    assert mean_occ == 0.0 and math.isnan(index) and mean_y == 5.0


def test_mean_y():
    assert observables(grid_from(lambda x, y: 10 <= y < 20))[2] == 14.5
    # Null arm (field 0, decay 0), 30 steps, seed 3: births are unbiased, so mean_y stays
    # near the seeding centre. Measured over seeds 1-10: mean 24.9846, sd 0.1118,
    # min 24.8075, max 25.1292.
    seed_all(3)
    field = E.make_radiation_field() * 0.0
    gx, gy = E.field_gradient(field)
    grid = np.empty((E.WIDTH, E.HEIGHT), dtype=object)
    mono = np.zeros((E.WIDTH, E.HEIGHT))
    grid = E.initialize_defensive_population(grid, mono)
    for _ in range(30):
        grid, mono, L = E.step(grid, mono, field, gx, gy, decay=0.0)
    mean_y = E.summarize(grid, mono)[6]
    assert 24.9846 - 4 * 0.1118 < mean_y < 24.9846 + 4 * 0.1118


def test_field_scale_zero_is_a_null():
    field0 = E.make_radiation_field() * 0.0
    gx, gy = E.field_gradient(field0)
    org = E.Organism(radiotropism=5.0)
    assert set(E.slot_weights(org, 25, 25, E.cylinder_neighbors(25, 25), gx, gy)) == {1.0}
    seed_all(5)
    grid = np.empty((E.WIDTH, E.HEIGHT), dtype=object)
    mono = np.zeros((E.WIDTH, E.HEIGHT))
    grid = E.initialize_defensive_population(grid, mono)
    for _ in range(20):
        grid, mono, L = E.step(grid, mono, field0, gx, gy)
        assert L["deaths"] == 0
    # CONTROL: scale 4 reaches the damage path. Top-row lone organism: 0.49/step,
    # alive after step 2 (0.02), dead at step 3.
    field4 = E.make_radiation_field() * 4.0
    g4x, g4y = E.field_gradient(field4)
    grid = E.empty_grid()
    mono = np.zeros((E.WIDTH, E.HEIGHT))
    grid[10, 49] = {"occupied": True, "organism": E.Organism()}
    for step in range(1, 3):
        grid, mono, L = E.step(grid, mono, field4, g4x, g4y)
        assert grid[10, 49]["occupied"]
    assert grid[10, 49]["organism"].core_health == pytest.approx(0.02, abs=1e-9)
    grid, mono, L = E.step(grid, mono, field4, g4x, g4y)
    assert not grid[10, 49]["occupied"] and L["deaths"] == 1


def test_decay_scale_isolates_damage():
    # field 1 / decay 0: the gradient is present (weights not all 1) and damage is off.
    field = E.make_radiation_field()
    gx, gy = E.field_gradient(field)
    org = E.Organism(radiotropism=5.0)
    assert not all(w == 1.0 for w in E.slot_weights(org, 25, 25, E.cylinder_neighbors(25, 25), gx, gy))
    seed_all(5)
    grid = np.empty((E.WIDTH, E.HEIGHT), dtype=object)
    mono = np.zeros((E.WIDTH, E.HEIGHT))
    grid = E.initialize_defensive_population(grid, mono)
    for _ in range(20):
        grid, mono, L = E.step(grid, mono, field, gx, gy, decay=0.0)
        assert L["deaths"] == 0
    # CONTROL: the default decay reproduces the round-1 seed-1 counts.
    seed_all(1)
    grid = np.empty((E.WIDTH, E.HEIGHT), dtype=object)
    mono = np.zeros((E.WIDTH, E.HEIGHT))
    grid = E.initialize_defensive_population(grid, mono)
    births = deaths = 0
    for _ in range(100):
        grid, mono, L = E.step(grid, mono, field, gx, gy)
        births += L["births"]
        deaths += L["deaths"]
    assert (E.summarize(grid, mono)[0], births, deaths) == (293, 184, 11)
