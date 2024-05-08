import matplotlib.pyplot as plt
import numpy as np
import os
import json
import pandas as pd

GRANULARITIES = [1, 6, 12, 24, 48, 96]

def load_data(granularity):
    directory = f"hyperparameter-tuning/results-noOW/bs-96-g-{granularity}/"
    workers_data = []
    files = os.listdir(directory)
    for file in files:
        with open(os.path.join(directory, file), "r") as f:
            data = json.load(f)
            workers_data.extend(data)
    df = pd.DataFrame.from_records(workers_data)
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = pd.to_numeric(df[col], errors="coerce")
    t0 = df["init_fn"].min() / 1000
    t = (df["input_gathered"] / 1000) - t0
    return t

if __name__ == "__main__":
    data_to_plot = []
    labels = []
    for granularity in GRANULARITIES:
        t = load_data(granularity)
        data_to_plot.append(t)
        labels.append(f"g={granularity}")

    fig, ax = plt.subplots()
    ax.boxplot(data_to_plot, labels=labels)

    ax.set_title("Time to gather input data")
    ax.set_ylabel("Time (s)")

    fig.tight_layout()
    plt.savefig("hyperparameter-tuning/input-gathered.png")
