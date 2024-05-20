from matplotlib.collections import LineCollection
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import math
from collections import defaultdict
from cycler import cycler


# plt.style.use("ggplot")
# colors = plt.rcParams["axes.prop_cycle"]
# plt.style.use("matplotlib")


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
        "axes.prop_cycle": cycler(
            "color", ["#348ABD", "#7A68A6", "#A60628", "#467821", "#CF4457", "#188487", "#E24A33"]
        ),
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
        "legend.labelspacing": 0.15,
        "legend.handlelength": 1,
        "legend.handletextpad": 0.2,
        "legend.columnspacing": 1,
        "legend.borderpad": 0.3,
    }
)

FILES = [
    "collectives/gather-dragonfly.csv",
    "collectives/scatter-dragonfly.csv",
    "collectives/broadcast-dragonfly.csv",
    "collectives/all-to-all-dragonfly.csv",
]

BURST_SIZES = [
    48,
    96,
    192,
]

GRANULARITIES = [
    1,
    6,
    12,
    24,
    48,
]

COLLECTIVES = [
    "Gather",
    "Scatter",
    "Broadcast",
    "AllToAll",
]


def do_plot_latency(benchmark, medians, stdevs, legend=True):
    # fig, ax = plt.subplots()
    fig, ax = plt.subplots(1, 1, figsize=(2.2, 2))
    plt.subplots_adjust(top=0.95, bottom=0.2, left=0.13, right=0.75)

    # ax.grid(axis="y", linestyle="--", alpha=0.7, zorder=0)
    ax.grid(zorder=0)

    X = np.arange(len(GRANULARITIES))
    X_labels = [str(granularity) for granularity in GRANULARITIES]

    ax.set_xticks(X)
    ax.set_xticklabels(X_labels)

    for burst_size in BURST_SIZES:
        ax.errorbar(
            X,
            list(medians[benchmark][burst_size].values()),
            yerr=list(stdevs[benchmark][burst_size].values()),
            marker="D",
            ls="--",
            capsize=3.0,
            label=str(burst_size),
            zorder=3,
        )

    ax.set_xlabel("Granularity")
    ax.set_ylabel("Latency (s)")
    if legend:
        ax.legend(title="Burst Size")
    # ax.set_title(f"{benchmark} Latency")

    fig.tight_layout()

    # plt.savefig(f"collectives/{benchmark}-latency.pdf", dpi=300)
    plt.savefig(f"collectives/{benchmark}-latency.pdf", dpi=300)
    plt.close(fig)


def do_plot_percent(benchmark, medians, stdevs, legend=True):
    percent_reduction = {
        burst_size: {granularity: 0.0 for granularity in GRANULARITIES if granularity != 1}
        for burst_size in BURST_SIZES
    }

    for burst_size in BURST_SIZES:
        g1 = medians[benchmark][burst_size][1]
        for granularity in GRANULARITIES:
            if granularity == 1:
                continue
            px = medians[benchmark][burst_size][granularity] / g1
            reduction = 1 - px
            print(f"{burst_size=} {granularity=} {reduction=:.2f}")
            percent_reduction[burst_size][granularity] = round(reduction * 100)

    fig, ax = plt.subplots(1, 1, figsize=(2.2, 2))
    plt.subplots_adjust(top=0.95, bottom=0.2, left=0.13, right=0.75)

    ax.grid(zorder=0)

    X = np.arange(len(GRANULARITIES) - 1)
    X_labels = [str(granularity) for granularity in GRANULARITIES if granularity != 1]

    ax.set_xticks(X)
    ax.set_xticklabels(X_labels)

    for burst_size in BURST_SIZES:
        ax.plot(
            X,
            list(percent_reduction[burst_size].values()),
            marker="D",
            ls="--",
            label=str(burst_size),
            zorder=3,
        )

    ax.set_xlabel("Granularity")
    ax.set_ylabel("Latency Reduction\nrespect to Granularity 1 (\%)")
    if legend:
        ax.legend(title="Burst Size")
    # ax.set_title(f"{benchmark} Latency Reduction")

    fig.tight_layout()

    # plt.savefig(f"collectives/{benchmark}-percent.pdf", dpi=300)
    plt.savefig(f"collectives/{benchmark}-percent.pdf", dpi=300)
    plt.close(fig)


def do_plot_histogram(run_data, title=None, legend=True):
    fig, ax = plt.subplots(figsize=(10, 10))

    benchmark = run_data["benchmark"].iloc[0]

    min_tstamp = run_data["start"].min()
    max_tstamp = run_data["end"].max()
    max_t = max_tstamp - min_tstamp

    ax.set_title("{benchmark} Execution Times")
    ax.set_xlabel("Execution Time (s)")
    ax.set_ylabel("Worker ID")

    ax.set_ylim(-1, run_data["burst_size"].values[0] + 1)
    ax.set_yticks(np.arange(0, run_data["burst_size"].values[0] + 1, 6))

    ax.grid(linestyle="--", linewidth=0.5)

    run_data_sorted = run_data.sort_values(by="worker_id")

    line_segments = LineCollection(
        [
            [(worker["start"] - min_tstamp, worker["worker_id"]), (worker["end"] - min_tstamp, worker["worker_id"])]
            for _, worker in run_data_sorted.iterrows()
        ],
        linestyles="solid",
        color="k",
        alpha=1,
        linewidth=1,
    )
    ax.add_collection(line_segments)

    ax.axvline(x=max_t, color="tab:blue", linestyle="--", label="Collective Completion Time")

    # add a line to represent the parallelism
    max_seconds = 4 * math.ceil(max_t / 4)
    parallelism = np.zeros(max_seconds)

    for _, worker in run_data_sorted.iterrows():
        f_start = math.ceil(worker["start"] - min_tstamp)
        f_stop = math.ceil(worker["end"] - min_tstamp)
        parallelism[f_start:f_stop] += 1

    ax.plot(parallelism, color="tab:red", label="Parallelism")

    # legend
    if legend:
        ax.legend(loc="upper right")

    if title is None:
        title = f"{benchmark} Execution Times"
    # ax.set_title(title)

    fig.tight_layout()

    # save plot
    plt.savefig(f"collectives/parallelism/{title}.pdf", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    dfs = []
    for file in FILES:
        tmp_df = pd.read_csv(file)
        dfs.append(tmp_df)

    df = pd.concat(dfs, ignore_index=True, axis=0)

    # df["benchmark"] = df["benchmark"].astype(str)
    # df["backend"] = df["backend"].astype(str)
    # df["burst_id"] = df["burst_id"].astype(str)
    # df["burst_size"] = df["burst_size"].astype(int)
    # df["groups"] = df["groups"].astype(int)
    # df["granularity"] = df["granularity"].astype(int)
    # df["chunking"] = df["chunking"].astype(bool)
    # df["chunk_size"] = df["chunk_size"].astype(int)
    # df["payload_size"] = df["payload_size"].astype(int)
    # df["group_id"] = df["group_id"].astype(str)
    # df["worker_id"] = df["worker_id"].astype(int)
    # df["throughput"] = df["throughput"].astype(float)
    # df["start"] = df["start"].astype(float)
    # df["end"] = df["end"].astype(float)

    print(df.info())

    tree = lambda: defaultdict(tree)

    medians = tree()
    stdevs = tree()
    fastest_run = tree()
    slowest_run = tree()

    for burst_size in BURST_SIZES:
        for granularity in GRANULARITIES:
            # print(f"Burst Size: {burst_size}, Granularity: {granularity}")
            tmp_df = df[(df["burst_size"] == burst_size) & (df["granularity"] == granularity)]
            if tmp_df.empty:
                print(f"Burst Size: {burst_size}, Granularity: {granularity} is empty. Skipping...")
                continue

            for collective in COLLECTIVES:
                coll_df = tmp_df[tmp_df["benchmark"] == collective]
                if not coll_df.empty:
                    runs = pd.unique(coll_df["burst_id"])
                    # print(runs)

                    times = []
                    for run in runs:
                        run_df = coll_df[coll_df["burst_id"] == run]

                        # Take t0 = min(start) and t1 = max(end)
                        t0 = run_df["start"].min()
                        t1 = run_df["end"].max()
                        times.append(t1 - t0)

                    imax = np.argmax(np.array(times))
                    imin = np.argmin(np.array(times))

                    fastest_run[collective][burst_size][granularity] = coll_df[coll_df["burst_id"] == runs[imin]]
                    slowest_run[collective][burst_size][granularity] = coll_df[coll_df["burst_id"] == runs[imax]]

                    median = np.median(times)
                    stdev = np.std(times)

                    print(f"{burst_size=} {granularity=} {collective=} ==> {median:.2f} s ± {stdev:.2f}")
                    medians[collective][burst_size][granularity] = median
                    stdevs[collective][burst_size][granularity] = stdev
                else:
                    print(f"{burst_size=} {granularity=} {collective=} ==> Empty!")
                    medians[collective][burst_size][granularity] = 0.0
                    stdevs[collective][burst_size][granularity] = 0.0

    do_plot_latency(COLLECTIVES[2], medians, stdevs)
    do_plot_percent(COLLECTIVES[2], medians, stdevs)

    do_plot_latency(COLLECTIVES[3], medians, stdevs, legend=False)
    do_plot_percent(COLLECTIVES[3], medians, stdevs, legend=False)
    # for collective in COLLECTIVES:
    # do_plot_latency(collective, medians, stdevs)
    # do_plot_percent(collective, medians, stdevs)
    # for burst_size in BURST_SIZES:
    #     for granularity in GRANULARITIES:
    #         do_plot_histogram(
    #             fastest_run[collective][burst_size][granularity],
    #             f"{collective} Execution Times (fastest run, {burst_size=}, {granularity=})",
    #         )
    #         do_plot_histogram(
    #             slowest_run[collective][burst_size][granularity],
    #             f"{collective} Execution Times (slowest run, {burst_size=}, {granularity=})",
    #         )
