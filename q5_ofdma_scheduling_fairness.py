# Program 5 - OFDMA scheduling and fairness (Jain's fairness index)
# Usage:
#   python q5_ofdma_scheduling_fairness.py                 -> built-in Python model of DRR / PF / Max C/I
#   python q5_ofdma_scheduling_fairness.py 3.2 2.9 2.5 ... -> Jain index for your own per-UE throughputs
import sys
import numpy as np


def jain(x):
    x = np.asarray(x, dtype=float)
    return x.sum() ** 2 / (len(x) * (x ** 2).sum())


def run_scheduler(policy, rate, slots=20000, beta=0.01, seed=1):
    """Per-slot downlink scheduling of one resource unit among UEs (saturated traffic)."""
    rng = np.random.default_rng(seed)
    n = len(rate)
    served = np.zeros(n)                 # total bits served
    avg = np.full(n, 1e-6)               # PF average throughput
    for s in range(slots):
        inst = rate * rng.exponential(1.0, n)      # instantaneous rate (fading)
        if policy == "DRR":
            u = s % n                                # round robin
        elif policy == "MAXCI":
            u = int(np.argmax(inst))                 # best channel wins
        else:                                        # "PF"
            u = int(np.argmax(inst / avg))
        served[u] += inst[u]
        got = np.zeros(n); got[u] = inst[u]
        avg = (1 - beta) * avg + beta * got
    return served / slots


if len(sys.argv) > 1:
    x = [float(v) for v in sys.argv[1:]]
    print(f"Total = {sum(x):.2f}   Jain index = {jain(x):.3f}")
    sys.exit()

# UE1..UE5 at increasing distance -> decreasing mean channel rate (Mbps)
rate = np.array([30.0, 22.0, 15.0, 9.0, 4.0])

print("\nProgram 5 - OFDMA scheduling and fairness (5 UEs, saturated downlink)")
print("-" * 76)
print(f"{'Scheduler':<10}" + "".join(f"{'UE'+str(i+1):>8}" for i in range(5)) + f"{'Total':>9}{'Fairness':>10}")
res = {}
for name, key in [("DRR", "DRR"), ("PF", "PF"), ("Max C/I", "MAXCI")]:
    x = run_scheduler(key, rate)
    res[name] = x
    print(f"{name:<10}" + "".join(f"{v:8.2f}" for v in x) + f"{x.sum():9.2f}{jain(x):10.3f}")

best = max(res, key=lambda k: res[k].sum())
fair = max(res, key=lambda k: jain(res[k]))
print(f"\nHighest total throughput : {best}")
print(f"Fairest scheduler        : {fair}")
