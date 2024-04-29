import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import json
import math
import os
import pandas as pd

prop_cycle = plt.rcParams["axes.prop_cycle"]
colors = iter(prop_cycle.by_key()["color"])

GRANULARITY = 64
ITERATIONS = 3
INPUT_FILES = f"aws/g{GRANULARITY}/"
PLOT_FILE = f"lines_plot_g{GRANULARITY}"
LABELS = [
    "Data\nDownload",
    "Broadcast\nRanks",
    "Compute\nRanks",
    "Reduce\nRanks",
    "Sync\nError",
]
COLORS = [next(colors) for _ in range(len(LABELS))]


def compute_times_rates(time_rates, runtime_bins):
    x = np.array(time_rates)
    start_time = x[:, 0]
    end_time = x[:, 1]

    N = len(start_time)

    runtime_calls_hist = np.zeros((N, len(runtime_bins)))

    for i in range(N):
        s = start_time[i]
        e = end_time[i]
        a, b = np.searchsorted(runtime_bins, [s, e])
        if b - a > 0:
            runtime_calls_hist[i, a:b] = 1

    return {"start_tstamp": start_time, "end_tstamp": end_time, "runtime_calls_hist": runtime_calls_hist}


def calc_segments(start_t, end_t, stage_ix, print_label=True):
    assert len(start_t) == len(end_t)

    total_calls = len(start_t)
    y = np.arange(total_calls)

    # c = next(colors)
    # c = next(colors)
    # c = colors[stage_ix]
    label = LABELS[stage_ix] if print_label else None
    ax.scatter(start_t, y, s=1.5, c=COLORS[stage_ix], alpha=1, marker="o", zorder=2, label=label)
    # ax.scatter(start_t, y, s=15, c=c, alpha=1, marker="x", zorder=2)

    max_seconds = math.ceil(max(end_t))
    runtime_bins = np.linspace(0, max_seconds, max_seconds)
    times_rates = list(zip(start_t, end_t))
    time_hist = compute_times_rates(times_rates, runtime_bins)
    N = len(time_hist["start_tstamp"])
    line_segments = LineCollection(
        [[[time_hist["start_tstamp"][i], i], [time_hist["end_tstamp"][i], i]] for i in range(N)],
        linestyles="solid",
        color=COLORS[stage_ix],
        alpha=0.9,
        linewidth=1,
        zorder=2,
    )

    return line_segments


if __name__ == "__main__":
    fig, ax = plt.subplots()

    workers_data = []
    files = os.listdir(INPUT_FILES)
    for file in files:
        with open(os.path.join(INPUT_FILES, file), "r") as f:
            workers_data.extend(json.load(f))

    print(f"Loaded {len(workers_data)} workers data from {INPUT_FILES}")

    workers_data = sorted(workers_data, key=lambda x: x["key"])

    w0 = workers_data[0]
    cols = ["key"]
    cols.extend([key["key"] for key in w0["timestamps"]])

    rows = []
    for worker in workers_data:
        row = [worker["key"]]
        row.extend([(int(tstamp["value"]) / 1000) for tstamp in worker["timestamps"]])
        rows.append(row)

    df = pd.DataFrame(rows, columns=cols)

    global_t0 = df["worker_start"].min()
    global_t1 = df[f"iter_{ITERATIONS - 1}_end"].max()
    df["worker_start"] = global_t0

    ax.set_yticks(np.arange(0, len(df["key"]) + 16, 16))
    # ax.set_yticklabels(df["key"])

    # ax.set_xticks(np.arange(0, math.ceil(global_t1 - global_t0) + 10, 10))
    # ax.set_xticklabels(np.arange(0, math.ceil(df["worker_end"].max()), 10))

    lc = calc_segments(df["worker_start"] - global_t0, df["iter_0_start"] - global_t0, 0)
    ax.add_collection(lc)

    for iter in range(ITERATIONS):
        lc = calc_segments(
            df[f"iter_{iter}_start"] - global_t0, df[f"iter_{iter}_broadcast_weights"] - global_t0, 1, iter == 0
        )
        ax.add_collection(lc)

        lc = calc_segments(
            df[f"iter_{iter}_broadcast_weights"] - global_t0, df[f"iter_{iter}_calc_sums"] - global_t0, 2, iter == 0
        )
        ax.add_collection(lc)

        lc = calc_segments(
            df[f"iter_{iter}_calc_sums"] - global_t0, df[f"iter_{iter}_reduce"] - global_t0, 3, iter == 0
        )
        ax.add_collection(lc)

        lc = calc_segments(df[f"iter_{iter}_reduce"] - global_t0, df[f"iter_{iter}_end"] - global_t0, 4, iter == 0)
        ax.add_collection(lc)

    ax.set_title(f"Pagerank worker stages (Granularity = {GRANULARITY})")
    ax.set_xticks(np.arange(0, math.ceil(global_t1 - global_t0) + 25, 10))
    # ax.set_xticks(np.arange(0, math.ceil(global_t1 - global_t0) + 100, 25))

    ax.set_xlabel("Wallclock Time (s)")
    ax.set_ylabel("Worker ID")

    ax.grid(True, which="major", axis="both", linestyle="--", linewidth=0.5, alpha=0.75, zorder=1)
    ax.legend(loc="upper right")

    fig.tight_layout()
    plt.savefig(PLOT_FILE, dpi=300)
