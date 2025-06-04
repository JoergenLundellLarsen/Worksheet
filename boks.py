
# src/ljts/box.py
import random
from Molecule import Molecule

class Boks:
    """
    Representerer en boks med molekyler fordelt i væske- og dampfaser.
    Inkluderer periodiske randbetingelser (implisitt).
    """
    def __init__(self, lengde_x, lengde_y, lengde_z, tetthet_vaeske, tetthet_damp):
        self.lx = lengde_x
        self.ly = lengde_y
        self.lz = lengde_z
        self.tetthet_vaeske = tetthet_vaeske
        self.tetthet_damp = tetthet_damp
        self.molekyler = []

        self._fyll_boks()

    def _fyll_boks(self):
        """
        Fyller boksen med molekyler basert på fasedelt y-akse:
        40% damp (bunn), 20% væske (midten), 40% damp (topp).
        """

        # Grenser mellom fasene langs y-aksen
        y_bunn = 0
        y_vaeske_start = self.ly * 0.4
        y_vaeske_slutt = self.ly * 0.6
        y_topp = self.ly

        # Volum av væske- og dampfaser
        volum_vaeske = self.lx * (y_vaeske_slutt - y_vaeske_start) * self.lz
        volum_damp_enkel = self.lx * (y_vaeske_start - y_bunn) * self.lz  # én dampfase

        # Antall molekyler basert på tetthet og volum
        antall_vaeske = int(self.tetthet_vaeske * volum_vaeske)
        antall_damp_total = int(self.tetthet_damp * volum_damp_enkel * 2)  # to dampfaser

        # Fyll molekyler i hver fase
        self.molekyler += self._generer_molekyler(antall_damp_total // 2, y_bunn, y_vaeske_start)
        self.molekyler += self._generer_molekyler(antall_vaeske, y_vaeske_start, y_vaeske_slutt)
        self.molekyler += self._generer_molekyler(antall_damp_total // 2, y_vaeske_slutt, y_topp)

    def _generer_molekyler(self, antall, y_min, y_maks):
        """
        Lager en liste med molekyler fordelt tilfeldig innenfor angitt y-område.
        """
        nye_molekyler = []
        for _ in range(antall):
            x = random.uniform(0, self.lx)
            y = random.uniform(y_min, y_maks)
            z = random.uniform(0, self.lz)
            nye_molekyler.append(Molecule(x, y, z))
        return nye_molekyler

    def antall_molekyler(self):
        return len(self.molekyler)
    
    def beregn_potensiell_energi(self):
        """
        Beregner total potensiell energi i boksen basert på Lennard-Jones
        truncated-shifted (LJTS) potensialet mellom alle molekylpar.
        """
        total_energi = 0.0                  # Akkumulert total energi
        cutoff_avstand = 2.5
        cutoff_r2 = cutoff_avstand ** 2    # Bruk r^2 for å unngå unødvendige kvadratrøtter
        potensial_shift = 0.01631689       # u_LJ(2.5) for å gjøre potensialet glatt ved cutoff

        antall_molekyler = len(self.molekyler)

        for indeks_i in range(antall_molekyler):
            mol_i = self.molekyler[indeks_i]

            for indeks_j in range(indeks_i + 1, antall_molekyler):
                mol_j = self.molekyler[indeks_j]

                # Beregn forskyvning mellom molekylene i hver retning, sjekker hver eneste molekyl indeks i mot hver eneste molekyl ideks j + 1
                dx = mol_i.x - mol_j.x
                dy = mol_i.y - mol_j.y
                dz = mol_i.z - mol_j.z

                # Periodiske randbetingelser (minimum image convention) finner korteste avstand selvom de er "langt unna hverandre" men nærme hver sin kant
                dx -= round(dx / self.lx) * self.lx
                dy -= round(dy / self.ly) * self.ly
                dz -= round(dz / self.lz) * self.lz

                # Beregn kvadrert avstand
                avstand_r2 = dx * dx + dy * dy + dz * dz

                if avstand_r2 < cutoff_r2:
                    # Lennard-Jones potensial: u_LJ(r) = 4 * (1/r^12 - 1/r^6)
                    invers_r2 = 1.0 / avstand_r2
                    invers_r6 = invers_r2 ** 3
                    invers_r12 = invers_r6 ** 2

                    energi_ij = 4 * (invers_r12 - invers_r6) + potensial_shift
                    total_energi += energi_ij

        return total_energi
