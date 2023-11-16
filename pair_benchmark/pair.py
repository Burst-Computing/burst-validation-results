import numpy as np
import matplotlib.pyplot as plt


throughput = [
    (616.918286142723, 616.836123659347),
    (600.054675594388, 599.522772599232),
    (619.53743598491, 1138.59278170914),
    (596.227122051095, 594.779331344595),
    (618.820179377165, 1137.0259879359),
    (597.415574861884, 595.837443110885),
]

group_size = [4, 8, 16, 32, 64, 96]

payload_per_worker = 256  # MB


def plot_agg_throughput():
    X = ["8", "16", "32", "64", "128", "192"]

    fig, ax = plt.subplots()

    X_axis = np.arange(len(X))

    ax.grid(axis="y", linestyle="--", linewidth=0.5)

    ax.bar(X_axis - 0.15, [x[0] for x in throughput], 0.25, label="Receive", edgecolor="black", linewidth=1, zorder=3)
    ax.bar(X_axis + 0.15, [x[1] for x in throughput], 0.25, label="Send", edgecolor="black", linewidth=1, zorder=3)

    ax.set_xticks(X_axis, X)
    ax.set_xlabel("Burst Size")
    ax.set_ylabel("Aggregated Throughput (MB/s)")
    ax.legend(loc="upper left")

    fig.tight_layout()

    fig.savefig("pair_benchmark/pair.pdf", format="pdf", dpi=500)


def plot_worker_throughput():
    X = [str(x * payload_per_worker) + "MB\n(" + str(x) + ")" for x in group_size]
    worker_throughput_send = [t[0] / gz for t, gz in zip(throughput, group_size)]
    worker_throughput_receive = [t[1] / gz for t, gz in zip(throughput, group_size)]

    fig, ax = plt.subplots()

    X_axis = np.arange(len(X))

    ax.grid(axis="y", linestyle="--", linewidth=0.5)

    ax.bar(X_axis - 0.15, worker_throughput_receive, 0.25, label="Receive", edgecolor="black", linewidth=1, zorder=3)
    ax.bar(X_axis + 0.15, worker_throughput_send, 0.25, label="Send", edgecolor="black", linewidth=1, zorder=3)

    ax.set_xticks(X_axis, X)
    ax.set_xlabel("Data transmitted (Group Size)")
    ax.set_ylabel("Avg. Worker Throughput (MB/s)")
    ax.legend(loc="upper right")

    fig.tight_layout()
    fig.savefig("pair_benchmark/pair_worker_troughput.pdf", format="pdf", dpi=500)


def plot_worker_time():
    X = [str(x * payload_per_worker) + "MB\n(" + str(x) + ")" for x in group_size]
    worker_time_send = [payload_per_worker / (t[0] / gz) for t, gz in zip(throughput, group_size)]
    worker_time_receive = [payload_per_worker / (t[1] / gz) for t, gz in zip(throughput, group_size)]

    fig, ax = plt.subplots()

    X_axis = np.arange(len(X))

    ax.grid(axis="y", linestyle="--", linewidth=0.5)

    ax.bar(X_axis - 0.15, worker_time_send, 0.25, label="Receive", edgecolor="black", linewidth=1, zorder=3)
    ax.bar(X_axis + 0.15, worker_time_receive, 0.25, label="Send", edgecolor="black", linewidth=1, zorder=3)

    ax.set_xticks(X_axis, X)
    ax.set_xlabel("Data transmitted (Group Size)")
    ax.set_ylabel("Avg. Worker Data Transmit Time (s)")
    ax.legend(loc="upper left")

    fig.tight_layout()
    fig.savefig("pair_benchmark/pair_worker_time.pdf", format="pdf", dpi=500)


if __name__ == "__main__":
    plot_agg_throughput()
    plot_worker_throughput()
    plot_worker_time()
