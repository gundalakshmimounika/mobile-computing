# Program 22 - Latency trends in a simulated mobile network
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def simulate(seed=7, T=300, base=45.0):
    rng = np.random.default_rng(seed)
    t = np.arange(T)
    lat = base + 15 * np.sin(2 * np.pi * t / 120) + rng.gamma(2.0, 3.0, T)
    for h in (80, 160, 240):                 # handover interruptions
        lat[h:h + 3] += 120
    lat[rng.random(T) < 0.01] = np.nan       # packet loss
    return pd.Series(lat, index=t, name="latency_ms")


def from_ping(path):                         # parse "time=23.4 ms"
    vals = [float(m.group(1)) for l in open(path)
            if (m := re.search(r"time=([\d.]+)", l))]
    return pd.Series(vals, name="latency_ms")


s = simulate()                               # or: s = from_ping("ping.log")
roll = s.rolling(10, min_periods=1)

print("\nProgram 22 - Latency trends")
print("-" * 36)
print(f"Mean latency   = {s.mean():.1f} ms")
print(f"Median latency = {s.median():.1f} ms")
print(f"95th percentile= {s.quantile(0.95):.1f} ms")
print(f"Jitter         = {s.diff().abs().mean():.1f} ms")
print(f"Packet loss    = {100 * s.isna().mean():.1f} %")
for h in (80, 160, 240):
    print(f"Latency at handover t={h}s = {s.iloc[h:h + 3].max():.1f} ms")

plt.figure(figsize=(9, 4))
plt.plot(s.index, s, lw=0.6, label="Latency sample")
plt.plot(s.index, roll.mean(), "r", label="10 s moving average")
plt.xlabel("Time (s)")
plt.ylabel("Latency (ms)")
plt.legend()
plt.title("Latency trend")
plt.tight_layout()
plt.savefig("latency.png", dpi=150)
print("\nGraph saved as latency.png")
plt.show()
