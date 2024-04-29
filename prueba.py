import tkinter as tk

# Crear una ventana
ventana = tk.Tk()
ventana.title("Ejemplo de Separación entre Botones")

# Crear un marco
marco = tk.Frame(ventana, padx=20, pady=20)
marco.pack()

# Crear un botón
boton1 = tk.Button(marco, text="Botón 1", padx=10, pady=5)
boton1.pack()

# Agregar espacio entre los botones
espacio_entre_botones = tk.Label(marco, text="", padx=5, pady=5)  
espacio_entre_botones.pack()

# Crear otro botón
boton2 = tk.Button(marco, text="Botón 2", padx=10, pady=5)
boton2.pack()

# Ejecutar el bucle de eventos
ventana.mainloop()
