import matplotlib.pyplot as plt
from src.ljts.boks import Box

def main():
    length_x = 5
    length_y = 40
    length_z = 5
    density_liquid = 0.73
    density_vapor = 0.02

    box = Box (length_x, length_y, length_z, density_liquid, density_vapor)

    initial_energy = box.compute_potential_energy()
    print(f"Potential energy FØR MC: {initial_energy:.6f}")

    N = box.get_molecule_count()
    b = 1.0 / 8
    T = 0.8  
    sweeps = 50
    log_interval = 1

    energy_history = [initial_energy]
    accept_total = 0

    # --- Live plot setup ---
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot(energy_history)
    ax.set_xlabel("Sweep")
    ax.set_ylabel("Potensiell energi")
    ax.set_title("Live plot av potensiell energi")
    ax.set_ylim(-1000,5000)

    for sweep in range(1, sweeps+1):
        accept = box.mc_sweep(b, T)
        accept_total += accept
        if sweep % log_interval == 0:
            curr_energy = box.compute_potential_energy()
            energy_history.append(curr_energy)
            print(f"Sweep {sweep}: Pot.energy = {curr_energy:.6f}")
            # --- Live plot update ---
            line.set_data(range(len(energy_history)), energy_history)
            ax.relim()
            ax.autoscale_view()
            plt.draw()
            plt.pause(0.01)

    plt.ioff()
    plt.show()

    accept_rate = accept_total / (sweeps * N)
    print(f"\nAcceptance ratio: {accept_rate:.3f}")

if __name__ == "__main__":
    main()

