import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import json
import math
import os
import pandas as pd
from pprint import pprint
from cycler import cycler

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
        "legend.borderpad": 0.3,
    }
)

# path, burst size, granularity
INPUT_FILES = [
    ("pagerank/aws/g1/", 1),
    ("pagerank/aws/g2/", 2),
    ("pagerank/aws/g4/", 4),
    ("pagerank/aws/g8/", 8),
    ("pagerank/aws/g16/", 16),
    ("pagerank/aws/g32/", 32),
    ("pagerank/aws/g64/", 64),
]

IERATIONS = 10


def process_exec(workers_data, granularity):
    w0 = workers_data[0]
    cols = ["key"]
    cols.extend([key["key"] for key in w0["timestamps"]])

    rows = []
    for worker in workers_data:
        row = [worker["key"]]
        row.extend([(int(tstamp["value"]) / 1000) for tstamp in worker["timestamps"]])
        rows.append(row)

    df = pd.DataFrame(rows, columns=cols)

    data_download = df["get_input"] - df["worker_start"]
    # print(data_download.max(), data_download.min(), data_download.median())

    print("Granularity ===>", granularity)

    acum_compute = np.zeros(len(df))
    acum_comm = np.zeros(len(df))
    for iter in range(IERATIONS):
        # if iter == 0 and granularity == 64:
        #     iter = 1

        bcast_ranks = df[f"iter_{iter}_broadcast_weights"] - df[f"iter_{iter}_start"]
        acum_comm += bcast_ranks
        print("Broadcast ranks", bcast_ranks.max(), bcast_ranks.min(), bcast_ranks.median())

        calc_sums = df[f"iter_{iter}_calc_sums"] - df[f"iter_{iter}_broadcast_weights"]
        acum_compute += calc_sums
        print("Calc", calc_sums.max(), calc_sums.min(), calc_sums.median())

        reduce_sums = df[f"iter_{iter}_reduce"] - df[f"iter_{iter}_calc_sums"]
        acum_comm += reduce_sums
        print("Reduce", reduce_sums.max(), reduce_sums.min(), reduce_sums.median())

        # calc_err = df[f"iter_{iter}_calc_err"] - df[f"iter_{iter}_reduce"]
        # acum_compute += calc_err
        # print(calc_err.max(), calc_err.min(), calc_err.median())

        # bcast_err = df[f"iter_{iter}_broadcast_err"] - df[f"iter_{iter}_calc_err"]
        # acum_comm += bcast_err
        # print("Broascast err", bcast_err.max(), bcast_err.min(), bcast_err.median())

        # reset = df[f"iter_{iter}_end"] - df[f"iter_{iter}_broadcast_err"]
        # acum_compute += reset
        # print(reset.max(), reset.min(), reset.median())

        print("---")

    print("=============================")

    # print(acum_comm.max(), acum_comm.min(), acum_comm.median())
    # print(acum_compute.max(), acum_compute.min(), acum_compute.median())

    return data_download, acum_comm, acum_compute


def single_plot(data_download_t, comm_t, compute_t, granularities):
    data_download_t = np.array(data_download_t)
    comm_t = np.array(comm_t)
    compute_t = np.array(compute_t)

    X = np.arange(len(granularities))
    fig, ax = plt.subplots(figsize=(3.33, 2))
    plt.subplots_adjust(top=0.95, bottom=0.2, left=0.13, right=0.75)

    ax.grid(zorder=0)
    # ax.grid(True, which="major", axis="y", linestyle="--", alpha=0.5)

    ax.set_xticks(X)
    ax.set_xticklabels(granularities)

    ax.bar(X, data_download_t, label="Data download", zorder=2)
    ax.bar(X, compute_t, label="Computation", bottom=data_download_t, zorder=2)
    ax.bar(X, comm_t, label="Communication overhead", bottom=data_download_t + compute_t, zorder=2)

    ax.set_ylabel("Accumulated\nExecution time (s)")
    ax.set_xlabel("Granularity")
    ax.set_title("Pagerank Execution Time Breakdown")

    ax.legend()

    fig.tight_layout()

    fig.savefig("pagerank/pagerank_execution_time_breakdown.pdf", dpi=500)


def broken_plot(data_download_t, comm_t, compute_t, granularities):
    data_download_t = np.array(data_download_t)
    comm_t = np.array(comm_t)
    compute_t = np.array(compute_t)

    X = np.arange(len(granularities))
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(3.33, 2))
    fig.subplots_adjust(hspace=0.05)  # adjust space between axes

    # ax1.grid(True, which="major", axis="y", linestyle="--", alpha=0.5)
    ax1.grid(zorder=0)
    ax2.grid(zorder=0)

    ax1.set_ylim(650, 850)  # outliers only
    ax2.set_ylim(0, 200)  # most of the data

    ax1.spines.bottom.set_visible(False)
    ax2.spines.top.set_visible(False)
    ax1.xaxis.tick_top()
    ax1.tick_params(labeltop=False)  # don't put tick labels at the top
    ax2.xaxis.tick_bottom()

    ax1.set_xticks(X)
    ax1.set_xticklabels(granularities)

    ax1.bar(X, data_download_t, label="Data download", zorder=2)
    ax2.bar(X, data_download_t, label="Data download", zorder=2)
    ax1.bar(X, compute_t, label="Computation", bottom=data_download_t, zorder=2)
    ax2.bar(X, compute_t, label="Computation", bottom=data_download_t, zorder=2)
    ax1.bar(X, comm_t, label="Communication overhead", bottom=data_download_t + compute_t, zorder=2)
    ax2.bar(X, comm_t, label="Communication overhead", bottom=data_download_t + compute_t, zorder=2)

    # d = 0.5  # proportion of vertical to horizontal extent of the slanted line
    # kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12, linestyle="none", color="k", mec="k", mew=1, clip_on=False)
    # ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
    # ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)

    # ax2.set_ylabel("Accumulated Execution time (s)")
    fig.text(0.0001, 0.5, "Accumulated\nExecution time (s)", va="center", rotation="vertical")
    ax2.set_xlabel("Granularity")
    # ax1.set_title("Pagerank Execution Time Breakdown")

    ax1.legend()

    fig.tight_layout()
    plt.subplots_adjust(left=0.175)

    fig.savefig("pagerank/pagerank_execution_time_breakdown2.pdf", dpi=500)


if __name__ == "__main__":

    data_download_t = []
    comm_t = []
    compute_t = []
    granularities = []

    for execution in INPUT_FILES:
        input_dir, granularity = execution
        workers_data = []
        files = os.listdir(input_dir)
        for file in files:
            with open(os.path.join(input_dir, file), "r") as f:
                workers_data.extend(json.load(f))

        print(f"Loaded {len(workers_data)} workers data from {input_dir}")

        data_download, comm, compute = process_exec(workers_data, granularity)
        data_download_t.append(data_download.median())
        comm_t.append(comm.median())
        compute_t.append(compute.median())
        granularities.append(str(granularity))

    single_plot(data_download_t, comm_t, compute_t, granularities)
    broken_plot(data_download_t, comm_t, compute_t, granularities)
