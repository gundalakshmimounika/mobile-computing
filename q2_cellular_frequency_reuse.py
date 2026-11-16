# Program 2 - Cellular layout and frequency reuse (Part A: analytical)
import numpy as np
import matplotlib.pyplot as plt

N = np.array([3, 4, 7, 9, 12])
gamma, total = 4, 336

Q = np.sqrt(3 * N)                      # co-channel reuse ratio D/R
ch = total / N                          # channels per cell
si_db = 10 * np.log10(Q ** gamma / 6)   # first-tier S/I in dB

print("\nProgram 2 - Cellular layout and frequency reuse")
print("-" * 46)
print(f"{'N':<5}{'Q=D/R':>8}{'ch/cell':>10}{'S/I (dB)':>11}")
for n, q, c, s in zip(N, Q, ch, si_db):
    print(f"{n:<5d}{q:8.2f}{c:10.1f}{s:11.2f}")

fig, ax1 = plt.subplots(figsize=(7, 4.5))
ax1.plot(N, si_db, "o-b")
ax1.set_xlabel("Cluster size N")
ax1.set_ylabel("S/I (dB)", color="b")
ax2 = ax1.twinx()
ax2.plot(N, ch, "s--r")
ax2.set_ylabel("Channels per cell", color="r")
plt.title("Capacity vs interference trade-off")
plt.tight_layout()
plt.savefig("reuse.png", dpi=150)
print("\nGraph saved as reuse.png")
plt.show()
