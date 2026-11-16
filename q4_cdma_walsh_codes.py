# Program 4 - Multiple access techniques: CDMA with Walsh codes
import numpy as np

try:
    from scipy.linalg import hadamard
except ImportError:                      # fallback if SciPy is not installed
    def hadamard(n):
        H = np.array([[1]])
        while H.shape[0] < n:
            H = np.block([[H, H], [H, -H]])
        return H

W = hadamard(4)                          # 4 orthogonal Walsh codes (rows), +/-1
bits1 = np.array([1, -1, 1, 1])          # user 1 data (+/-1)
bits2 = np.array([-1, -1, 1, -1])        # user 2 data


def spread(bits, code):
    """Multiply each bit by the whole code."""
    return np.concatenate([b * code for b in bits])


def despread(rx, code):
    chips = rx.reshape(-1, len(code))
    return np.sign(chips @ code / len(code)).astype(int)


tx = spread(bits1, W[1]) + spread(bits2, W[2])   # channel adds the signals

print("\nProgram 4 - CDMA with Walsh codes")
print("-" * 40)
print("Walsh codes:\n", W)
print("\nTransmitted (sum) signal:", tx)
print("\nUser1 recovered:", despread(tx, W[1]), " sent:", bits1)
print("User2 recovered:", despread(tx, W[2]), " sent:", bits2)
print("Wrong code W3 correlation:", (tx.reshape(-1, 4) @ W[3]) / 4)   # all zeros

print("\nComparison of multiple access techniques")
rows = [
    ("Technique", "Resource shared", "Guard needs", "Interference", "Typical use"),
    ("FDMA", "Frequency bands", "Guard bands", "Adjacent-channel", "1G (AMPS)"),
    ("TDMA", "Time slots", "Guard time, sync", "Slot overlap", "2G GSM"),
    ("CDMA", "Codes (spread spectrum)", "None (code orthogonality)", "MAI, near-far", "IS-95, UMTS"),
    ("OFDMA", "Subcarriers and time (RBs)", "Cyclic prefix", "Inter-cell only", "4G LTE, 5G NR"),
]
widths = [max(len(r[i]) for r in rows) for i in range(5)]
for k, r in enumerate(rows):
    print("  ".join(c.ljust(w) for c, w in zip(r, widths)))
    if k == 0:
        print("  ".join("-" * w for w in widths))
