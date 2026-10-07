Transcription record for engine_original.py.

Source: the paste with id 911e ("Complete Simulation Engine Implementation" section),
preserved at
`~/.claude/projects/-Users-aurascoper/1b6536a8-4e77-4f27-b506-038b657a9f3f/tool-results/bn4ei4bzq.txt`
lines 471-652. The paste's newlines were destroyed wherever a comment or a constant
assignment sat at column 0 and was followed by another column-0 line. A transcription
is therefore a set of decisions. These are the decisions.

Restored line breaks, 32 in all.

Each row is `fragment as pasted` -> `lines as written`. Nothing else in the engine
functions was changed; indentation inside functions survived the paste intact.

| # | fragment as pasted | restored as |
|---|---|---|
| 1-2 | `import numpy as npimport randomimport copy` | three import lines |
| 3-5 | `# ====# GLOBAL ECOSYSTEM CONFIGURATION & SYSTEM CONSTANTS# ====WIDTH = 50` | banner / title / banner / `WIDTH = 50` |
| 6-8 | `WIDTH = 50HEIGHT = 50MAX_MONOMER_CAPACITY = 100.0DIFFUSION_COEFFICIENT = 0.15` | four assignments |
| 9-12 | `# Environmental Injection ProfileVENT_X = WIDTH // 2VENT_Y = HEIGHT // 2VENT_RADIUS = 5VENT_INFLUX_RATE = 25.0` | comment + four assignments |
| 13-14 | `# Initializer PropertiesINITIAL_POPULATION_SIZE = 120CLUSTER_SPREAD = 3` | comment + two assignments |
| 15-17 | `# Mutation Limits & BoundsMIN_PURINE_RATIO = 0.1; MAX_PURINE_RATIO = 9.0; MUTATION_STEP_PURINE = 0.05MIN_RADIOTROPISM = 0.0; MAX_RADIOTROPISM = 5.0; MUTATION_STEP_TROPISM = 0.1MUTATION_RATE = 0.02` | comment + three lines. The semicolons are genuine (`0.1; MAX_`, `9.0; MUTATION_`, `0.0; MAX_`, `5.0; MUTATION_`) and were kept; only the joins at `0.05MIN_` and `0.1MUTATION_` were broken |
| 18-20 | `# Core Mechanics ThresholdsCRITICAL_REPLICATION_THRESHOLD = 15.0DECAY_CONSTANT = 0.05MONOMER_RECOVERY_VALUE = 5.0` | comment + three assignments |
| 21-23 | `# ====# STRUCTURAL DATA ARCHITECTURE# ====class Organism:` | banner / title / banner / `class Organism:` |
| 24-26 | `# ====# INDEPENDENT COMPONENT ROUTINES# ====def inject_vent_monomers_toroidal(monomer_grid):` | banner / title / banner / def |
| 27-29 | `# ====# FUNCTIONAL MAIN LOOP STEP ENGINE# ====def execute_system_timestep(grid, monomer_grid, flux_gradient_map):` | banner / title / banner / def |
| 30-32 | `# ====# EXECUTIVE RUNTIME & REAL-TIME LOGGER TERMINAL# ====if __name__ == "__main__":` | the `__main__` block is not transcribed (see below); the three breaks are listed for completeness |

Blank lines between top-level blocks are unrecoverable from the paste and were not
guessed; the file has none between top-level definitions, as the paste has none.

What was dropped and what was added.

- Dropped: the `if __name__ == "__main__":` block (grid allocation, the radiation field
  loop, the 100-step loop, the console logger, the extinction circuit-breaker). `run.py`
  replaces it with a seeded runner and a CSV writer.
- Added: `make_radiation_field()`, which is the field loop from that block
  (`radiation_field[:, y] = (y / HEIGHT) * 2.5`, trailing space on that line kept) wrapped
  in a function so the runner and the tests can call it. It is the only function in the
  file that was not in the paste as a function.
- Added: the header comment at the top of the file.

Defects carried on purpose.

1. Health is decremented on the deep-copied snapshot organism; the live grid is never
   decremented, so lysis is unreachable.
2. Alignment is `dx * (flux[target] - flux[here])` for a field that varies only in y.
3. Injection and the death return are clamped at 100 with no record of what the clamp
   discarded; there is no mass ledger.
4. `dx = tx - x` is not unwrapped at the x seam, so a seam-crossing slot has `dx = +-49`,
   the exponent hits the +-20 clamp, and the move gets weight `e^20`. Harmless in the CSV
   run only because the colony never reaches the seam in 100 steps.
