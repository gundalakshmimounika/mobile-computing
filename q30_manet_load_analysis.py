# Program 30 - Performance analysis of a MANET under varying network loads (analyse.py)
# Reads results.csv produced by run_loads.sh (ns-3):  rate,tx,rx,pdr,delay_ms,thr_kbps,run
# If results.csv is not found, DEMO data is generated so the script still runs.
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if os.path.exists("results.csv"):
    df = pd.read_csv("results.csv")
else:
    print("results.csv not found -> using DEMO data (replace with real ns-3 results)\n")
    rng = np.random.default_rng(5)
    rows = []
    for load in (64, 128, 256, 512, 1024, 2048):
        for run in range(1, 6):
            tx = 4 * load * 10
            pdr = max(30, 99 - 0.00001 * load ** 2 - 0.01 * load + rng.normal(0, 1.2))
            rx = int(tx * pdr / 100)
            delay = 12 + 0.00009 * load ** 2 + rng.normal(0, 1.5)
            thr = min(4 * load * pdr / 100, 1500 + rng.normal(0, 25))
            rows.append((f"{load}kbps", tx, rx, round(pdr, 2), round(delay, 2), round(thr, 2), run))
    df = pd.DataFrame(rows, columns=["rate", "tx", "rx", "pdr", "delay_ms", "thr_kbps", "run"])

df["load"] = df["rate"].str.replace("kbps", "").astype(int)
m = df.groupby("load")[["pdr", "delay_ms", "thr_kbps"]].mean()
print(m.round(2))

fig, ax = plt.subplots(1, 3, figsize=(12, 3.6))
for a, col, lab in zip(ax, m.columns, ["PDR (%)", "Delay (ms)", "Throughput (kbps)"]):
    a.plot(m.index, m[col], "o-")
    a.set_xscale("log", base=2)
    a.set_xlabel("Offered load per flow (kbps)")
    a.set_ylabel(lab)
    a.grid(True)
plt.tight_layout()
plt.savefig("manet_load.png", dpi=150)
print("\nGraph saved as manet_load.png")
plt.show()
