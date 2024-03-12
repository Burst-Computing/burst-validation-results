from matplotlib.collections import LineCollection
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from collections import defaultdict


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

BASELINE_GRANULARITY = 6

GRANULARITIES = [
    6,
    12,
    24,
    48,
]

DATA_REDUCTION = {
    48: [14.28571429, 42.85714286, 100],
    96: [6.666666667, 20, 46.66666667],
    192: [
        3.225806452,
        9.677419355,
        22.58064516,
    ],
}

COLLECTIVES = [
    "Gather",
    "Scatter",
    "Broadcast",
    "AllToAll",
]


def do_plot_compare(benchmark, medians, burst_size):
    percent_reduction = {}

    g_baseline = medians[benchmark][burst_size][BASELINE_GRANULARITY]
    for granularity in GRANULARITIES:
        if granularity == BASELINE_GRANULARITY:
            continue
        px = medians[benchmark][burst_size][granularity] / g_baseline
        reduction = 1 - px
        print(f"{burst_size=} {granularity=} {reduction=:.2f}")
        percent_reduction[granularity] = round(reduction * 100)

    fig, ax = plt.subplots()

    ax.grid(axis="y", linestyle="--", alpha=0.7, zorder=0)

    X = np.arange(len(GRANULARITIES) - 1)
    X_labels = [str(granularity) for granularity in GRANULARITIES if granularity != BASELINE_GRANULARITY]

    ax.set_xticks(X)
    ax.set_xticklabels(X_labels)

    ax.set_ylim(-10, 110)
    ax.set_yticks(np.arange(0, 101, 20))

    ax.plot(
        X,
        list(percent_reduction.values()),
        marker="x",
        ls="--",
        color="tab:red",
        zorder=3,
    )

    ax.set_xlabel("Granularity")
    ax.set_ylabel("Measured Latency Reduction respect to Granularity 6 (%)", color="tab:red")

    ax.tick_params(axis="y", labelcolor="tab:red")
    # ax.spines["left"].set_color("tab:red")

    ax.set_title(f"{benchmark} Latency & Remote Data Reduction ({burst_size=})")

    ax_t = ax.twinx()

    ax_t.set_ylim(-10, 110)
    ax_t.set_yticks(np.arange(0, 101, 20))

    ax_t.plot(
        X,
        DATA_REDUCTION[burst_size],
        marker="+",
        color="tab:grey",
        ls="--",
        label=str(burst_size),
        zorder=3,
    )
    ax_t.set_ylabel("Theoric Remote Data Reduction respect to Granularity 6 (%)", color="tab:grey")
    ax_t.tick_params(axis="y", labelcolor="tab:grey")
    # ax_t.spines["right"].set_color("tab:grey")

    fig.tight_layout()

    # plt.savefig(f"collectives/{benchmark}-percent.pdf", dpi=300)
    plt.savefig(f"collectives/{benchmark}-{burst_size}-compare.png", dpi=300)
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

                    median = np.median(times)

                    print(f"{burst_size=} {granularity=} {collective=} ==> {median:.2f} s")
                    medians[collective][burst_size][granularity] = median
                else:
                    print(f"{burst_size=} {granularity=} {collective=} ==> Empty!")
                    medians[collective][burst_size][granularity] = 0.0

    for burst_size in BURST_SIZES:
        for collective in COLLECTIVES:
            do_plot_compare(collective, medians, burst_size)
