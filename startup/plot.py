import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import defaultdict
from cycler import cycler
from itertools import count

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

BURST_SIZES = [
    100,
    1000,
]

SERVICES = [
    "AWS 256 MB",
    "AWS 10 GB",
    "GCP 256 MB",
    "GCP 8 GB",
]

FILES = [
    "startup/aws-100func-single256.csv",
    "startup/aws-100func-biglambda.csv",
    "startup/gcp-100-256MB.csv",
    "startup/gcp-100-8192MB.csv",
    "startup/aws-1000func-single256.csv",
    "startup/aws-1000func-biglambda.csv",
    "startup/gcp-1000-256MB.csv",
    "startup/gcp-1000-8192MB.csv",
]


if __name__ == "__main__":
    dfs = []
    for file in FILES:
        df_burstsize_backend = pd.read_csv(file)
        dfs.append(df_burstsize_backend)
    
    mins = []
    maxs = []
    ctns = []
    times = []
    for df in dfs:
        time_zero = df["host_job_create_tstamp"].min()
        times.append(df["worker_func_start_tstamp"] - time_zero)
        mins.append((df["worker_func_start_tstamp"] - time_zero).min())
        maxs.append((df["worker_func_start_tstamp"] - time_zero).max())
        ctns.append(df.shape[0])

    tups = zip(mins, maxs, ctns)
    
    for size in BURST_SIZES:
        for service in SERVICES:
            tup = next(tups)
            print(f"{service} - {tup[2]} Min: {tup[0]} Max: {tup[1]}")


    # PLOT

    # X_labels = [str(size) for size in BURST_SIZES]
    # X = np.arange(len(X_labels))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(3.33, 1.6))
    # plt.subplots_adjust(top=0.8, bottom=0.1, left=0.1, right=0.9)

    # ax.set_ylim(0, 3)
    # ax.set_yticks(np.arange(0, 3.1, 0.5))

    ax1.grid(which='both', axis='x', zorder=1)
    ax1.grid(which='minor', axis='x', linewidth=0.1, linestyle="--")
    ax1.minorticks_on()
    ax1.tick_params(axis='y', which='both', left=False)
    ax1.set_yticklabels([])
    ax1.set_xlabel("Time (s)")

    data = zip(mins, maxs)
    X = count()
    
    for service in SERVICES:
        (first, last) = next(data)
        x = next(X)
        ax1.barh(
            x,
            last,
            label=service,
        )
        ax1.plot(first, x, marker='|', color='k', markersize=14)


    
    ax2.grid(which='both', axis='x', zorder=1)
    ax2.grid(which='minor', axis='x', linewidth=0.1, linestyle="--")
    ax2.minorticks_on()
    ax2.tick_params(axis='y', which='both', left=False)

    ax2.set_yticklabels([])
    ax2.set_xlabel("Time (s)")

    X = count()
    
    for service in SERVICES:
        (first, last) = next(data)
        x = next(X)
        ax2.barh(
            x,
            last,
            # label=service,
        )
        ax2.plot(first, x, marker='|', color='k', markersize=14)

    fig.legend(
         loc="upper left", mode="expand", borderaxespad=0, ncol=4, frameon=False
    )

    fig.tight_layout()
    plt.savefig("startup/faas-startup.pdf", format="pdf", dpi=500)


    # CDF

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(3.33, 1.6))
    plt.subplots_adjust(top=0.85, bottom=0.2, left=0.12, right=0.95)
    plt.subplots_adjust(wspace=0.3, hspace=.6)

    ax1.set_xlim(0, 30)
    # ax1.set_ylim(0, 1)
    # ax.set_yticks(np.arange(0, 3.1, 0.5))

    ax1.grid(which='both', axis='both')
    ax1.grid(which='minor', axis='both', linewidth=0.1, linestyle="--")
    # ax1.minorticks_on()
    # ax1.tick_params(axis='y', which='both', left=False)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("CDF")

    data = iter(times)
    
    for service in SERVICES:
        times = next(data).sort_values()
        cumu = np.linspace(1/times.size, 1, times.size)
        ax1.plot(
            times,
            cumu,
            label=service,
        )

    
    ax2.set_xlim(0, 55)
    # ax2.set_ylim(0, 1)
    ax2.grid(which='both', axis='both')
    ax2.grid(which='minor', axis='both', linewidth=0.1, linestyle="--")
    # ax2.minorticks_on()
    # ax2.tick_params(axis='y', which='both', left=False)

    # ax2.set_yticklabels([])
    ax2.set_xlabel("Time (s)")
    # ax2.set_ylabel("CDF")
    
    for service in SERVICES:
        times = next(data).sort_values()
        cumu = np.linspace(1/times.size, 1, times.size)
        ax2.plot(
            times,
            cumu,
            # label=service,
        )

    fig.legend(
         loc="upper left", mode="expand", borderaxespad=0, ncol=4, frameon=False
    )

    # fig.tight_layout()
    plt.savefig("startup/faas-startup-cdf.pdf", format="pdf", dpi=500)
