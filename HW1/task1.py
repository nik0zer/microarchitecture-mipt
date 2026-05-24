import numpy as np
import matplotlib.pyplot as plt

perf_range = np.linspace(0.01, 1.8, 500)

IPC_E, C_E = 1, 1
IPC_P, C_P = 2, 4
F_MAX = 1.8
U_MIN = 1.0

def get_power(perf, ipc, c_dyn):
    f = perf / ipc

    if f > F_MAX:
        return np.nan

    u = np.maximum(U_MIN, f + 0.2)

    return c_dyn * (u**2) * f

power_e = np.array([get_power(p, IPC_E, C_E) for p in perf_range])
power_p = np.array([get_power(p, IPC_P, C_P) for p in perf_range])

power_opt = np.fmin(np.nan_to_num(power_e, nan=1e9), power_p)

plt.figure(figsize=(10, 6))

plt.plot(perf_range, power_e, label='Efficient Core (E)', color='blue', linestyle='--', linewidth=1.5)
plt.plot(perf_range, power_p, label='Performance Core (P)', color='red', linestyle='--', linewidth=1.5)

plt.plot(perf_range, power_opt, label='Optimal Curve', color='black', linewidth=3, alpha=0.8)

plt.title('Power vs Performance for Heterogeneous Processor', fontsize=14)
plt.xlabel('Performance (Relative units)', fontsize=12)
plt.ylabel('Power (Relative units)', fontsize=12)
plt.grid(True, which='both', linestyle=':', alpha=0.5)
plt.legend()

idx = np.nanargmin(np.abs(power_e - power_p))
switch_perf = perf_range[idx]
plt.annotate(f'Switch point\nPerf ≈ {switch_perf:.2f}',
             xy=(switch_perf, power_e[idx]), xytext=(switch_perf-0.8, power_e[idx]+5),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1))

plt.xlim(0, 1.8)
plt.ylim(0, 30)
plt.show()