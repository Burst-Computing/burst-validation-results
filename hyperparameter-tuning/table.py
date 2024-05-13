import os
import json
import pandas as pd

from tabulate import tabulate

GRANULARITIES = [1, 6, 12, 24, 48, 96]

INIT_TIMES_OW = {
    6: 2.675213,
    12: 2.131605,
    24: 1.887219,
    48: 1.768838,
    96: 1.508818,
}

def load_data(granularity):
    directory = f"hyperparameter-tuning/results-noOW/bs-96-g-{granularity}/"
    workers_data = []
    files = os.listdir(directory)
    for file in files:
        with open(os.path.join(directory, file), "r") as f:
            for d in json.load(f):
                if granularity == 1:
                    host_submit_tstamp = d[0]["host_submit_tstamp"]
                    d = d[1]
                else:
                    host_submit_tstamp = int(d["init_fn"]) / 1000 - INIT_TIMES_OW[granularity]
                input_gathered = int(d["input_gathered"]) / 1000
                donwload_time = (int(d["input_gathered"]) - int(d["init_fn"])) / 1000
                workers_data.append({
                    "host_submit_tstamp": host_submit_tstamp,
                    "input_gathered": input_gathered,
                    "download_time": donwload_time
                })
    return pd.DataFrame.from_records(workers_data)

if __name__ == "__main__":
    table = []
    # Table for each granularity with 2 columns: download time and input gathering time
    for granularity in GRANULARITIES:
        df = load_data(granularity)
        download_time = df["download_time"].max()
        input_gathered = df["input_gathered"] - df["host_submit_tstamp"]
        input_gathered = input_gathered.max()
        table.append([granularity, download_time, input_gathered])
    print(tabulate(table, headers=[
        "Granularity", "Download Time (s)", "Input Gathering Time (s)"], tablefmt="latex"))
