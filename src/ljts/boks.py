import random
from src.ljts.Molecule import Molecule

class Box:

    def __init__(self, length_x, length_y, length_z, density_liquid, density_vapor):
        self._lx = length_x
        self._ly = length_y
        self._lz = length_z
        self._density_liquid = density_liquid
        self._density_vapor = density_vapor
        self._molecules = []

        self._fill_box()

    def _fill_box(self):
        """
        Fills the box with molecules along the y axis:
        40% vapor, 20% liquid, 40% vapor.
        """

        # Define y-boundaries of the compartments
        y_bottom = 0
        y_liquid_start = self._ly * 0.4
        y_liquid_end = self._ly * 0.6
        y_top = self._ly

        # Calculate volumes
        volume_liquid = self._lx * (y_liquid_end - y_liquid_start) * self._lz
        volume_vapor_single = self._lx * (y_liquid_start - y_bottom) * self._lz  # one vapor region

        # Compute number of molecules
        num_liquid = round(self._density_liquid * volume_liquid)
        num_vapor_total = round(self._density_vapor * volume_vapor_single * 2)  # two vapor regions

        # Generate molecules for each volume
        self._molecules += self._generate_molecules(num_vapor_total // 2, y_bottom, y_liquid_start)
        self._molecules += self._generate_molecules(num_liquid, y_liquid_start, y_liquid_end)
        self._molecules += self._generate_molecules(num_vapor_total // 2, y_liquid_end, y_top)

    def _generate_molecules(self, count, y_min, y_max):
        """
        Return a list of molecules randomly distributed in the box between y_min and y_max.
        """
        new_molecules = []
        for _ in range(count):
            x = random.uniform(0, self._lx)
            y = random.uniform(y_min, y_max)
            z = random.uniform(0, self._lz)
            new_molecules.append(Molecule(x, y, z))
        return new_molecules

    def get_molecule_count(self):
        return len(self._molecules)

    def compute_potential_energy(self):
        """
        Calculates the total potential energy of the system.
        """
        total_energy = 0.0
        cutoff = 2.5
        cutoff_squared = cutoff ** 2 
        shift_value = 0.01631689  # Energy shift to make potential zero at cutoff

        num_molecules = len(self._molecules)

        for i in range(num_molecules):
            mol_i = self._molecules[i]

            for j in range(i + 1, num_molecules):
                mol_j = self._molecules[j]

                # Difference between molecules in all directions
                dx = mol_i._x - mol_j._x
                dy = mol_i._y - mol_j._y
                dz = mol_i._z - mol_j._z

                # Apply minimum image convention
                dx -= round(dx / self._lx) * self._lx
                dy -= round(dy / self._ly) * self._ly
                dz -= round(dz / self._lz) * self._lz

                # Compute squared distance
                r_squared = dx * dx + dy * dy + dz * dz

                if r_squared < cutoff_squared:
                    # LJ potential: u_LJ(r) = 4 * (1/r^12 - 1/r^6)
                    inv_r2 = 1.0 / r_squared
                    inv_r6 = inv_r2 ** 3
                    inv_r12 = inv_r6 ** 2

                    energy_ij = 4 * (inv_r12 - inv_r6) + shift_value
                    total_energy += energy_ij

        return total_energy
