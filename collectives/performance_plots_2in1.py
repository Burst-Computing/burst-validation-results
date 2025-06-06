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
        "axes.prop_cycle": (
            cycler(color=["#348ABD", "#7A68A6", "#A60628", "#467821", "#CF4457", "#188487", "#E24A33"]) +
            cycler(linestyle=['-', '--', ':', '-.', '-', '--', ':'])
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
        "legend.labelspacing": 0.1,
        # "legend.handlelength": 1,
        "legend.handletextpad": 0.5,
        "legend.columnspacing": 1,
        "legend.borderpad": 0.1,
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


def do_plots(benchmark, medians, stdevs, print_legend=True):
    # fig, ax = plt.subplots()
    if print_legend:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(3.33, 1.6))
    else:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(3.33, 1.25))
    # plt.subplots_adjust(top=0.65, bottom=0.2, left=0.1, right=0.9, hspace=1)

    # ax.grid(axis="y", linestyle="--", alpha=0.7, zorder=0)
    ax1.grid(zorder=0)

    X = np.arange(len(GRANULARITIES))
    # X = np.arange(len(GRANULARITIES) - 1)
    X_labels = [str(granularity) for granularity in GRANULARITIES]
    # X_labels = [str(granularity) for granularity in GRANULARITIES if granularity != 1]

    ax1.set_xticks(X)
    ax1.set_xticklabels(X_labels)

    handles = []

    for burst_size in BURST_SIZES:
        handle = ax1.errorbar(
            X,
            list(medians[benchmark][burst_size].values()),
            # list(medians[benchmark][burst_size].values())[1:],
            yerr=list(stdevs[benchmark][burst_size].values()),
            # yerr=list(stdevs[benchmark][burst_size].values())[1:],
            marker="D",
            # ls="--",
            capsize=3.0,
            label=str(burst_size),
            zorder=3,
        )
        handles.append(handle)

    ax1.set_xlabel("Granularity")
    ax1.set_ylabel("Latency (s)")
    # ax1.legend(title="Burst Size")
    # ax.set_title(f"{benchmark} Latency")

    percent_reduction = {
        burst_size: {granularity: 0.0 for granularity in GRANULARITIES if granularity != 1}
        # burst_size: {granularity: 0.0 for granularity in GRANULARITIES}
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

    ax2.grid(zorder=0)

    # X = np.arange(len(GRANULARITIES))
    X = np.arange(len(GRANULARITIES) - 1)
    # X_labels = [str(granularity) for granularity in GRANULARITIES]
    X_labels = [str(granularity) for granularity in GRANULARITIES if granularity != 1]

    ax2.set_xticks(X)
    ax2.set_xticklabels(X_labels)

    for burst_size in BURST_SIZES:
        ax2.plot(
            X,
            list(percent_reduction[burst_size].values()),
            marker="D",
            # ls="--",
            label=str(burst_size),
            zorder=3,
        )

    ax2.set_xlabel("Granularity")
    ax2.set_ylabel("Latency Reduction\ncompared to\nGranularity 1 (\%)")
    # ax2.legend(title="Burst Size")

    if print_legend:
        fig.legend(
            handles,
            [str(burst_size) for burst_size in BURST_SIZES],
            bbox_to_anchor=(0.75, 1.00),
            # loc="upper center",
            # mode="expand",
            # borderaxespad=0,
            ncol=3,
            frameon=False,
            title="Burst Size",
        )

    fig.tight_layout()

    if print_legend:
        plt.subplots_adjust(top=0.7, bottom=0.2)
    else:
        plt.subplots_adjust(top=0.9, bottom=0.25)

    # plt.savefig(f"collectives/{benchmark}-latency.pdf", dpi=300)
    plt.savefig(f"collectives/{benchmark}-2in1.pdf", dpi=300)
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

    # for collective in COLLECTIVES:
    #     do_plots(collective, medians, stdevs)

    do_plots("Broadcast", medians, stdevs, True)
    do_plots("AllToAll", medians, stdevs, False)
