import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict


FILES = [
    "collectives/gather-dragonfly.csv",
    "collectives/scatter-dragonfly.csv",
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


def do_plot(benchmark, medians, stdevs):
    fig, ax = plt.subplots()

    ax.grid(axis="y", linestyle="--", alpha=0.7, zorder=0)

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
    ax.legend(title="Burst Size")

    fig.tight_layout()

    plt.savefig(f"collectives/{benchmark}.pdf", dpi=300)


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

    for burst_size in BURST_SIZES:
        for granularity in GRANULARITIES:
            print(f"Burst Size: {burst_size}, Granularity: {granularity}")
            tmp_df = df[(df["burst_size"] == burst_size) & (df["granularity"] == granularity)]
            if tmp_df.empty:
                print(f"Burst Size: {burst_size}, Granularity: {granularity} is empty. Skipping...")
                continue

            # Gather
            gather_df = tmp_df[tmp_df["benchmark"] == "Gather"]
            if not gather_df.empty:
                runs = pd.unique(gather_df["burst_id"])
                # print(runs)

                times = []
                for run in runs:
                    run_df = gather_df[gather_df["burst_id"] == run]

                    # For gather, consider only root worker (worker_id == 0)
                    worker_0 = run_df[run_df["worker_id"] == 0]
                    t0 = worker_0["start"].values[0]
                    t1 = worker_0["end"].values[0]
                    times.append(t1 - t0)

                median = np.median(times)
                stdev = np.std(times)

                print(f"Gather Latency: {median:.2f} s ± {stdev:.2f}")
                medians["gather"][burst_size][granularity] = median
                stdevs["gather"][burst_size][granularity] = stdev
            else:
                print(f"Burst Size: {burst_size}, Granularity: {granularity}, Gather is empty. Skipping...")
                medians["gather"][burst_size][granularity] = 0.0
                stdevs["gather"][burst_size][granularity] = 0.0

            # Scatter
            scatter_df = tmp_df[tmp_df["benchmark"] == "Scatter"]
            if not scatter_df.empty:
                runs = pd.unique(scatter_df["burst_id"])
                # print(runs)

                times = []
                for run in runs:
                    run_df = scatter_df[scatter_df["burst_id"] == run]

                    # For scatter, take t0 = min(start) and t1 = max(end)
                    t0 = run_df["start"].min()
                    t1 = run_df["end"].max()
                    times.append(t1 - t0)

                median = np.median(times)
                stdev = np.std(times)

                print(f"Scatter Latency: {median:.2f} s ± {stdev:.2f}")
                medians["scatter"][burst_size][granularity] = median
                stdevs["scatter"][burst_size][granularity] = stdev
            else:
                print(f"Burst Size: {burst_size}, Granularity: {granularity}, Scatter is empty. Skipping...")
                medians["scatter"][burst_size][granularity] = 0.0
                stdevs["scatter"][burst_size][granularity] = 0.0

    do_plot("gather", medians, stdevs)
    do_plot("scatter", medians, stdevs)
