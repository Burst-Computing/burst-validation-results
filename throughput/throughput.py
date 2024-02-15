import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


BURST_SIZES = [
    8,
    16,
    32,
    96,
    192,
    384,
]

BACKENDS = {
    "RabbitMQ": "RabbitMQ",
    "RedisList": "Redis (List)",
    "DragonflyList": "Dragonfly (List)",
    "RedisStream": "Redis (Stream)",
    "DragonflyStream": "Dragonfly (Stream)",
    # "S3": "S3",
    "BurstMessageRelay": "Message Relay Server",
}

FILES = [
    "throughput/rabbitmq.csv",
    "throughput/redis-list.csv",
    "throughput/dragonfly-list.csv",
    "throughput/redis-stream.csv",
    "throughput/dragonfly-stream.csv",
    # "throughput/s3.csv",
    "throughput/message-relay.csv",
]


if __name__ == "__main__":
    dfs = []
    for file in FILES:
        df_burstsize_backend = pd.read_csv(file)
        dfs.append(df_burstsize_backend)

    df = pd.concat(dfs, ignore_index=True, axis=0)

    Y_throughput = defaultdict(list)
    Y_throughput_stdev = defaultdict(list)
    Y_throughput_workers = defaultdict(list)
    for backend in BACKENDS.keys():
        for burst_size in BURST_SIZES:
            df_burstsize_backend = df[(df["burst_size"] == burst_size) & (df["backend"] == backend)]
            if df_burstsize_backend.empty:
                print(f"Backend: {backend}, Burst Size: {burst_size} is empty. Skipping...")
                Y_throughput[backend].append(0.0)
                Y_throughput_stdev[backend].append(0.0)
                continue

            runs = []
            agg_data_sz = set()
            payload_sz = df_burstsize_backend["payload_size"].unique()
            assert len(payload_sz) == 1, f"Payload sizes are not consistent: {payload_sz}"
            payload_sz = payload_sz[0] / 1024 / 1024  # MB
            throughput_workers = []

            for burst_id in df_burstsize_backend["burst_id"].unique():
                df_burstsize_backend_burstid = df_burstsize_backend[df_burstsize_backend["burst_id"] == burst_id]

                # group 1 is the sender (start), group 0 is the receiver (end)
                t_start = df_burstsize_backend_burstid[df_burstsize_backend_burstid["group_id"] == 1]
                t_end = df_burstsize_backend_burstid[df_burstsize_backend_burstid["group_id"] == 0]

                # worker_id are not the same for sender group and receiver group, but they are paired consecutively
                # e.g. for a burst size of 8: worker 0 receives from worker 4, worker 1 from worker 5, ..., worker 3 from worker 7
                # so, we can sort by worker_id instead of joining the dataframes
                t_start = t_start.sort_values(by=["worker_id"])
                t_end = t_end.sort_values(by=["worker_id"])

                times = t_end["end"].to_numpy() - t_start["start"].to_numpy()
                throughput_workers_burstid = payload_sz / times
                throughput_workers.extend(throughput_workers_burstid)

                agg_data_transmitted = t_start["payload_size"].sum() / 1024 / 1024 / 1024  # GB
                t0 = t_start["start"].min()
                t1 = t_end["end"].max()
                throughput = agg_data_transmitted / (t1 - t0)

                agg_data_sz.add(agg_data_transmitted)  # sanity check for payload size
                runs.append(throughput)

            assert len(agg_data_sz) == 1, f"Data sizes are not consistent: {agg_data_sz}"
            throughput_avg = np.median(runs)
            throughput_std_dev = np.std(runs)

            print(f"{backend} Throughput ({burst_size}): {throughput_avg:.2f} GB/s ± {throughput_std_dev:.2f} GB/s")

            Y_throughput[backend].append(throughput_avg)
            Y_throughput_stdev[backend].append(throughput_std_dev)
            Y_throughput_workers[backend].append(throughput_workers)

    X_labels = [str(burst_size) for burst_size in BURST_SIZES]
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

    ax.bar(X - 0.3, Y_throughput["RabbitMQ"], yerr=Y_throughput_stdev["RabbitMQ"], label="RabbitMQ", **kwargs)
    ax.bar(X - 0.2, Y_throughput["RedisList"], yerr=Y_throughput_stdev["RedisList"], label="Redis (List)", **kwargs)
    ax.bar(
        X - 0.1,
        Y_throughput["DragonflyList"],
        yerr=Y_throughput_stdev["DragonflyList"],
        label="DragonflyDB (List)",
        **kwargs,
    )
    ax.bar(X, Y_throughput["RedisStream"], yerr=Y_throughput_stdev["RedisStream"], label="Redis (Stream)", **kwargs)
    ax.bar(
        X + 0.1,
        Y_throughput["DragonflyStream"],
        yerr=Y_throughput_stdev["DragonflyStream"],
        label="DragonflyDB (Stream)",
        **kwargs,
    )
    # ax.bar(X + 0.2, Y_throughput["S3"], yerr=Y_throughput_stdev["S3"], label="S3", **kwargs)
    ax.bar(
        X + 0.3,
        Y_throughput["BurstMessageRelay"],
        yerr=Y_throughput_stdev["BurstMessageRelay"],
        label="Xavi's server",
        **kwargs,
    )

    ax.set_xticks(X)
    ax.set_xticklabels(X_labels)
    ax.set_xlabel("Burst Size")
    ax.set_ylabel("Aggregated Throughput (GB/s)")
    ax.legend(loc="upper left")

    fig.tight_layout()
    plt.savefig("throughput/throughput.pdf", format="pdf", dpi=500)

    fig, ax = plt.subplots()
    ax.grid(axis="y", linestyle="--", alpha=0.7, zorder=0)

    elems = []

    bp = ax.boxplot(
        Y_throughput_workers["RabbitMQ"],
        positions=X - 0.3,
        widths=0.1,
        notch=False,
        showfliers=False,
        patch_artist=True,
        boxprops=dict(facecolor="lightyellow"),
        medianprops=dict(color="red"),
    )
    elems.append(bp)
    bp = ax.boxplot(
        Y_throughput_workers["RedisList"],
        positions=X - 0.2,
        widths=0.1,
        notch=False,
        showfliers=False,
        patch_artist=True,
        boxprops=dict(facecolor="thistle"),
        medianprops=dict(color="red"),
    )
    elems.append(bp)
    bp = ax.boxplot(
        Y_throughput_workers["DragonflyList"],
        positions=X - 0.1,
        widths=0.1,
        notch=False,
        showfliers=False,
        patch_artist=True,
        boxprops=dict(facecolor="lightgreen"),
        medianprops=dict(color="red"),
    )
    elems.append(bp)
    bp = ax.boxplot(
        Y_throughput_workers["RedisStream"],
        positions=X,
        widths=0.1,
        notch=False,
        showfliers=False,
        patch_artist=True,
        boxprops=dict(facecolor="lightblue"),
        medianprops=dict(color="red"),
    )
    elems.append(bp)
    bp = ax.boxplot(
        Y_throughput_workers["DragonflyStream"],
        positions=X + 0.1,
        widths=0.1,
        notch=False,
        showfliers=False,
        patch_artist=True,
        boxprops=dict(facecolor="lightcyan"),
        medianprops=dict(color="red"),
    )
    elems.append(bp)
    bp = ax.boxplot(
        Y_throughput_workers["BurstMessageRelay"],
        positions=X + 0.3,
        widths=0.1,
        notch=False,
        showfliers=False,
        patch_artist=True,
        boxprops=dict(facecolor="lightsalmon"),
        medianprops=dict(color="red"),
    )
    elems.append(bp)

    ax.legend(
        [element["boxes"][0] for element in elems], [backend for backend in BACKENDS.values()], loc="upper right"
    )

    ax.set_xticks(X)
    ax.set_xticklabels(X_labels)
    ax.set_xlabel("Burst size")
    ax.set_ylabel("Throughput per Worker (MB/s)")

    fig.tight_layout()
    plt.savefig("throughput/workers.pdf", format="pdf", dpi=500)
