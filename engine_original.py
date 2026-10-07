# SPDX-License-Identifier: MIT
# LICENSING NOTE: this file transcribes machine-generated text (an LLM-written engine
# pasted into a chat on 2026-10-06). No copyright is claimed over the transcribed content,
# whose copyright status is unsettled. The restored line breaks, the added
# make_radiation_field() wrapper and this header are released under the MIT license in
# LICENSE-CODE. The rest of the repository's code is MIT; its prose, specs and data are
# CC BY 4.0 (LICENSE).
# Verbatim transcription of the pasted engine (paste id 911e, "Complete Simulation
# Engine Implementation"). Engine functions are unchanged. The paste's newlines were
# destroyed inside the constant blocks and import line; every restored line break is
# listed in TRANSCRIPTION.md. The original __main__ block is not here; run.py replaces it.
# This file carries all four defects on purpose. Do not fix anything in it.
import numpy as np
import random
import copy
# ==============================================================================
# GLOBAL ECOSYSTEM CONFIGURATION & SYSTEM CONSTANTS
# ==============================================================================
WIDTH = 50
HEIGHT = 50
MAX_MONOMER_CAPACITY = 100.0
DIFFUSION_COEFFICIENT = 0.15
# Environmental Injection Profile
VENT_X = WIDTH // 2
VENT_Y = HEIGHT // 2
VENT_RADIUS = 5
VENT_INFLUX_RATE = 25.0
# Initializer Properties
INITIAL_POPULATION_SIZE = 120
CLUSTER_SPREAD = 3
# Mutation Limits & Bounds
MIN_PURINE_RATIO = 0.1; MAX_PURINE_RATIO = 9.0; MUTATION_STEP_PURINE = 0.05
MIN_RADIOTROPISM = 0.0; MAX_RADIOTROPISM = 5.0; MUTATION_STEP_TROPISM = 0.1
MUTATION_RATE = 0.02
# Core Mechanics Thresholds
CRITICAL_REPLICATION_THRESHOLD = 15.0
DECAY_CONSTANT = 0.05
MONOMER_RECOVERY_VALUE = 5.0
# ==============================================================================
# STRUCTURAL DATA ARCHITECTURE
# ==============================================================================
class Organism:
    def __init__(self, purine_ratio=1.5, radiotropism=0.5):
        self.purine_ratio = purine_ratio
        self.radiotropism = radiotropism
        self.core_health = 1.0
def get_toroidal_moore_neighbors(x, y):
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            neighbors.append(((x + dx) % WIDTH, (y + dy) % HEIGHT))
    return neighbors
# ==============================================================================
# INDEPENDENT COMPONENT ROUTINES
# ==============================================================================
def inject_vent_monomers_toroidal(monomer_grid):
    for dx in range(-VENT_RADIUS, VENT_RADIUS + 1):
        for dy in range(-VENT_RADIUS, VENT_RADIUS + 1):
            if dx**2 + dy**2 <= VENT_RADIUS**2:
                tx, ty = (VENT_X + dx) % WIDTH, (VENT_Y + dy) % HEIGHT
                monomer_grid[tx, ty] = min(monomer_grid[tx, ty] + VENT_INFLUX_RATE, MAX_MONOMER_CAPACITY)
    return monomer_grid
def diffuse_monomers_conservative(monomer_grid):
    flux_delta = np.zeros_like(monomer_grid, dtype=np.float64)
    assert DIFFUSION_COEFFICIENT < 0.25, "CFL Stability Blown"
    
    for x in range(WIDTH):
        for y in range(HEIGHT):
            curr = monomer_grid[x, y]
            if curr <= 0.0: continue
            neighbors = get_toroidal_moore_neighbors(x, y)
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
    np.clip(monomer_grid, 0.0, MAX_MONOMER_CAPACITY, out=monomer_grid)
    return monomer_grid
def initialize_defensive_population(grid, monomer_grid):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            grid[x, y] = {"occupied": False, "organism": None}
            
    monomer_grid = inject_vent_monomers_toroidal(monomer_grid)
    valid_seed_centers = [((VENT_X + dx) % WIDTH, (VENT_Y + dy) % HEIGHT) for dx in range(-2, 3) for dy in range(-2, 3)]
    
    seeded_count, attempts, max_attempts = 0, 0, INITIAL_POPULATION_SIZE * 20
    while seeded_count < INITIAL_POPULATION_SIZE and attempts < max_attempts:
        attempts += 1
        base_x, base_y = random.choice(valid_seed_centers)
        tx = (base_x + int(random.gauss(0, CLUSTER_SPREAD))) % WIDTH
        ty = (base_y + int(random.gauss(0, CLUSTER_SPREAD))) % HEIGHT
        
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
# ==============================================================================
# FUNCTIONAL MAIN LOOP STEP ENGINE
# ==============================================================================
def execute_system_timestep(grid, monomer_grid, flux_gradient_map):
    """Updates the cellular automaton and continuous monomer maps for one step."""
    grid_snapshot = copy.deepcopy(grid)
    
    # 1. Chemical Environment Updates
    monomer_grid = inject_vent_monomers_toroidal(monomer_grid)
    monomer_grid = diffuse_monomers_conservative(monomer_grid)
    
    # 2. Biological Processing Loop
    for x in range(WIDTH):
        for y in range(HEIGHT):
            cell = grid_snapshot[x, y]
            if not cell["occupied"]:
                continue
                
            org = cell["organism"]
            local_flux = max(0.0, flux_gradient_map[x, y])
            neighbors = get_toroidal_moore_neighbors(x, y)
            
            # Defensive Shielding Step
            shielding_points = 0.0
            for nb_x, nb_y in neighbors:
                if grid_snapshot[nb_x, nb_y]["occupied"]:
                    shielding_points += grid_snapshot[nb_x, nb_y]["organism"].purine_ratio
            
            kappa = org.purine_ratio * 0.25
            attenuated_flux = local_flux * np.exp(-kappa * shielding_points)
            org.core_health -= (attenuated_flux * DECAY_CONSTANT)
            
            # Lysis Execution
            if org.core_health <= 0.0:
                grid[x, y]["occupied"] = False
                grid[x, y]["organism"] = None
                monomer_grid[x, y] = min(monomer_grid[x, y] + MONOMER_RECOVERY_VALUE, MAX_MONOMER_CAPACITY)
                continue
                
            # Metabolic Replication Step
            if monomer_grid[x, y] >= CRITICAL_REPLICATION_THRESHOLD:
                empty_slots = [(nx, ny) for nx, ny in neighbors if not grid_snapshot[nx, ny]["occupied"] and not grid[nx, ny]["occupied"]]
                
                if len(empty_slots) > 0:
                    monomer_grid[x, y] -= CRITICAL_REPLICATION_THRESHOLD
                    slot_weights = []
                    
                    for tx, ty in empty_slots:
                        dx, dy = tx - x, ty - y
                        grad_x = flux_gradient_map[tx, ty] - local_flux
                        exponent = max(-20.0, min(org.radiotropism * (dx * grad_x), 20.0))
                        slot_weights.append(np.exp(exponent))
                    
                    # Safe stochastic choice block
                    sum_w = sum(slot_weights)
                    probs = [w / sum_w for w in slot_weights] if sum_w > 0 else [1.0/len(empty_slots)]*len(empty_slots)
                    
                    chosen_idx = np.random.choice(len(empty_slots), p=probs)
                    tx, ty = empty_slots[chosen_idx]
                    
                    grid[tx, ty]["organism"] = copy_and_mutate_organism(org)
                    grid[tx, ty]["occupied"] = True
                    
    return grid, monomer_grid


def make_radiation_field():
    """The field from the original __main__ block, verbatim: increasing from top to bottom."""
    radiation_field = np.zeros((WIDTH, HEIGHT), dtype=np.float64)
    for y in range(HEIGHT):
        radiation_field[:, y] = (y / HEIGHT) * 2.5 
    return radiation_field
