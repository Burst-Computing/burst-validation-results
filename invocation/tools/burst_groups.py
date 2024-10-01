import pandas as pd
import numpy as np

# Lee el CSV existente
df = pd.read_csv('960/gran48.csv')

num_groups=20
# new column with random values from {0..num_groups-1}. firsts 48 rows are 0, next 48 are 1, etc. 
df['hostname'] = np.repeat(np.arange(num_groups), len(df)/num_groups)

# Guarda el DataFrame de nuevo en el archivo CSV
df.to_csv('960/gran48.csv', index=False)