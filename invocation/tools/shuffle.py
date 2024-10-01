import pandas as pd
import numpy as np

# Cargar el archivo CSV original
original_data = pd.read_csv('960.csv')
# Dividir los datos en grupos de 48 filas
grouped_data = [group.reset_index(drop=True) for _, group in original_data.groupby((np.arange(len(original_data)) +1) // 48)]

# Barajar los grupos
shuffled_indices = np.random.permutation(len(grouped_data))
shuffled_groups = [grouped_data[i] for i in shuffled_indices]

# Concatenar los grupos barajados
final_data = pd.concat(shuffled_groups, ignore_index=True)

# Guardar el resultado en un nuevo archivo CSV
final_data.to_csv('960.csv', index=False)
