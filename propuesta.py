import pandas as pd
import numpy as np

path = "content/Propuesta abril.xlsx"
df = pd.read_excel(path)
df
 

# Crea un diccionario para mapear descuentos en mayúsculas a descuentos en minúsculas
discount_map = {
    'precio fijo ': 'Precio Fijo',
    'Precio fijo': 'Precio Fijo',
    'Precio Fijo': 'Precio Fijo',
    '2x1': '2x1',
    '2X1': '2x1',
    '2 x 1': '2x1',
    '2 X 1': '2x1',

    # Agrega otros mapeos según sea necesario
}

# Itera sobre los descuentos únicos
for discount in df['Descuento'].unique():
    # Convierte el descuento a minúsculas
    if discount is str:
      discount = discount.lower()

    # Verifica si el descuento en minúsculas está en el mapeo
    if discount in discount_map:
        # Reemplaza el descuento en mayúsculas con el descuento en minúsculas
        df.loc[df['Descuento'] == discount, 'Descuento'] = discount_map[discount]

# Guarda el DataFrame actualizado en un nuevo archivo de Excel
df.to_excel('updated_Propuesta_abril.xlsx', index=False)

# Genera los archivos de texto para cada descuento
for discount in df['Descuento'].unique():
    df_filtered = df[df['Descuento'] == discount]
    codes = df_filtered['Codebar'].tolist()

    with open(f'content/{discount}_discount.txt', 'w') as f:
        # Itera sobre todos los códigos excepto el último
      for code in codes[:-1]:
        f.write(str(code) + ';' + '\n')

      # Escribe el último código sin añadir una nueva línea al final
      if codes:  # Verifica si la lista codes no está vacía
        f.write(str(codes[-1]) + ';')

# Prompt: borrar todos los archivos txt de la carpeta content

# !rm /content/*.txt

# Prompt: necesito ver todas las opciones de la columna descuento

df['Descuento'].unique()
