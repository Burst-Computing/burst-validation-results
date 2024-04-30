import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import defaultdict
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
        "legend.borderpad": 0.1,
    }
)


CHUNK_SIZES = [
    (65536, "64KB"),
    (1048576, "1MB"),
    (67108864, "64MB"),
    (134217728, "128MB"),
    (268435456, "256MB"),
]

BACKENDS = {
    "RabbitMQ": "RabbitMQ",
    "RedisList": "Redis (List)",
    "DragonflyList": "Dragonfly (List)",
    "RedisStream": "Redis (Stream)",
    "DragonflyStream": "Dragonfly (Stream)",
    "S3": "S3",
    # "BurstMessageRelay": "Message Relay Server",
}

FILES = [
    "pairs2/rabbitmq.csv",
    "pairs2/redis-list.csv",
    "pairs2/dragonfly-list.csv",
    "pairs2/redis-stream.csv",
    "pairs2/dragonfly-stream.csv",
    "pairs2/s3.csv",
    # "pairs2/message-relay.csv",
]


if __name__ == "__main__":
    dfs = []
    for file in FILES:
        tmp_df = pd.read_csv(file)
        print(file)
        dfs.append(tmp_df)

    df = pd.concat(dfs, ignore_index=True, axis=0)

    Y_lat = defaultdict(list)
    Y_lat_stddev = defaultdict(list)
    Y_throughput = defaultdict(list)
    Y_throughput_stdev = defaultdict(list)
    for backend in BACKENDS.keys():
        for chunk_size, chunk_size_label in CHUNK_SIZES:
            tmp_df = df[(df["chunk_size"] == chunk_size) & (df["backend"] == backend)]
            if tmp_df.empty:
                print(f"Backend: {backend}, Chunk Size: {chunk_size} is empty. Skipping...")
                Y_lat[backend].append(0.0)
                Y_lat_stddev[backend].append(0.0)
                Y_throughput[backend].append(0.0)
                Y_throughput_stdev[backend].append(0.0)
                continue

            # group 1 is the sender (start), group 0 is the receiver (end)
            t_start = tmp_df[tmp_df["group_id"] == 1][["burst_id", "start"]]
            t_end = tmp_df[tmp_df["group_id"] == 0][["burst_id", "end"]]

            df_times = pd.merge(t_start, t_end, on="burst_id")
            latencies = df_times["end"] - df_times["start"]
            latency_avg = np.median(latencies)
            latency_std_dev = np.std(latencies)

            print(f"{backend} Latency ({chunk_size_label}): {latency_avg:.2f} s ± {latency_std_dev:.2f}")
            Y_lat[backend].append(latency_avg)
            Y_lat_stddev[backend].append(latency_std_dev)

            payload_sizes = tmp_df["payload_size"].unique()
            assert len(payload_sizes) == 1, f"Payload sizes are not consistent: {payload_sizes}"

            payload_size = payload_sizes[0] / 1024 / 1024  # Convert to MB
            throughputs = payload_size / latencies
            throughput_avg = np.median(throughputs)
            throughput_std_dev = np.std(throughputs)

            print(f"{backend} Throoughput ({chunk_size_label}): {throughput_avg:.2f} MB/s ± {throughput_std_dev:.2f}")
            Y_throughput[backend].append(throughput_avg)
            Y_throughput_stdev[backend].append(throughput_std_dev)

    X_labels = [chunk_size_label for _, chunk_size_label in CHUNK_SIZES]
    X = np.arange(len(X_labels))

    # fig, ax = plt.subplots(1, 1, figsize=(3.33, 2.4))
    # plt.subplots_adjust(top=0.95, bottom=0.2, left=0.13, right=0.75)

    # ax.grid(zorder=1)
    # bar_width = 0.12
    # kwargs = {
    #     "width": 0.1,
    #     "linewidth": 1,
    #     "edgecolor": "black",
    #     "align": "center",
    #     "alpha": 0.75,
    #     "ecolor": "black",
    #     "capsize": 3,
    #     "zorder": 3,
    # }

    # ax.bar(X - (bar_width * 2) - (bar_width / 2), Y_lat["RabbitMQ"], yerr=Y_lat_stddev["RabbitMQ"], label="RabbitMQ", **kwargs)
    # ax.bar(X - (bar_width * 2) - (bar_width / 2), Y_lat["RedisList"], yerr=Y_lat_stddev["RedisList"], label="RedisList", **kwargs)
    # ax.bar(
    #     X - (bar_width * 2) - (bar_width / 2),
    #     Y_lat["DragonflyList"],
    #     yerr=Y_lat_stddev["DragonflyList"],
    #     label="DragonflyList",
    #     **kwargs,
    # )
    # ax.bar(X - (bar_width * 2) - (bar_width / 2), Y_lat["RedisStream"], yerr=Y_lat_stddev["RedisStream"], label="RedisStream", **kwargs)
    # ax.bar(
    #     X - (bar_width * 2) - (bar_width / 2),
    #     Y_lat["DragonflyStream"],
    #     yerr=Y_lat_stddev["DragonflyStream"],
    #     label="DragonflyStream",
    #     **kwargs,
    # )
    # ax.bar(X - (bar_width * 2) - (bar_width / 2), Y_lat["S3"], yerr=Y_lat_stddev["S3"], label="S3", **kwargs)
    # ax.bar(
    #     X - (bar_width * 2) - (bar_width / 2),
    #     Y_lat["BurstMessageRelay"],
    #     yerr=Y_lat_stddev["BurstMessageRelay"],
    #     label="MessageRelay",
    #     **kwargs,
    # )

    # ax.set_xticks(X)
    # ax.set_xticklabels(X_labels)
    # ax.set_xlabel("Chunk Size")
    # ax.set_ylabel("Latency (s)")
    # ax.legend(loc="upper right")

    # fig.tight_layout()
    # plt.savefig("pairs2/latency.pdf", format="pdf", dpi=500)

    fig, ax = plt.subplots(1, 1, figsize=(3.33, 2.4))
    plt.subplots_adjust(top=0.95, bottom=0.2, left=0.13, right=0.75)

    ax.grid(zorder=0)
    bar_width = 0.12

    ax.set_ylim(0, 400)
    ax.set_yticks(np.arange(0, 401, 50))

    kwargs = {
        "width": bar_width,
        "linewidth": 0.5,
        "edgecolor": "black",
        "align": "center",
        "alpha": 0.75,
        "ecolor": "black",
        "capsize": 1.5,
        "zorder": 3,
    }

    ax.bar(
        X - (bar_width * 2) - (bar_width / 2),
        Y_throughput["RabbitMQ"],
        yerr=Y_throughput_stdev["RabbitMQ"],
        label="RabbitMQ",
        **kwargs,
    )
    ax.bar(
        X - (bar_width * 1) - (bar_width / 2),
        Y_throughput["RedisList"],
        yerr=Y_throughput_stdev["RedisList"],
        label="Redis List",
        **kwargs,
    )
    ax.bar(
        X - (bar_width * 0) - (bar_width / 2),
        Y_throughput["DragonflyList"],
        yerr=Y_throughput_stdev["DragonflyList"],
        label="DragonflyDB List",
        **kwargs,
    )
    ax.bar(
        X + (bar_width * 0) + (bar_width / 2),
        Y_throughput["RedisStream"],
        yerr=Y_throughput_stdev["RedisStream"],
        label="Redis Stream",
        **kwargs,
    )
    ax.bar(
        X + (bar_width * 1) + (bar_width / 2),
        Y_throughput["DragonflyStream"],
        yerr=Y_throughput_stdev["DragonflyStream"],
        label="DragonflyDB Stream",
        **kwargs,
    )
    ax.bar(
        X + (bar_width * 2) + (bar_width / 2), Y_throughput["S3"], yerr=Y_throughput_stdev["S3"], label="S3", **kwargs
    )
    # ax.bar(
    #     X - (bar_width * 2) - (bar_width / 2),
    #     Y_throughput["BurstMessageRelay"],
    #     yerr=Y_throughput_stdev["BurstMessageRelay"],
    #     label="MessageRelay",
    #     **kwargs,
    # )

    ax.set_xticks(X)
    ax.set_xticklabels(X_labels)
    ax.set_xlabel("Chunk Size")
    ax.set_ylabel("Throughput (MB/s)")

    # ax.legend(
    #     ncols=2,
    #     frameon=False,
    #     loc="upper left",
    #     # bbox_to_anchor=(0, 1.02, 1, 0.2),
    # )
    plt.legend(
        bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=2, frameon=False
    )

    fig.tight_layout()
    plt.savefig("pairs2/throughput-pair.pdf", format="pdf", dpi=500)
