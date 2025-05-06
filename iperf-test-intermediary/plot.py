import os
import json
import numpy as np
import matplotlib.pyplot as plt

def read_jsons(path):
    results = {}
    for folder in os.listdir(path):
        _, _, cl_sv, _, num, *bidir = folder.split('-', maxsplit=5)
        num = int(num)
        bidir = 'bidir' if bidir else 'single'
        results.setdefault(bidir, {})
        results[bidir].setdefault(cl_sv, {})
        results[bidir][cl_sv][num] = json.load(open(f'{path}/{folder}/iperf-{cl_sv}.json'))['end']
    return results


def plot_bidir(results):
    x = np.arange(1, 5)

    fig, ax = plt.subplots()
    ax.grid(axis="y", linestyle="--", alpha=0.7, zorder=0)

    kwargs = {
        "width": 0.35,
        "linewidth": 1,
        "edgecolor": "black",
        "align": "center",
        "alpha": 0.75,
        "ecolor": "black",
        "capsize": 3,
        "zorder": 3,
    }

    ax.bar(x - .35/2, [results['client'][i]['sum_sent']['bits_per_second'] / 1024**3 for i in range(1, 5)],  label='Sent', **kwargs)
    ax.bar(x + .35/2, [results['client'][i]['sum_received_bidir_reverse']['bits_per_second'] / 1024**3 for i in range(1, 5)],  label='Received', **kwargs)

    ax.set_ylabel('Throughput (Gbps)')
    ax.set_xlabel('Number of TCP streams')
    ax.set_title('Bidirectional Throughput')

    ax.set_xticks(x)
    ax.set_xticklabels([str(i) for i in range(1, 5)])
    ax.legend(loc="upper right")
    fig.tight_layout()
    plt.savefig("iperf-test-intermediary/bidir.pdf", format="pdf", dpi=500)

def plot_single(results):
    x = np.arange(1, 6)

    fig, ax = plt.subplots()
    ax.grid(axis="y", linestyle="--", alpha=0.7, zorder=0)

    kwargs = {
        "width": 0.35,
        "linewidth": 1,
        "edgecolor": "black",
        "align": "center",
        "alpha": 0.75,
        "ecolor": "black",
        "capsize": 3,
        "zorder": 3,
    }

    ax.bar(x, [results['client'][i]['sum_sent']['bits_per_second'] / 1024**3 for i in range(1, 6)],  label='Sent', **kwargs)

    ax.set_ylabel('Throughput (Gbps)')
    ax.set_xlabel('Number of TCP streams')
    ax.set_title('Single Direction Throughput')

    ax.set_xticks(x)
    ax.set_xticklabels([str(i) for i in range(1, 6)])
    ax.legend(loc="upper right")
    fig.tight_layout()
    plt.savefig("iperf-test-intermediary/single.pdf", format="pdf", dpi=500)


if __name__ == '__main__':
    path = 'iperf-test-intermediary/results'
    results = read_jsons(path)
    plot_bidir(results['bidir'])
    plot_single(results['single'])

