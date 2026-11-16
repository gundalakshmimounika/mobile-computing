# Program 10 - Mini project: aggregate repetitions (mean + 95% CI) and plot
# Reads results.csv with columns: config,param,run,throughput,delay
# If results.csv is not found, DEMO data is generated so the script still runs.
# Replace it with your real OMNeT++ / Simu5G results before submission.
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if os.path.exists("results.csv"):
    df = pd.read_csv("results.csv")
else:
    print("results.csv not found -> using DEMO data (replace with real results)\n")
    rng = np.random.default_rng(3)
    rows = []
    for ues in (5, 10, 20, 40, 80):
        for run in range(1, 6):
            thr = 95 * (1 - np.exp(-ues / 25)) / (1 + ues / 120) + rng.normal(0, 1.5)
            dly = 8 + 0.35 * ues + rng.normal(0, 1.0)
            rows.append(("cfg_%d" % ues, ues, run, round(thr, 3), round(dly, 3)))
    df = pd.DataFrame(rows, columns=["config", "param", "run", "throughput", "delay"])

g = df.groupby("param")["throughput"]
mean, ci = g.mean(), 1.96 * g.std() / np.sqrt(g.count())

plt.errorbar(mean.index, mean.values, yerr=ci.values, marker="o", capsize=3)
plt.xlabel("Parameter (e.g. number of UEs)")
plt.ylabel("Mean throughput (Mbps)")
plt.grid(True)
plt.savefig("mini_project.png", dpi=150)

print(df.groupby("param")[["throughput", "delay"]].agg(["mean", "std"]).round(3))
print("\nGraph saved as mini_project.png")
plt.show()
