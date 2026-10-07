import numpy as np

class Engine3D:
    def __init__(self, size=40, field_scale=20.0, decay_scale=1.0, seed=None):
        if seed is not None:
            np.random.seed(seed)
            
        self.X, self.Y, self.Z = size, size, size
        self.registry = np.zeros((self.X, self.Y, self.Z), dtype=np.int32)
        
        center_x, center_y = self.X // 2, self.Y // 2
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                self.registry[center_x+dx, center_y+dy, 0] = 1
        
        self.purines = np.zeros((self.X, self.Y, self.Z), dtype=np.float32)
        self.purines[self.registry == 1] = 1.0 
        
        self.monomers = np.ones((self.X, self.Y, self.Z), dtype=np.float32) * 5.0
        self.field_scale = field_scale
        self.decay_scale = decay_scale
        
        self.k_shield = 0.25
        self.gamma_decay = 0.05
        self.diffusion_rate = 0.1
        
        self.neighbors_26 = [
            (dx, dy, dz)
            for dx in [-1, 0, 1] for dy in [-1, 0, 1] for dz in [-1, 0, 1]
            if not (dx == 0 and dy == 0 and dz == 0)
        ]
        
        self.z_indices = np.arange(self.Z).reshape(1, 1, self.Z)
        self.field = np.ones((self.X, self.Y, self.Z)) * (self.Z - self.z_indices) / self.Z * self.field_scale

    def _diffuse_monomers(self):
        laplacian = (
            np.roll(self.monomers, 1, axis=0) + np.roll(self.monomers, -1, axis=0) +
            np.roll(self.monomers, 1, axis=1) + np.roll(self.monomers, -1, axis=1) +
            np.roll(self.monomers, 1, axis=2) + np.roll(self.monomers, -1, axis=2) -
            6.0 * self.monomers
        )
        self.monomers += self.diffusion_rate * laplacian
        self.monomers[:, :, 0] += 0.5

    def _calculate_shielding(self):
        S_matrix = np.zeros_like(self.purines)
        for dx, dy, dz in self.neighbors_26:
            S_matrix += np.roll(self.purines, shift=(dx, dy, dz), axis=(0, 1, 2))
        return S_matrix

    def _replicate_with_thermodynamics(self):
        base_birth_sink = 1.0 
        active_indices = np.argwhere(self.registry == 1)
        if len(active_indices) == 0:
            return
            
        np.random.shuffle(active_indices)
        
        # Pre-generate random choices to avoid loop overhead
        n_active = len(active_indices)
        choices = np.random.randint(0, 26, size=n_active)
        mutations = np.random.normal(0, 0.05, size=n_active)
        
        for i in range(n_active):
            x, y, z = active_indices[i]
            dx, dy, dz = self.neighbors_26[choices[i]]
            nx, ny, nz = x + dx, y + dy, z + dz
            
            if not (0 <= nx < self.X and 0 <= ny < self.Y and 0 <= nz < self.Z):
                continue
            if self.registry[nx, ny, nz] != 0:
                continue
                
            r_squared = dx**2 + dy**2 + dz**2
            metabolic_cost = base_birth_sink * r_squared
            
            if self.monomers[nx, ny, nz] >= metabolic_cost: # using target site monomers
                self.monomers[nx, ny, nz] -= metabolic_cost
                self.registry[nx, ny, nz] = 1
                new_purine = max(0.0, min(1.0, self.purines[x, y, z] + mutations[i]))
                self.purines[nx, ny, nz] = new_purine

    def step(self):
        self._diffuse_monomers()
        S = self._calculate_shielding()
        
        damage = self.field * np.exp(-self.k_shield * self.purines * S) * self.decay_scale * self.gamma_decay
        
        mortality_mask = (self.registry == 1) & (np.random.random((self.X, self.Y, self.Z)) < damage)
        self.registry[mortality_mask] = 0
        self.purines[mortality_mask] = 0.0
        
        self._replicate_with_thermodynamics()
        
        pop = np.sum(self.registry)
        if pop > 0:
            z_coords = np.argwhere(self.registry == 1)[:, 2]
            mean_y = np.mean(z_coords)
            
            S_occ = np.zeros_like(self.registry)
            for dx, dy, dz in self.neighbors_26:
                S_occ += np.roll(self.registry, shift=(dx, dy, dz), axis=(0, 1, 2))
            mean_occ = np.mean(S_occ[self.registry == 1])
        else:
            mean_y = 0.0
            mean_occ = 0.0
            
        return {"n": pop, "mean_y": mean_y, "clustering": mean_occ}
