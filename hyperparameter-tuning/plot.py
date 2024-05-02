import matplotlib.pyplot as plt
import numpy as np
import os
import json
import pandas as pd

GRANULARITY_1_DIR = "hyperparameter-tuning/results-noOW/bs-96-g-1/"
GRANULARITY_MAX_DIR = "hyperparameter-tuning/results-noOW/bs-96-g-96/"

if __name__ == "__main__":
    workers_data = []
    files = os.listdir(GRANULARITY_1_DIR)
    for file in files:
        with open(os.path.join(GRANULARITY_1_DIR, file), "r") as f:
            data = json.load(f)
            workers_data.extend(data)

    g1_df = pd.DataFrame.from_records(workers_data)
    for col in g1_df.columns:
        if g1_df[col].dtype == "object":
            g1_df[col] = pd.to_numeric(g1_df[col], errors="coerce")

    print(pd.to_numeric(g1_df["input_gathered"], errors="coerce"))

    g1_t0 = g1_df["init_fn"].min() / 1000
    g1_t = (g1_df["input_gathered"] / 1000) - g1_t0

    files = os.listdir(GRANULARITY_MAX_DIR)
    workers_data = []
    for file in files:
        with open(os.path.join(GRANULARITY_MAX_DIR, file), "r") as f:
            data = json.load(f)
            workers_data.extend(data)

    gmax_df = pd.DataFrame.from_dict(workers_data)
    for col in gmax_df.columns:
        if gmax_df[col].dtype == "object":
            gmax_df[col] = pd.to_numeric(gmax_df[col], errors="coerce")

    gmax_t0 = gmax_df["init_fn"].min() / 1000
    gmax_t = (gmax_df["input_gathered"] / 1000) - gmax_t0

    fig, ax = plt.subplots()
    ax.boxplot([g1_t, gmax_t], labels=["Granularity 1", "Granularity Max"])

    ax.set_title("Time to gather input data")
    ax.set_ylabel("Time (s)")

    fig.tight_layout()
    plt.savefig("hyperparameter-tuning/input-gathered.png")

    # print(g1_df)
    # print(gmax_df)
