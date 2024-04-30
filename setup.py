import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import os

# Crea un diccionario para mapear descuentos con distintos nombres pero mismo descuento
discount_map = {
    'precio fijo ': 'Precio Fijo',
    'Precio fijo': 'Precio Fijo',
    '2X1': '2x1',
    '2 x 1': '2x1',
    '2 X 1': '2x1',
    '1 + 1 BONIF ': '1 + 1 BONIF',
    '2do al 70': '2da al 70',
    '2do al 70%': '2da al 70',
    '2° al 70%': '2da al 70',
    '2do al 50': '2da al 50',
    '3 x 2': '3 X 2'
    # Agrega otros mapeos según sea necesario
}

# Función para cargar el archivo Excel
def cargar_excel():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
    if file_path:
        try:
            df = pd.read_excel(file_path)
            tk.messagebox.showinfo("Información", "Archivo cargado con exito.")
            
        except Exception as e:
            tk.messagebox.showerror("Error", "No se pudo cargar el archivo Excel. Asegúrate de seleccionar un archivo válido.")
            return
    else:
        tk.messagebox.showinfo("Información", "No se ha seleccionado ningún archivo.")

# Función para mostrar las opciones de descuento
def mostrar_descuentos():
    for discount in df['Descuento mostrador'].unique():
    # Convierte el descuento a minúsculas
        if discount is str:
            discount = discount.lower()

        # Verifica si el descuento está en el mapeo
        if discount in discount_map:
            # Reemplaza el descuento por el generico
            df.loc[df['Descuento mostrador'] == discount, 'Descuento mostrador'] = discount_map[discount]

    descuentos = df['Descuento mostrador'].unique()
    descuentos_str = [str(descuento) for descuento in descuentos]  # Convertir todos los elementos a cadenas
    descuentos_sorted = sorted(descuentos_str)
    messagebox.showinfo("Control opciones de Descuento", "\n".join(descuentos_sorted))  # Mostrar las opciones en una ventana emergente
        
        
# Función para generar archivos de texto
def writeNormal(discount, codes, observaciones, productos):
    nan_products = set()  # Utilizamos un conjunto para evitar duplicados

    with open(f'content/{discount}_discount.txt', 'w') as f_main:
        observation_files = {}  # Diccionario para almacenar los archivos de observaciones

        for i, (code, observacion, producto) in enumerate(zip(codes, observaciones, productos)):
            if pd.notnull(code):
                # Verifica si no es la última línea del mismo tipo de descuento y observación
                if i < len(codes) - 1 and observaciones[i] == observaciones[i+1]:
                    # Si hay una observación no nula
                    if not pd.isnull(observacion):
                        if observacion not in observation_files:
                            observation_files[observacion] = open(f'content/{discount}_{observacion}.txt', 'w')
                        observation_files[observacion].write(str(int(code)) + ';' + '\n')
                    else:
                        # Escribe el código en el archivo principal
                        f_main.write(str(int(code)) + ';' + '\n')
                else:
                    # Si es el último del tipo de descuento y observación
                    if not pd.isnull(observacion):
                        if observacion not in observation_files:
                            observation_files[observacion] = open(f'content/{discount}_{observacion}.txt', 'w')
                        observation_files[observacion].write(str(int(code)) + ';')
                    else:
                        # Escribe el código en el archivo principal
                        f_main.write(str(int(code)) + ';')
            else:
                nan_products.add(producto)

        # Cerrar los archivos de observaciones
        for file in observation_files.values():
            file.close()

    if nan_products:
        root = tk.Tk()
        root.withdraw()
        message = "El archivo tiene celdas importantes vacías en los siguientes productos:\n"
        for product in nan_products:
            message += f"{product}\n"
        messagebox.showinfo("Advertencia", message)

def writePrecioFijo(prices, codes, productos):
    has_empty_cell = False 
    nan_codes = [] 
    
    
    with open(f'content/PrecioFijoConPrecio_discount.txt', 'w') as f:
        # Itera sobre todos los códigos y precios al mismo tiempo
        for i, (code, price, producto) in enumerate(zip(codes, prices, productos)):
            if pd.notnull(price) or pd.notnull(code):
                if i < len(codes) - 1:  # Verifica si no es la última línea
                    f.write(str(code).rstrip(".0") + ';' + str(int(price)) + ';' + '\n') # Escribe el código y el precio con un salto de línea
                else:
                    f.write(str(code).rstrip(".0") + ';' + str(int(price)) + ';')   
            else: 
                has_empty_cell = True
                nan_codes.append(producto)
    if has_empty_cell:
        # Muestra el mensaje de advertencia si hay una celda vacía
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana principal de Tkinter
        message = "El archivo tiene una celda importante vacía en los siguientes códigos:\n"
        for code in set(nan_codes):
            message += f"{code}\n"
        messagebox.showinfo("Advertencia", message)



def generar_archivos():
            
    for discount in df['Descuento mostrador'].unique():
        df_filtered = df[df['Descuento mostrador'] == discount]
        codes = df_filtered['Codebar'].tolist()
        observaciones = df_filtered['Duracion propuesta'].tolist()
        productos = df_filtered['Producto'].tolist()
        precios = df_filtered['Precios fijos'].tolist()
        
        if discount == "Precio Fijo":
            # Se crean dos txts, uno solo con los codigos de barra y otro con los codigos y los precios
            writeNormal(discount, codes, observaciones, productos)
            writePrecioFijo(precios, codes, productos) 
        else:
            writeNormal(discount, codes, observaciones, productos)
            
    tk.messagebox.showinfo("Éxito", "Los archivos se han creado correctamente.")

# Función para eliminar archivos de texto
def eliminar_archivos():
    folder_path = "content"  
    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    for file in files:
        file_path = os.path.join(folder_path, file)  # Ruta completa del archivo a eliminar
        os.remove(file_path)
        
    tk.messagebox.showinfo("Éxito", "Archivos txt de la carpeta content eliminados con exito.")

# Función para cambiar el cursor al pasar sobre un botón
def cambiar_cursor(event):
    event.widget.config(cursor="hand2")

# Función para agregar un margin o espacio entre elementos
def generar_espacio():
    espacio_entre_botones = tk.Label(marco, text="", padx=5, pady=5)  
    espacio_entre_botones.pack()
    
# Crear la ventana principal
root = tk.Tk()
root.title("Gestor de Descuentos")

# Crear un marco
marco = tk.Frame(root, padx=20, pady=20)
marco.pack()

# Establecer el ancho y alto de la ventana principal
ancho_ventana = 400
alto_ventana = 370
x_ventana = (root.winfo_screenwidth() // 2) - (ancho_ventana // 2)
y_ventana = (root.winfo_screenheight() // 2) - (alto_ventana // 2)
root.geometry(f'{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}')

# Estilos 
button_style = {'font': ('Arial', 10), 'bg': 'lightgreen', 'fg': 'black', 'padx': 5, 'pady': 1}

# Crear un marco
marco = tk.Frame(root, padx=20, pady=20)
marco.pack()

# Botones para cargar, mostrar, generar y eliminar archivos
cargar_btn = tk.Button(marco, text="Cargar Excel", command=cargar_excel, **button_style)
cargar_btn.pack()
cargar_btn.bind("<Enter>", cambiar_cursor)

generar_espacio()

mostrar_btn = tk.Button(marco, text="Mostrar Descuentos", command=mostrar_descuentos, **button_style)
mostrar_btn.pack()
mostrar_btn.bind("<Enter>", cambiar_cursor)

generar_espacio()

generar_btn = tk.Button(marco, text="Generar Archivos de Texto", command=generar_archivos, **button_style)
generar_btn.pack()
generar_btn.bind("<Enter>", cambiar_cursor)

generar_espacio()

eliminar_btn = tk.Button(marco, text="Eliminar Archivos de Texto", command=eliminar_archivos, **button_style)
eliminar_btn.pack()
eliminar_btn.bind("<Enter>", cambiar_cursor)

generar_espacio()

root.mainloop()