import random
from Molecule import Molecule

class Box:

    def __init__(self, length_x, length_y, length_z, density_liquid, density_vapor):
        self.lx = length_x
        self.ly = length_y
        self.lz = length_z
        self.density_liquid = density_liquid
        self.density_vapor = density_vapor
        self.molecules = []

        self._fill_box()

    def _fill_box(self):
        """
        Fills the box with molecules along the y axis:
        40% vapor, 20% liquid, 40% vapor.
        """

        # Define y-boundaries of the compartments
        y_bottom = 0
        y_liquid_start = self.ly * 0.4
        y_liquid_end = self.ly * 0.6
        y_top = self.ly

        # Calculate volumes
        volume_liquid = self.lx * (y_liquid_end - y_liquid_start) * self.lz
        volume_vapor_single = self.lx * (y_liquid_start - y_bottom) * self.lz  # one vapor region

        # Compute number of molecule
        num_liquid = int(self.density_liquid * volume_liquid)
        num_vapor_total = int(self.density_vapor * volume_vapor_single * 2)  # two vapor regions

        # Generate molecules for each volume
        self.molecules += self._generate_molecules(num_vapor_total // 2, y_bottom, y_liquid_start) #// for integer divisjon
        self.molecules += self._generate_molecules(num_liquid, y_liquid_start, y_liquid_end)
        self.molecules += self._generate_molecules(num_vapor_total // 2, y_liquid_end, y_top)

    def _generate_molecules(self, count, y_min, y_max):
        """
        retrn a list of molecules randomly distributed within y axis.
        """
        new_molecules = []
        for _ in range(count):
            x = random.uniform(0, self.lx)
            y = random.uniform(y_min, y_max)
            z = random.uniform(0, self.lz)
            new_molecules.append(Molecule(x, y, z))
        return new_molecules

    def get_molecule_count(self):
        return len(self.molecules)

    def compute_potential_energy(self):
        """
        Calculates the total potential energy of the system
        """
        total_energy = 0.0
        cutoff = 2.5
        cutoff_squared = cutoff ** 2 
        shift_value = 0.01631689  #LJ value r = 2.5

        num_molecules = len(self.molecules)

        for i in range(num_molecules):
            mol_i = self.molecules[i]

            for j in range(i + 1, num_molecules):
                mol_j = self.molecules[j]

                #difference between molecules in all directions
                dx = mol_i.x - mol_j.x
                dy = mol_i.y - mol_j.y
                dz = mol_i.z - mol_j.z

                # Apply minimum image convention -> not to sure if we need this #######
                dx -= round(dx / self.lx) * self.lx
                dy -= round(dy / self.ly) * self.ly
                dz -= round(dz / self.lz) * self.lz

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
