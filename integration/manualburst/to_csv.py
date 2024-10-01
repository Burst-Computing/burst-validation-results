import json
import pandas as pd

for i in range(1, 4):

    json0 = json.load(open(f'exec{i}/output_terasort_group-0.json'))
    json1 = json.load(open(f'exec{i}/output_terasort_group-1.json'))

    df0 = pd.DataFrame(json0)
    df1 = pd.DataFrame(json1)

    merged = pd.concat([df0, df1], axis=0)
    merged = merged.drop(['bucket', 'etag'], axis=1)
    merged['fn_id'] = range(0, len(merged))

    merged['host_submit'] = min(merged['init_fn'])

    merged.to_csv(f'output_terasort_{i}.csv', index=False)