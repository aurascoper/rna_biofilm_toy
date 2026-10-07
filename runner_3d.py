import numpy as np
from engine_3d import Engine3D
import sys
import os

# Add path to get engine.py (2D)
sys.path.append("/Users/aurascoper/Developer/rna_biofilm_toy")
import engine as E2D

def run_3d(seed, steps=100, field_scale=20.0):
    e = Engine3D(field_scale=field_scale, decay_scale=1.0, seed=seed)
    for _ in range(steps):
        obs = e.step()
    return obs

def run_2d(seed, steps=100, field_scale=20.0):
    E2D.seed_all(seed)
    grid = np.empty((E2D.WIDTH, E2D.HEIGHT), dtype=object)
    mono = np.zeros((E2D.WIDTH, E2D.HEIGHT), dtype=np.float64)
    field = E2D.make_radiation_field() * field_scale
    gx, gy = E2D.field_gradient(field)
    decay = E2D.DECAY_CONSTANT # Match decay_scale=1.0
    grid = E2D.initialize_defensive_population(grid, mono)
    for step in range(1, steps + 1):
        grid, mono, L = E2D.step(grid, mono, field, gx, gy, decay=decay)
    n, m, purine, tropism, mean_occ, index, mean_y = E2D.summarize(grid, mono)
    return {"n": n, "mean_y": mean_y, "clustering": index}

def main():
    steps = 100
    field_scale = 20.0
    
    print("Running Calibration (Seeds 1-20) for 3-D CA...")
    res_3d = {}
    for s in range(1, 21):
        res_3d[s] = run_3d(s, steps, field_scale)
        print(f"  Seed {s} 3D: {res_3d[s]}")
        
    # Calculate 3D Sham Contrasts (i vs i+10)
    diffs_mean_y = []
    diffs_cluster = []
    for i in range(1, 11):
        dy = res_3d[i]["mean_y"] - res_3d[i+10]["mean_y"]
        dc = res_3d[i]["clustering"] - res_3d[i+10]["clustering"]
        diffs_mean_y.append(dy)
        diffs_cluster.append(dc)
        
    sd_mean_y = np.std(diffs_mean_y, ddof=1)
    sd_cluster = np.std(diffs_cluster, ddof=1)
    
    floor_mean_y = 2.0 * sd_mean_y
    floor_cluster = 2.0 * sd_cluster
    
    print("\n--- 3-D CA Noise Floors ---")
    print(f"Floor mean_y: {floor_mean_y:.6f}")
    print(f"Floor clustering: {floor_cluster:.6f}")
    
    print("\nRunning Confirmatory Contrasts (Seeds 21-30) [3D vs 2D]...")
    success_mean_y = 0
    success_cluster = 0
    
    for s in range(21, 31):
        obs_3d = run_3d(s, steps, field_scale)
        obs_2d = run_2d(s, steps, field_scale)
        
        dy = obs_3d["mean_y"] - obs_2d["mean_y"]
        dc = obs_3d["clustering"] - obs_2d["clustering"]
        
        # We expect a negative shift exceeding the floor
        sig_y = (dy < 0) and (abs(dy) > floor_mean_y)
        sig_c = (dc < 0) and (abs(dc) > floor_cluster)
        
        if sig_y: success_mean_y += 1
        if sig_c: success_cluster += 1
            
        print(f"  Seed {s} | 3D_y: {obs_3d['mean_y']:.2f}, 2D_y: {obs_2d['mean_y']:.2f} | dY: {dy:.4f} (Sig: {sig_y}) | 3D_c: {obs_3d['clustering']:.4f}, 2D_c: {obs_2d['clustering']:.4f} | dC: {dc:.4f} (Sig: {sig_c})")
        
    print("\n--- Confirmation Results ---")
    print(f"mean_y dropped significantly in {success_mean_y}/10 pairs.")
    print(f"clustering dropped significantly in {success_cluster}/10 pairs.")

if __name__ == '__main__':
    main()
