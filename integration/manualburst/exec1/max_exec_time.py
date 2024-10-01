import pandas as pd

df1 = pd.read_csv('output_terasort_1.csv')
df2 = pd.read_csv('output_terasort_2.csv')
df3 = pd.read_csv('output_terasort_3.csv')

# get the max exec time and its index
max_exec_time = (df1['end_fn'] - df1['host_submit']).max()
max_exec_time2 = (df2['end_fn'] - df2['host_submit']).max()
max_exec_time3 = (df3['end_fn'] - df3['host_submit']).max()

print(f'Max exec time for exec1: {max_exec_time}')
print(f'Max exec time for exec2: {max_exec_time2}')
print(f'Max exec time for exec3: {max_exec_time3}')


