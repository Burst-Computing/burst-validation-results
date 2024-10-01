import pandas as pd
import numpy as np

# Lee el CSV existente
df = pd.read_csv('960/gran1.csv')

# Agrega una nueva columna llamada 'grupo_aleatorio' con valores aleatorios del grupo {0-9}
df['hostname'] = np.random.randint(0, 20, size=len(df))

# Guarda el DataFrame de nuevo en el archivo CSV
df.to_csv('960/gran1.csv', index=False)