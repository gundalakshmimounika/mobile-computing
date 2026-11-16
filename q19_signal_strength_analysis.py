# Program 19 - Signal strength analysis between nodes (log-distance path loss + shadowing)
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(1)
N, AREA = 8, 200.0
Pt, PL0, n, sigma, d0, SENS = 20.0, 40.0, 3.0, 4.0, 1.0, -85.0

pos = rng.uniform(0, AREA, (N, 2))
D = np.linalg.norm(pos[:, None] - pos[None], axis=2)
R = Pt - PL0 - 10 * n * np.log10(np.maximum(D, d0) / d0) + rng.normal(0, sigma, (N, N))
R = np.triu(R, 1)
R = R + R.T                                  # symmetric shadowing
np.fill_diagonal(R, np.nan)
A = (R >= SENS).astype(int)                  # adjacency (nan -> False)

print("\nProgram 19 - Signal strength analysis")
print("-" * 40)
print("RSSI matrix (dBm):")
print(np.round(R, 1))
print("\nAdjacency matrix:")
print(A)
print("\nPath-loss exponent n :", n)
print("Average degree       :", A.sum() / N)

seen, stack = {0}, [0]                       # connectivity by graph search
while stack:
    u = stack.pop()
    for v in np.where(A[u])[0]:
        if v not in seen:
            seen.add(int(v)); stack.append(int(v))
print("Connected            :", "Yes" if len(seen) == N else "No")

# Distance at which mean RSSI (no shadowing) drops below -85 dBm
d_limit = d0 * 10 ** ((Pt - PL0 - SENS) / (10 * n))
print(f"Distance at which RSSI < {SENS:.0f} dBm : {d_limit:.1f} m")

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
iu = np.triu_indices(N, 1)
ax[0].scatter(D[iu], R[iu])
ax[0].axhline(SENS, color="r", ls="--")
ax[0].set_xlabel("Distance (m)")
ax[0].set_ylabel("RSSI (dBm)")
ax[0].set_title("RSSI vs distance")
for i in range(N):
    for j in range(i + 1, N):
        if A[i, j]:
            ax[1].plot(*zip(pos[i], pos[j]), "g-", lw=0.8)
ax[1].scatter(pos[:, 0], pos[:, 1], c="b")
for i, p in enumerate(pos):
    ax[1].annotate(str(i), p)
ax[1].set_title("Connectivity graph (RSSI >= -85 dBm)")
plt.tight_layout()
plt.savefig("rssi.png", dpi=150)
print("\nGraph saved as rssi.png")
plt.show()
