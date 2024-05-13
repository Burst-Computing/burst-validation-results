import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler
from matplotlib.collections import LineCollection
import numpy as np
import json
import math
import os
import pandas as pd


mpl.use("pgf")
plt.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "serif",
        "pgf.texsystem": "pdflatex",
        "font.size": 9,  # footnote/caption size 9pt for paper
        # "font.size": 10,     # caption size 10pt on thesis
        "pgf.preamble": "\n".join(
            [
                r"\usepackage{libertine}",
                # r"\usepackage{lmodern}",
            ]
        ),
        # "lines.linewidth": 0.8,
        "lines.markersize": 3,
        "axes.linewidth": 0.5,
        "grid.linewidth": 0.3,
        "grid.linestyle": "-",
        "axes.edgecolor": mpl.rcParams["grid.color"],
        # "ytick.color": mpl.rcParams["grid.color"],
        "ytick.direction": "in",
        # "xtick.color": mpl.rcParams["grid.color"],
        "xtick.direction": "in",
        "axes.titlesize": "medium",
        "axes.titlepad": 4,
        "axes.labelpad": 1,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.bottom": False,
        "axes.spines.left": False,
        "axes.axisbelow": True,  # grid below patches
        "axes.prop_cycle": cycler(
            "color", ["#348ABD", "#7A68A6", "#A60628", "#467821", "#CF4457", "#188487", "#E24A33"]
        ),
        "legend.labelspacing": 0.1,
        "legend.handlelength": 1,
        "legend.handletextpad": 0.2,
        "legend.columnspacing": 1,
        "legend.borderpad": 0.2,
    }
)

prop_cycle = plt.rcParams["axes.prop_cycle"]
colors = iter(prop_cycle.by_key()["color"])
COLORS = [next(colors) for _ in range(7)]

INPUT_MR_FILE = "terasort/terasort-classic2.csv"
INPUT_BURST_FILE = "terasort/terasort-burst1.csv"
# COLORS = [next(colors) for _ in range(len(3))]


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


def create_line_segments(x1, x2, y, color, label, ls, alpha):
    # ax1.scatter(
    #     x1,
    #     y,
    #     s=1,
    #     c=color,
    #     alpha=1,
    #     marker="o",
    #     zorder=2,
    #     label=label,
    # )

    runtime_bins = np.linspace(0, 200, 200)
    times_rates = list(zip(x1, x2))
    time_hist = compute_times_rates(times_rates, runtime_bins)
    N = len(time_hist["start_tstamp"])
    line_segments = LineCollection(
        [[[time_hist["start_tstamp"][i], i], [time_hist["end_tstamp"][i], i]] for i in range(N)],
        linestyles=ls,
        color=color,
        alpha=alpha,
        linewidth=0.5,
        zorder=2,
    )

    return line_segments


if __name__ == "__main__":
    with open(INPUT_MR_FILE, "r") as f:
        mr_df = pd.read_csv(f)

    # with open(INPUT_BURST_FILE, "r") as f:
    #     burst_df = pd.read_csv(f)

    worker_data = []
    path = "terasort/terasort-burst-noOW/exec2"
    for file in os.listdir(path):
        with open(os.path.join(path, file), "r") as f:
            group_data = json.load(f)
            worker_data.extend(group_data)
    burst_df = pd.DataFrame.from_dict(worker_data)
    for col in burst_df.columns:
        if burst_df[col].dtype == "object":
            burst_df[col] = pd.to_numeric(burst_df[col], errors="coerce")

    print(mr_df)
    print(burst_df)

    assert mr_df.shape[0] == burst_df.shape[0]

    fig, ax1 = plt.subplots(1, 1, figsize=(3.33, 2.1))
    # plt.subplots_adjust(top=0.95, bottom=0.2, left=0.13, right=0.75)

    ax1.grid(zorder=1)

    total_calls = mr_df.shape[0]
    print("Total calls:", total_calls)
    Y = np.arange(total_calls)

    ax1.set_yticks(np.arange(0, total_calls + 32, 32))
    ax1.set_xlim(0, 150)

    ax1.set_xlabel("Wallclock Time (s)")
    ax1.set_ylabel("Worker ID")

    mr_t0 = mr_df["init_fn_map"].min()
    # mr_t0 = mr_df["host_submit_map"].min()
    mr_t1 = mr_df["end_fn_reduce"].max()
    mr_t = mr_t1 - mr_t0

    print("Map-reduce time:", mr_t / 1000, "s")

    lc_handles = []

    print("Max worker runtime map:", mr_df["end_fn_map"].idxmax(), mr_df["end_fn_map"].max())

    # x1 = (mr_df["init_fn_map"] - mr_t0) / 1000
    # x2 = (mr_df["post_download_map"] - mr_t0) / 1000

    # line_segments = create_line_segments(x1, x2, Y, "tab:blue", "Input download", "-", 0.9)
    # ax1.add_collection(line_segments)
    # lc_handles.append(line_segments)

    # x1 = (mr_df["post_download_map"] - mr_t0) / 1000
    x1 = (mr_df["init_fn_map"] - mr_t0) / 1000
    x2 = (mr_df["end_fn_map"] - mr_t0) / 1000

    line_segments = create_line_segments(x1, x2, Y, "black", "Running worker", "-", 0.9)
    ax1.add_collection(line_segments)
    lc_handles.append(line_segments)

    x1 = (mr_df["init_fn_reduce"] - mr_t0) / 1000
    x2 = (mr_df["end_fn_reduce"] - mr_t0) / 1000

    line_segments = create_line_segments(x1, x2, Y, "black", "Sort", "-", 0.9)
    ax1.add_collection(line_segments)

    x1 = (mr_df["pre_upload_map"] - mr_t0) / 1000
    x2 = (mr_df["post_download_reduce"] - mr_t0) / 1000

    line_segments = create_line_segments(x1, x2, Y, "tab:red", "Shuffle", "-", 0.5)
    ax1.add_collection(line_segments)
    lc_handles.append(line_segments)

    # plt.legend(
    #     lc_handles,
    #     ["Input download", "Sort", "Shuffle"],
    #     bbox_to_anchor=(0, 1.02, 1, 0.2),
    #     loc="lower left",
    #     # mode="expand",
    #     borderaxespad=0,
    #     ncol=3,
    #     frameon=False,
    # )
    plt.legend(
        lc_handles,
        ["Running worker", "Shuffle"],
        bbox_to_anchor=(0, 1.02, 1, 0.2),
        loc="lower left",
        # mode="expand",
        borderaxespad=0,
        ncol=2,
        frameon=False,
    )

    fig.tight_layout()
    plt.savefig("terasort/terasort_mr.pdf", dpi=300)
    plt.close(fig)

    fig, ax2 = plt.subplots(1, 1, figsize=(3.33, 2.0))
    # plt.subplots_adjust(top=0.95, bottom=0.2, left=0.13, right=0.75)

    ax2.grid(zorder=1)

    ax2.set_yticks(np.arange(0, total_calls + 32, 32))
    ax2.set_xlim(0, 150)

    ax2.set_xlabel("Wallclock Time (s)")
    ax2.set_ylabel("Worker ID")

    # burst_t0 = burst_df["host_submit"].min()
    burst_t0 = burst_df["init_fn"].min()
    burst_t1 = burst_df["end_fn"].max()
    burst_t = burst_t1 - burst_t0

    print("Burst time:", burst_t / 1000, "s")

    lc_handles = []

    # x1 = (burst_df["init_fn"] - burst_t0) / 1000
    # x2 = (burst_df["post_download"] - burst_t0) / 1000

    # line_segments = create_line_segments(x1, x2, Y, "tab:blue", "Input download", "-", 0.9)
    # ax2.add_collection(line_segments)
    # lc_handles.append(line_segments)

    # x1 = (burst_df["post_download"] - burst_t0) / 1000
    x1 = (burst_df["init_fn"] - burst_t0) / 1000
    x2 = (burst_df["end_fn"] - burst_t0) / 1000

    line_segments = create_line_segments(x1, x2, Y, "black", "Running worker", "-", 0.9)
    ax2.add_collection(line_segments)
    lc_handles.append(line_segments)

    x1 = (burst_df["pre_shuffle"] - burst_t0) / 1000
    x2 = (burst_df["post_shuffle"] - burst_t0) / 1000

    line_segments = create_line_segments(x1, x2, Y, "tab:red", "Shuffle", "-", 0.5)
    ax2.add_collection(line_segments)
    lc_handles.append(line_segments)

    fig.tight_layout()
    plt.savefig("terasort/terasort_burst.pdf", dpi=300)
    plt.close(fig)

    print("Speedup: ", mr_t / burst_t)
