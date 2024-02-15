import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


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
    "BurstMessageRelay": "Message Relay Server",
}

FILES = [
    "pairs2/rabbitmq.csv",
    "pairs2/redis-list.csv",
    "pairs2/dragonfly-list.csv",
    "pairs2/redis-stream.csv",
    "pairs2/dragonfly-stream.csv",
    "pairs2/s3.csv",
    "pairs2/message-relay.csv",
]

PAYLOAD_SIZE = (1073741824 / 1024) / 1024  # 1GB in MB


if __name__ == "__main__":
    dfs = []
    for file in FILES:
        tmp_df = pd.read_csv(file)
        print(file)
        dfs.append(tmp_df)

    df = pd.concat(dfs, ignore_index=True, axis=0)

    Y_lat = defaultdict(list)
    Y_lat_stddev = defaultdict(list)
    data_throughput = defaultdict(list)
    data_throughput_std_dev = defaultdict(list)
    for backend in BACKENDS.keys():
        for chunk_size, chunk_size_label in CHUNK_SIZES:
            tmp_df = df[(df["chunk_size"] == chunk_size) & (df["backend"] == backend)]
            if tmp_df.empty:
                print(f"Backend: {backend}, Chunk Size: {chunk_size} is empty. Skipping...")
                Y_lat[backend].append(0.0)
                Y_lat_stddev[backend].append(0.0)
                data_throughput[backend].append(0.0)
                data_throughput_std_dev[backend].append(0.0)
                continue

            t_start = tmp_df[tmp_df["group_id"] == 0][["burst_id", "start"]]
            t_end = tmp_df[tmp_df["group_id"] == 1][["burst_id", "end"]]

            df_times = pd.merge(t_start, t_end, on="burst_id")
            latencies = df_times["end"] - df_times["start"]
            latency_avg = np.median(latencies)
            latency_std_dev = np.std(latencies)

            print(f"{backend} Latency ({chunk_size_label}): {latency_avg:.2f} s ± {latency_std_dev:.2f}")
            Y_lat[backend].append(latency_avg)
            Y_lat_stddev[backend].append(latency_std_dev)

            throughputs = PAYLOAD_SIZE / latencies
            throughput_avg = np.median(throughputs)
            throughput_std_dev = np.std(throughputs)

            print(f"{backend} Throoughput ({chunk_size_label}): {throughput_avg:.2f} MB/s ± {throughput_std_dev:.2f}")
            data_throughput[backend].append(throughput_avg)
            data_throughput_std_dev[backend].append(throughput_std_dev)

    X_labels = [chunk_size_label for _, chunk_size_label in CHUNK_SIZES]
    X = np.arange(len(X_labels))

    fig, ax = plt.subplots()
    ax.grid(axis="y", linestyle="--", alpha=0.7, zorder=0)
    kwargs = {
        "width": 0.1,
        "linewidth": 1,
        "edgecolor": "black",
        "align": "center",
        "alpha": 0.75,
        "ecolor": "black",
        "capsize": 3,
        "zorder": 3,
    }

    ax.bar(X - 0.3, Y_lat["RabbitMQ"], yerr=Y_lat_stddev["RabbitMQ"], label="RabbitMQ", **kwargs)
    ax.bar(X - 0.2, Y_lat["RedisList"], yerr=Y_lat_stddev["RedisList"], label="RedisList", **kwargs)
    ax.bar(
        X - 0.1,
        Y_lat["DragonflyList"],
        yerr=Y_lat_stddev["DragonflyList"],
        label="DragonflyList",
        **kwargs,
    )
    ax.bar(X, Y_lat["RedisStream"], yerr=Y_lat_stddev["RedisStream"], label="RedisStream", **kwargs)
    ax.bar(
        X + 0.1,
        Y_lat["DragonflyStream"],
        yerr=Y_lat_stddev["DragonflyStream"],
        label="DragonflyStream",
        **kwargs,
    )
    ax.bar(X + 0.2, Y_lat["S3"], yerr=Y_lat_stddev["S3"], label="S3", **kwargs)
    ax.bar(
        X + 0.3,
        Y_lat["BurstMessageRelay"],
        yerr=Y_lat_stddev["BurstMessageRelay"],
        label="MessageRelay",
        **kwargs,
    )

    ax.set_xticks(X)
    ax.set_xticklabels(X_labels)
    ax.set_xlabel("Chunk Size")
    ax.set_ylabel("Latency (s)")
    ax.legend(loc="upper right")

    fig.tight_layout()
    plt.savefig("pairs2/latency.pdf", format="pdf", dpi=500)

    fig, ax = plt.subplots()
    ax.grid(axis="y", linestyle="--", alpha=0.7, zorder=0)
    kwargs = {
        "width": 0.1,
        "linewidth": 1,
        "edgecolor": "black",
        "align": "center",
        "alpha": 0.75,
        "ecolor": "black",
        "capsize": 3,
        "zorder": 3,
    }
    ax.bar(X - 0.3, data_throughput["RabbitMQ"], yerr=data_throughput_std_dev["RabbitMQ"], label="RabbitMQ", **kwargs)
    ax.bar(
        X - 0.2, data_throughput["RedisList"], yerr=data_throughput_std_dev["RedisList"], label="RedisList", **kwargs
    )
    ax.bar(
        X - 0.1,
        data_throughput["DragonflyList"],
        yerr=data_throughput_std_dev["DragonflyList"],
        label="DragonflyList",
        **kwargs,
    )
    ax.bar(
        X, data_throughput["RedisStream"], yerr=data_throughput_std_dev["RedisStream"], label="RedisStream", **kwargs
    )
    ax.bar(
        X + 0.1,
        data_throughput["DragonflyStream"],
        yerr=data_throughput_std_dev["DragonflyStream"],
        label="DragonflyStream",
        **kwargs,
    )
    ax.bar(X + 0.2, data_throughput["S3"], yerr=data_throughput_std_dev["S3"], label="S3", **kwargs)
    ax.bar(
        X + 0.3,
        data_throughput["BurstMessageRelay"],
        yerr=data_throughput_std_dev["BurstMessageRelay"],
        label="MessageRelay",
        **kwargs,
    )

    ax.set_xticks(X)
    ax.set_xticklabels(X_labels)
    ax.set_xlabel("Chunk Size")
    ax.set_ylabel("Throughput (MB/s)")
    ax.legend(loc="upper right")

    fig.tight_layout()
    plt.savefig("pairs2/throughput.pdf", format="pdf", dpi=500)
