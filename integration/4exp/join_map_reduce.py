import pandas as pd
import random

m = pd.read_csv('terasort-classic-onlymap3.csv')
r = pd.read_csv('terasort-classic-onlyreduce3.csv')

for i in range(len(m) - len(r)):
        j = int(random.random() * len(r))
        r.loc[len(r)] = r.loc[j].copy()
        r.reset_index(drop=True)
for i in range(192):
        r.at[i, 'fn_id'] = i

r['end_fn_reduce']
r['end_fn_reduce'].max()
m['end_fn_map'].max()
last = m['end_fn_map'].max()
first = r['host_submit_reduce'].min()
diff = first - last
diff = diff - 1500
r['host_submit_reduce'] = r['host_submit_reduce'] - diff
r['init_fn_reduce'] = r['init_fn_reduce'] - diff
r['post_download_reduce'] = r['post_download_reduce'] - diff
r['pre_upload_reduce'] = r['pre_upload_reduce'] - diff
r['end_fn_reduce'] = r['end_fn_reduce'] - diff
r['finished'] = r['finished'] - diff

merged = pd.concat([m, r], axis=1)
merged.to_csv('terasort-classic3.csv')
