from src.ljts.boks import Box

def main():
    length_x = 5
    length_y = 40
    length_z = 5

    #densities
    density_liquid = 0.73
    density_vapor = 0.02

    #Creates a box
    box = Box(length_x, length_y, length_z, density_liquid, density_vapor)

    #for easier visibility in the terminal 
    divider = "----------------------------"
    print("\n", divider, "\n", divider, "\n")

    print(f"Total number of molecules: {box.get_molecule_count()}")

    potential_energy = box.compute_potential_energy()
    
    print("Potential energy: ", potential_energy)

    print("\n", divider, "\n", divider)

if __name__ == "__main__":
    main()
