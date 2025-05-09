import subprocess
import matplotlib
matplotlib.use('TkAgg')  # Use an interactive backend

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

bitrates_bps = [
    0, 722528, 1570420, 3916672, 5682848, 5243308,
    3092480, 5586360, 6627700, 6101048, 5180788,
    4282992, 1138688, 4755456, 3848380, 741400,
    0, 845540, 1892248, 1985580, 3598228,
    4127328, 4950016
]
bitrates_bps = [b * 2 for b in bitrates_bps]

iface = "eno1"
times = []
rates_mbps = []

fig, ax = plt.subplots()

def apply_rate(rate_bps):
    subprocess.run(f"tc qdisc change dev {iface} root netem rate {rate_bps}bit", shell=True)
    print(f"{rate_bps} bps ({rate_bps / 1e6:.2f} Mbps)")

def init_tc():
    subprocess.run(f"tc qdisc add dev {iface} root netem rate {bitrates_bps[0]}bit", shell=True)

def reset_tc():
    subprocess.run(f"tc qdisc del dev {iface} root", shell=True)

def update(frame_idx):
    idx = frame_idx % len(bitrates_bps)  # Loop around!
    rate = bitrates_bps[idx]
    now = datetime.now()

    times.append(now)
    rates_mbps.append(rate / 1e6)

    apply_rate(rate)

    ax.clear()
    ax.plot(times, rates_mbps, '-o', color='tab:blue')
    ax.set_title("Network Emulation Rate Over Time (Looped)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Bitrate (Mbps)")
    ax.grid(True)
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()

try:
    init_tc()
    ani = animation.FuncAnimation(fig, update, interval=1000, repeat=True)
    plt.show()
except KeyboardInterrupt:
    print("Interrupted. Cleaning up.")
finally:
    reset_tc()
    print("Cleanup done.")

