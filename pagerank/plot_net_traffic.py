import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import numpy as np
from cycler import cycler

plt.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "serif",
        # "pgf.texsystem": "pdflatex",
        "font.size": 9,  # footnote/caption size 9pt for paper
        # "font.size": 10,     # caption size 10pt on thesis
        # "pgf.preamble": "\n".join(
        #     [
        #         r"\usepackage{libertine}",
        #         # r"\usepackage{lmodern}",
        #     ]
        # ),
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


BURST_SIZE = 256
GRANULARITIES = [1, 2, 4, 8, 16, 32, 64]
ITERATIONS = 1
INPUT_DATA_SZ = 128 * 1000 * 1000  # 128MB
VEC_SZ = 50_000_000
VEC_BYTES_SZ = VEC_SZ * (64 / 8)  # Vec type is float64 (64 bits), 8 bits in a byte, so 64/8


if __name__ == "__main__":
    traffic_granularity_tx = []
    traffic_granularity_rx = []

    for granularity in GRANULARITIES:
        groups = BURST_SIZE // granularity
        reduce_levels = int(math.log2(BURST_SIZE))
        local_levels = int(math.log2(granularity))
        remote_levels = reduce_levels - local_levels

        print("Reduce levels:", reduce_levels)
        print("Local levels:", local_levels)
        print("Remote levels:", remote_levels)
        print("Groups:", groups)

        remote_bytes_tx = 0
        remote_bytes_rx = 0
        local_bytes_tx = 0
        local_bytes_rx = 0

        for _ in range(ITERATIONS):
            # Broadcast weights
            remote_bytes_tx += VEC_BYTES_SZ  # root sends once to all
            remote_bytes_rx += groups * VEC_BYTES_SZ  # each group receives once

            # Tree reduce
            reduce_workers = 256
            for level in range(local_levels):
                w = reduce_workers // 2
                # print("Reduce level", level, "is local and has", w, "workers sending and receiving")
                local_bytes_tx += w * VEC_BYTES_SZ
                local_bytes_rx += w * VEC_BYTES_SZ
                reduce_workers = w
            for level in range(remote_levels):
                w = reduce_workers // 2
                # print("Reduce level", level, "is remote and has", w, "workers sending and receiving")
                remote_bytes_tx += w * VEC_BYTES_SZ
                remote_bytes_rx += w * VEC_BYTES_SZ
                reduce_workers = w

            # Err broadcast
            remote_bytes_tx += 64 / 8  # root sends once to all, err is a f64
            remote_bytes_rx += groups * (64 / 8)  # each group receives once, err is a f64

        print("Granularity:", granularity)
        print("Remote bytes tx (GB):", remote_bytes_tx / 1000 / 1000 / 1000)
        print("Remote bytes rx (GB):", remote_bytes_rx / 1000 / 1000 / 1000)

        traffic_granularity_tx.append(remote_bytes_tx)
        traffic_granularity_rx.append(remote_bytes_rx)

    traffic_granularity_tx = np.array(traffic_granularity_tx)
    traffic_granularity_rx = np.array(traffic_granularity_rx)

    traffic_granularity_tx /= 1000 * 1000 * 1000
    traffic_granularity_rx /= 1000 * 1000 * 1000

    fig, ax = plt.subplots(1, 1, figsize=(3.33, 2))
    plt.subplots_adjust(top=0.95, bottom=0.2, left=0.13, right=0.75)

    X = np.arange(len(GRANULARITIES))
    ax.set_xticks(X)
    ax.set_xticklabels([str(g) for g in GRANULARITIES])
    ax.grid(zorder=1)
    bar_width = 0.25

    ax.bar(
        X - (bar_width * 0) - (bar_width / 2),
        traffic_granularity_tx,
        width=bar_width,
        edgecolor="black",
        lw=1,
        label="Transmitted",
        color="tab:red",
        zorder=2,
    )
    ax.bar(
        X + (bar_width * 0) + (bar_width / 2),
        traffic_granularity_rx,
        width=bar_width,
        edgecolor="black",
        lw=1,
        label="Received",
        color="tab:blue",
        zorder=2,
    )

    ax.set_xlabel("Granularity")
    ax.set_ylabel("Total Network Traffic (GB)")
    # ax.set_title("Network Traffic (1 iteration)")

    ax.legend()
    fig.tight_layout()

    plt.savefig("pagerank/net_traffic.pdf", dpi=300)
