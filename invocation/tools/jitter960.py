import pandas as pd
import numpy as np

for i in [2,4,6,12,24]:
    # Lee el CSV existente
    df = pd.read_csv(f'960/gran{str(i)}.csv')

    # I want to add 0.2 to each value in the column "worker_start_tstamp"
    df['worker_start_tstamp'] = df['worker_start_tstamp'] + 0.2

    # I want to jitter the values in the column "worker_start_tstamp" by 0.3
    df['worker_start_tstamp'] = df['worker_start_tstamp'] + np.random.uniform(-0.3, 0.3, len(df))

    df.to_csv(f'960syn/gran{i}.csv', index=False)