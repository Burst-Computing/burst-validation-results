import csv
import random
import string

def generate_random_data(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

def generate_csv_file(file_path, num_rows, row_size):
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Escribir encabezados (opcional)
        csv_writer.writerow(['Columna1', 'Columna2', 'Columna3'])  # Reemplaza con tus nombres de columnas
        for _ in range(num_rows):
            row = [generate_random_data(row_size) for _ in range(3)]  # Reemplaza '3' con el número de columnas
            csv_writer.writerow(row)

if __name__ == "__main__":
    file_path = "archivo_grande.csv"
    num_rows = 10  # Número de filas
    row_size = 1024  # Tamaño de cada celda en bytes

    generate_csv_file(file_path, num_rows, row_size)
    print(f"Archivo CSV generado en: {file_path}")
