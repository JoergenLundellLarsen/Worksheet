
from boks import Boks

def main():
    # Dimensjoner på boksen (Lx x Ly x Lz)
    lengde_x = 5
    lengde_y = 40
    lengde_z = 5

    # Initielle tettheter (fra oppgaveteksten)
    tetthet_vaeske = 0.73
    tetthet_damp = 0.02

    # Lag boks med molekyler
    boks = Boks(lengde_x, lengde_y, lengde_z, tetthet_vaeske, tetthet_damp)
    # skille i terminal 
    tekst_skille = "----------------------------"
    print("\n",tekst_skille,"\n",tekst_skille,"\n")
    # Skriv ut hvor mange molekyler som ble laget totalt
    
    
    
    
    print(f"Totalt antall molekyler: {boks.antall_molekyler()}")
    potensiell_energi = boks.beregn_potensiell_energi()
    print("Potensiell energi: ",potensiell_energi)
    
    
    
    print("\n",tekst_skille,"\n",tekst_skille)
if __name__ == "__main__":
    main()
