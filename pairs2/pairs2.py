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

BACKENDS = {"RabbitMQ": "RabbitMQ", "RedisList": "Redis (List)", "RedisStream": "Redis (Stream)", "S3": "S3"}

FILES = ["pairs2/rabbitmq.csv", "pairs2/redis-list.csv", "pairs2/redis-stream.csv", "pairs2/s3.csv"]


if __name__ == "__main__":
    dfs = []
    for file, (chunk_size, chunk_size_str) in zip(FILES, CHUNK_SIZES):
        tmp_df = pd.read_csv(file)
        dfs.append(tmp_df)

    df = pd.concat(dfs, ignore_index=True, axis=0)

    data_latency = defaultdict(list)
    data_latency_std_dev = defaultdict(list)
    data_throughput = defaultdict(list)
    data_throughput_std_dev = defaultdict(list)
    for backend in BACKENDS.keys():
        for chunk_size, chunk_size_label in CHUNK_SIZES:
            tmp_df = df[(df["chunk_size"] == chunk_size) & (df["backend"] == backend)]
            latencies = tmp_df["end"] - tmp_df["start"]
            latency_avg = np.median(latencies)
            latency_std_dev = np.std(latencies)

            print(f"{backend} Latency ({chunk_size_label}): {latency_avg:.2f} s ± {latency_std_dev:.2f}")
            data_latency[backend].append(latency_avg)
            data_latency_std_dev[backend].append(latency_std_dev)

            throughputs = tmp_df["throughput"]
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
        "width": 0.15,
        "linewidth": 1,
        "edgecolor": "black",
        "align": "center",
        "alpha": 0.75,
        "ecolor": "black",
        "capsize": 3,
        "zorder": 3,
    }
    ax.bar(X - 0.3, data_latency["RabbitMQ"], yerr=data_latency_std_dev["RabbitMQ"], label="RabbitMQ", **kwargs)
    ax.bar(X - 0.15, data_latency["RedisList"], yerr=data_latency_std_dev["RedisList"], label="RedisList", **kwargs)
    ax.bar(X, data_latency["RedisStream"], yerr=data_latency_std_dev["RedisStream"], label="RedisStream", **kwargs)
    ax.bar(X + 0.15, data_latency["S3"], yerr=data_latency_std_dev["S3"], label="S3", **kwargs)
    # ax.bar(X + 0.3, data_latency["RedisStream"], yerr=data_latency_std_dev["RedisStream"], label="RedisList", **kwargs)

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
        "width": 0.15,
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
        X - 0.15, data_throughput["RedisList"], yerr=data_throughput_std_dev["RedisList"], label="RedisList", **kwargs
    )
    ax.bar(
        X, data_throughput["RedisStream"], yerr=data_throughput_std_dev["RedisStream"], label="RedisStream", **kwargs
    )
    ax.bar(X + 0.15, data_throughput["S3"], yerr=data_throughput_std_dev["S3"], label="S3", **kwargs)
    # ax.bar(X + 0.3, data_latency["RedisStream"], yerr=data_latency_std_dev["RedisStream"], label="RedisList", **kwargs)

    ax.set_xticks(X)
    ax.set_xticklabels(X_labels)
    ax.set_xlabel("Chunk Size")
    ax.set_ylabel("Throughput (MB/s)")
    ax.legend(loc="upper right")

    fig.tight_layout()
    plt.savefig("pairs2/throughput.pdf", format="pdf", dpi=500)
