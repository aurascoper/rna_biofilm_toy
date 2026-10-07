# The fixed toy. A copy of engine_original.py with exactly the changes listed in
# README.md: live-grid health, cylinder boundary, direction-cosine alignment, a measured
# mass ledger, and the diffusion assert's bound and name. Nothing else.
import math
import numpy as np
import random
import copy

WIDTH = 50
HEIGHT = 50
MAX_MONOMER_CAPACITY = 100.0
# Non-negativity bound, not CFL: with outflux = D * sum_n (c - c_n)/deg <= D * c, a cell
# can never be driven negative as long as D <= 1. (The original asserted D < 0.25, which is
# the explicit four-neighbour Laplacian bound for a different scheme.)
DIFFUSION_COEFFICIENT = 0.15
VENT_X = WIDTH // 2
VENT_Y = HEIGHT // 2
VENT_RADIUS = 5
VENT_INFLUX_RATE = 25.0
INITIAL_POPULATION_SIZE = 120
CLUSTER_SPREAD = 3
MIN_PURINE_RATIO = 0.1; MAX_PURINE_RATIO = 9.0; MUTATION_STEP_PURINE = 0.05
MIN_RADIOTROPISM = 0.0; MAX_RADIOTROPISM = 5.0; MUTATION_STEP_TROPISM = 0.1
MUTATION_RATE = 0.02
CRITICAL_REPLICATION_THRESHOLD = 15.0
DECAY_CONSTANT = 0.05
MONOMER_RECOVERY_VALUE = 5.0


class Organism:
    def __init__(self, purine_ratio=1.5, radiotropism=0.5):
        self.purine_ratio = purine_ratio
        self.radiotropism = radiotropism
        self.core_health = 1.0


def cylinder_neighbors(x, y):
    """Moore neighbours on a cylinder: x wraps, y does not. 5 on rows 0 and HEIGHT-1, else 8."""
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            ny = y + dy
            if ny < 0 or ny >= HEIGHT:
                continue
            neighbors.append(((x + dx) % WIDTH, ny))
    return neighbors


def unwrap_dx(x, tx):
    """Displacement from x to tx on the periodic x axis, folded to the shortest signed step."""
    return ((tx - x + WIDTH // 2) % WIDTH) - WIDTH // 2


def make_radiation_field():
    """Unchanged from the original: (y / HEIGHT) * 2.5, so row 0 is 0.0 and row 49 is 2.45.
    No seam exists because y does not wrap."""
    radiation_field = np.zeros((WIDTH, HEIGHT), dtype=np.float64)
    for y in range(HEIGHT):
        radiation_field[:, y] = (y / HEIGHT) * 2.5
    return radiation_field


def field_gradient(flux_map):
    """(d/dx, d/dy) of an [x, y]-indexed array. np.gradient uses one-sided differences at
    every edge and does not know x is periodic; harmless here because this field has
    d/dx == 0 exactly, wrong for any field that varies in x (use np.roll then)."""
    gx, gy = np.gradient(flux_map)
    return gx, gy


def inject_vent_monomers(monomer_grid):
    """Returns (grid, injected_gross, inject_clip). injected_gross is what the vent emits;
    inject_clip is what the capacity clamp discarded."""
    injected_gross = 0.0
    inject_clip = 0.0
    for dx in range(-VENT_RADIUS, VENT_RADIUS + 1):
        for dy in range(-VENT_RADIUS, VENT_RADIUS + 1):
            if dx**2 + dy**2 <= VENT_RADIUS**2:
                tx, ty = (VENT_X + dx) % WIDTH, (VENT_Y + dy) % HEIGHT
                before = monomer_grid[tx, ty]
                after = min(before + VENT_INFLUX_RATE, MAX_MONOMER_CAPACITY)
                injected_gross += VENT_INFLUX_RATE
                inject_clip += (before + VENT_INFLUX_RATE) - after
                monomer_grid[tx, ty] = after
    return monomer_grid, injected_gross, inject_clip


def diffuse_monomers(monomer_grid):
    """Downhill-only pairwise transfer, divide by the cell's own neighbour count. Exactly
    conservative by bookkeeping (every transfer is added to the receiver and subtracted from
    the giver). Returns (grid, diffusion_clip) where diffusion_clip = sum(pre - post) around
    the clip; provably 0.0 for this scheme (see README), kept so the ledger identity holds by
    construction rather than by geometry. Note the scheme is not self-adjoint: an edge cell
    pushes D/5 per link, an interior cell D/8. A modelling quirk, not a bug."""
    flux_delta = np.zeros_like(monomer_grid, dtype=np.float64)
    assert DIFFUSION_COEFFICIENT <= 1.0, "non-negativity bound: outflux <= D*c requires D <= 1"
    for x in range(WIDTH):
        for y in range(HEIGHT):
            curr = monomer_grid[x, y]
            if curr <= 0.0:
                continue
            neighbors = cylinder_neighbors(x, y)
            num_neighbors = len(neighbors)
            total_outflux = 0.0
            for nx, ny in neighbors:
                if curr > monomer_grid[nx, ny]:
                    gradient = curr - monomer_grid[nx, ny]
                    specific_flux = DIFFUSION_COEFFICIENT * (gradient / num_neighbors)
                    flux_delta[nx, ny] += specific_flux
                    total_outflux += specific_flux
            flux_delta[x, y] -= total_outflux
    monomer_grid += flux_delta
    pre_clip = monomer_grid.sum()
    np.clip(monomer_grid, 0.0, MAX_MONOMER_CAPACITY, out=monomer_grid)
    diffusion_clip = pre_clip - monomer_grid.sum()
    return monomer_grid, diffusion_clip


def initialize_defensive_population(grid, monomer_grid):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            grid[x, y] = {"occupied": False, "organism": None}
    monomer_grid, _, _ = inject_vent_monomers(monomer_grid)
    valid_seed_centers = [((VENT_X + dx) % WIDTH, (VENT_Y + dy) % HEIGHT) for dx in range(-2, 3) for dy in range(-2, 3)]
    seeded_count, attempts, max_attempts = 0, 0, INITIAL_POPULATION_SIZE * 20
    while seeded_count < INITIAL_POPULATION_SIZE and attempts < max_attempts:
        attempts += 1
        base_x, base_y = random.choice(valid_seed_centers)
        tx = (base_x + int(random.gauss(0, CLUSTER_SPREAD))) % WIDTH
        ty = base_y + int(random.gauss(0, CLUSTER_SPREAD))
        if ty < 0 or ty >= HEIGHT:
            # Cylinder: y does not wrap. Reject and retry (needs |gauss(0,3)| > 23 to happen).
            continue
        if not grid[tx, ty]["occupied"]:
            grid[tx, ty]["organism"] = Organism()
            grid[tx, ty]["occupied"] = True
            seeded_count += 1
    return grid


def copy_and_mutate_organism(parent_org):
    child = Organism(parent_org.purine_ratio, parent_org.radiotropism)
    if random.random() < MUTATION_RATE:
        p_shift = random.uniform(-MUTATION_STEP_PURINE, MUTATION_STEP_PURINE)
        child.purine_ratio = max(MIN_PURINE_RATIO, min(parent_org.purine_ratio + p_shift, MAX_PURINE_RATIO))
        t_shift = random.uniform(-MUTATION_STEP_TROPISM, MUTATION_STEP_TROPISM)
        child.radiotropism = max(MIN_RADIOTROPISM, min(parent_org.radiotropism + t_shift, MAX_RADIOTROPISM))
    return child


def slot_weights(org, x, y, slots, gx, gy):
    """Direction cosine: exponent = radiotropism * (unit displacement . grad flux at (x, y)).
    dx is unwrapped on the periodic x axis; dy is raw because y does not wrap. For the linear
    field a +y step gets r*0.05, a diagonal r*0.05/sqrt(2), a +-x step exactly 0. The +-20
    clamp is kept from the original although max |exponent| is now 0.25."""
    weights = []
    for tx, ty in slots:
        dx, dy = unwrap_dx(x, tx), ty - y
        norm = math.hypot(dx, dy)
        alignment = (dx * gx[x, y] + dy * gy[x, y]) / norm
        exponent = max(-20.0, min(org.radiotropism * alignment, 20.0))
        weights.append(math.exp(exponent))
    return weights


def step(grid, monomer_grid, flux_map, gx, gy):
    """One step. Returns (grid, monomer_grid, ledger). Ledger terms are measured deltas:
    M(t) - M(t-1) == injected_gross - inject_clip - diffusion_clip - birth_sink + death_return.
    death_return is the amount actually added after the capacity clamp, so the death clamp
    is folded into it rather than being a sixth term."""
    grid_snapshot = copy.deepcopy(grid)
    monomer_grid, injected_gross, inject_clip = inject_vent_monomers(monomer_grid)
    monomer_grid, diffusion_clip = diffuse_monomers(monomer_grid)
    birth_sink = 0.0
    death_return = 0.0
    births = 0
    deaths = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if not grid_snapshot[x, y]["occupied"]:
                continue
            # Live organism: damage, lysis and the parent copy all act on it. Safe because
            # births only target snapshot-empty cells and the only death at (x, y) is this one.
            org = grid[x, y]["organism"]
            local_flux = max(0.0, flux_map[x, y])
            neighbors = cylinder_neighbors(x, y)
            # Shielding reads the snapshot: newborns do not shield this step, and an organism
            # that lysed earlier this step still shields.
            shielding_points = 0.0
            for nb_x, nb_y in neighbors:
                if grid_snapshot[nb_x, nb_y]["occupied"]:
                    shielding_points += grid_snapshot[nb_x, nb_y]["organism"].purine_ratio
            kappa = org.purine_ratio * 0.25
            attenuated_flux = local_flux * np.exp(-kappa * shielding_points)
            org.core_health -= (attenuated_flux * DECAY_CONSTANT)
            if org.core_health <= 0.0:
                grid[x, y]["occupied"] = False
                grid[x, y]["organism"] = None
                before = monomer_grid[x, y]
                after = min(before + MONOMER_RECOVERY_VALUE, MAX_MONOMER_CAPACITY)
                monomer_grid[x, y] = after
                death_return += after - before
                deaths += 1
                continue
            if monomer_grid[x, y] >= CRITICAL_REPLICATION_THRESHOLD:
                # Both grids, as in the original: a cell vacated by lysis this step is still
                # occupied in the snapshot, so it is not available until the next step; the
                # live check only excludes cells filled by births earlier this step.
                empty_slots = [(nx, ny) for nx, ny in neighbors if not grid_snapshot[nx, ny]["occupied"] and not grid[nx, ny]["occupied"]]
                if len(empty_slots) > 0:
                    monomer_grid[x, y] -= CRITICAL_REPLICATION_THRESHOLD
                    birth_sink += CRITICAL_REPLICATION_THRESHOLD
                    births += 1
                    weights = slot_weights(org, x, y, empty_slots, gx, gy)
                    sum_w = sum(weights)
                    probs = [w / sum_w for w in weights] if sum_w > 0 else [1.0 / len(empty_slots)] * len(empty_slots)
                    chosen_idx = np.random.choice(len(empty_slots), p=probs)
                    tx, ty = empty_slots[chosen_idx]
                    grid[tx, ty]["organism"] = copy_and_mutate_organism(org)
                    grid[tx, ty]["occupied"] = True
    ledger = {
        "injected_gross": injected_gross,
        "inject_clip": inject_clip,
        "diffusion_clip": diffusion_clip,
        "birth_sink": birth_sink,
        "death_return": death_return,
        "births": births,
        "deaths": deaths,
    }
    return grid, monomer_grid, ledger


def empty_grid():
    grid = np.empty((WIDTH, HEIGHT), dtype=object)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            grid[x, y] = {"occupied": False, "organism": None}
    return grid


def summarize(grid, monomer_grid):
    """population, total mass, mean purine, mean radiotropism (means computed the same way)."""
    n = 0
    purine = 0.0
    tropism = 0.0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if grid[x, y]["occupied"]:
                n += 1
                purine += grid[x, y]["organism"].purine_ratio
                tropism += grid[x, y]["organism"].radiotropism
    return n, float(np.sum(monomer_grid)), (purine / n if n else 0.0), (tropism / n if n else 0.0)
