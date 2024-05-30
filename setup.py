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
            messagebox.showinfo("Información", "Archivo cargado con éxito.")
        except Exception as e:
            messagebox.showerror("Error", "No se pudo cargar el archivo Excel. Asegúrate de seleccionar un archivo válido.")
            return
    else:
        messagebox.showinfo("Información", "No se ha seleccionado ningún archivo.")


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
    nan_products = set() 
    
    # Crear el directorio 'content' si no existe
    if not os.path.exists('content'):
        os.makedirs('content')
    
    main_file_path = f'content/{discount}_discount.txt'
    obs_file_path = f'content/{discount}_observaciones.txt'
    
    with open(main_file_path, 'w') as f_main, open(obs_file_path, 'w') as f_obs:
    # Itera sobre todos los códigos excepto el último
        for i, (code, observacion, producto) in enumerate(zip(codes, observaciones, productos)):
            if pd.notnull(code):
                if not pd.isnull(observacion):
                    if i < len(codes) - 1:
                        f_obs.write(f'{str(int(code))};\n')
                    else:
                        f_obs.write(f'{str(int(code))};')
                else:
                    if i < len(codes) - 1:
                        f_main.write(f'{str(int(code))};\n')
                    else:
                        f_main.write(f'{str(int(code))};')
            else:
                nan_products.add(producto)
    
    # Eliminar archivos si están vacíos
    if os.path.getsize(main_file_path) == 0:
        os.remove(main_file_path)
    if os.path.getsize(obs_file_path) == 0:
        os.remove(obs_file_path)
        
    if nan_products:
        message = "El archivo tiene celdas importantes vacías en los siguientes productos:\n" + "\n".join(nan_products)
        messagebox.showinfo("Advertencia", message)

def writePrecioFijo(df_filtered, codes, productos):
    nan_products = set()
    
    # Crear el directorio 'content' si no existe
    if not os.path.exists('content'):
        os.makedirs('content')
        
    prices = df_filtered['Precios fijos'].tolist()
    file_path = f'content/PrecioFijoConPrecio_discount.txt'
    
    with open(file_path, 'w') as f:
        for i, (code, price, producto) in enumerate(zip(codes, prices, productos)):
            if pd.notnull(code) and pd.notnull(price):
                if i < len(codes) - 1:
                    f.write(f'{code};{price};\n')
                else:
                    f.write(f'{code};{price};')
            else:
                nan_products.add(producto)
    
    # Eliminar archivo si está vacío
    if os.path.getsize(file_path) == 0:
        os.remove(file_path)
    
    if nan_products:
        message = "El archivo tiene celdas importantes vacías en los siguientes productos:\n" + "\n".join(nan_products)
        messagebox.showinfo("Advertencia", message)
        
        
def generar_archivos():
    for discount in df['Descuento mostrador'].unique():
        df_filtered = df[df['Descuento mostrador'] == discount]
        codes = df_filtered['Codebar'].tolist()
        observaciones = df_filtered['Observaciones'].tolist()
        productos = df_filtered['Producto'].tolist()
        
        if discount == "Precio Fijo":
            # Se crean dos txts, uno solo con los codigos de barra y otro con los codigos y los precios
            writeNormal(discount, codes, observaciones, productos)
            writePrecioFijo(df_filtered, codes, productos) 
        else:
            writeNormal(discount, codes, observaciones, productos)
    tk.messagebox.showinfo("Éxito", "Los archivos se han CREADO correctamente.")

# Función para eliminar archivos de texto
def eliminar_archivos():
    # Crear el directorio 'content' si no existe
    if not os.path.exists('content'):
        os.makedirs('content')
        
    folder_path = "content"  
    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    for file in files:
        file_path = os.path.join(folder_path, file)  # Ruta completa del archivo a eliminar
        os.remove(file_path)
    tk.messagebox.showinfo("Éxito", "Los archivos se han ELIMINADO correctamente.")
    

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
alto_ventana = 270
x_ventana = (root.winfo_screenwidth() // 2) - (ancho_ventana // 2)
y_ventana = (root.winfo_screenheight() // 2) - (alto_ventana // 2)
root.geometry(f'{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}')

# Estilos 
def get_button_style(bg_color):
    return {'font': ('Arial', 10), 'bg': bg_color, 'fg': 'black', 'padx': 5, 'pady': 1}

# Crear un marco
marco = tk.Frame(root, padx=20, pady=20)
marco.pack()

# Botones para cargar, mostrar, generar y eliminar archivos
cargar_btn = tk.Button(marco, text="Cargar Excel", command=cargar_excel, **get_button_style('lightgreen'))
cargar_btn.pack()
cargar_btn.bind("<Enter>", cambiar_cursor)

generar_espacio()

mostrar_btn = tk.Button(marco, text="Mostrar Descuentos", command=mostrar_descuentos, **get_button_style('lightblue'))
mostrar_btn.pack()
mostrar_btn.bind("<Enter>", cambiar_cursor)

generar_espacio()

generar_btn = tk.Button(marco, text="Generar Archivos de Texto", command=generar_archivos, **get_button_style('lightgreen'))
generar_btn.pack()
generar_btn.bind("<Enter>", cambiar_cursor)

generar_espacio()

eliminar_btn = tk.Button(marco, text="Eliminar Archivos de Texto", command=eliminar_archivos, **get_button_style('firebrick2'))
eliminar_btn.pack()
eliminar_btn.bind("<Enter>", cambiar_cursor)

generar_espacio()

root.mainloop()