import tkinter as tk
from tkinter import messagebox
from listas import ListaDoblementeEnlazada, ListaSimple

# Instancia global de la lista doblemente enlazada para las compras del usuario
lista_compras = ListaDoblementeEnlazada()

# Instancias de listas simples para los almacenes
almacen_1 = ListaSimple()
almacen_2 = ListaSimple()
almacen_3 = ListaSimple()

def show_user_menu(root):
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Compras", font=("Arial", 16)).pack(pady=10)
    
    # Controles para agregar/eliminar
    frame_controls = tk.Frame(root)
    frame_controls.pack(pady=5)
    tk.Label(frame_controls, text="Producto:").grid(row=0, column=0, padx=5)
    entrada_producto = tk.Entry(frame_controls)
    entrada_producto.grid(row=0, column=1, padx=5)
    
    # Listado en Interfaz
    tk.Label(root, text="Mi Lista de Compras:").pack()
    listbox_compras = tk.Listbox(root, width=60, height=10)
    listbox_compras.pack(pady=5)
    
    # Función local para actualizar la vista de la lista en la GUI
    def actualizar_lista():
        listbox_compras.delete(0, tk.END)  # Limpiar la tabla
        for producto in lista_compras.mostrar():
            listbox_compras.insert(tk.END, producto)  # Insertar todos los elementos de nuevo
            
    # Función que maneja el click de Agregar
    def agregar_producto():
        producto = entrada_producto.get().strip()
        if producto:
            lista_compras.agregar_al_final(producto)
            entrada_producto.delete(0, tk.END)  # Limpiar la entrada
            actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Ingrese el nombre del producto")

    # Función que maneja el click de Eliminar
    def eliminar_producto():
        seleccion = listbox_compras.curselection()
        if seleccion:
            # Eliminar el elemento que se seleccionó con el ratón
            producto = listbox_compras.get(seleccion[0])
            borrado = lista_compras.eliminar(producto)
            if borrado:
                actualizar_lista()
        else:
            # Eliminar el elemento escrito en el campo de texto
            producto = entrada_producto.get().strip()
            if producto:
                borrado = lista_compras.eliminar(producto)
                if borrado:
                    entrada_producto.delete(0, tk.END)
                    actualizar_lista()
                else:
                    messagebox.showwarning("No encontrado", "Ese producto no esta en la lista")
            else:
                messagebox.showwarning("Advertencia", "Seleccione un producto de la tabla o escriba su nombre para eliminarlo")

    # Botones que usan las funciones correspondientes
    tk.Button(frame_controls, text="Agregar", command=agregar_producto).grid(row=0, column=2, padx=5)
    tk.Button(frame_controls, text="Eliminar", command=eliminar_producto).grid(row=0, column=3, padx=5)
    
    # Carga inicial de elementos si la lista de compras ya tiene contenido
    actualizar_lista()

    # Controles para buscar
    frame_search = tk.Frame(root)
    
    frame_search.pack(pady=5)
    tk.Button(frame_search, text="Buscar en almacenes").grid(row=0, column=2, padx=5)
    
    tk.Label(root, text="Resultados de Búsqueda:").pack()
    tk.Listbox(root, width=60, height=4).pack(pady=5)

    tk.Button(root, text="Volver", command=lambda: main_menu(root), width=20).pack(pady=10)

def show_admin_menu(root):
    for widget in root.winfo_children():
        widget.destroy()
        
    tk.Label(root, text="Agregar productos", font=("Arial", 16)).pack(pady=10)
    
    # Controles de Agregar Producto
    frame_add = tk.Frame(root)
    frame_add.pack(pady=10)
    
    tk.Label(frame_add, text="Nombre:").grid(row=0, column=0, padx=5)
    entry_nombre = tk.Entry(frame_add)
    entry_nombre.grid(row=0, column=1, padx=5)
    
    tk.Label(frame_add, text="Precio:").grid(row=0, column=2, padx=5)
    entry_precio = tk.Entry(frame_add)
    entry_precio.grid(row=0, column=3, padx=5)
    
    tk.Label(frame_add, text="Almacen:").grid(row=0, column=4, padx=5)
    opciones = ["Almacen 1", "Almacen 2", "Almacen 3"]
    var_almacen = tk.StringVar(value=opciones[0])
    tk.OptionMenu(frame_add, var_almacen, *opciones).grid(row=0, column=5, padx=5)
    
    # Visualización de los 3 almacenes
    frame_lists = tk.Frame(root)
    frame_lists.pack(pady=10)
    
    tk.Label(frame_lists, text="Almacen 1").grid(row=0, column=0)
    listbox_a1 = tk.Listbox(frame_lists, height=15, width=25)
    listbox_a1.grid(row=1, column=0, padx=10)
    
    tk.Label(frame_lists, text="Almacen 2").grid(row=0, column=1)
    listbox_a2 = tk.Listbox(frame_lists, height=15, width=25)
    listbox_a2.grid(row=1, column=1, padx=10)
    
    tk.Label(frame_lists, text="Almacen 3").grid(row=0, column=2)
    listbox_a3 = tk.Listbox(frame_lists, height=15, width=25)
    listbox_a3.grid(row=1, column=2, padx=10)
    
    def actualizar_almacenes():
        listbox_a1.delete(0, tk.END)
        for p in almacen_1.mostrar(): listbox_a1.insert(tk.END, f"{p['nombre']} - ${p['precio']:.2f}")
        
        listbox_a2.delete(0, tk.END)
        for p in almacen_2.mostrar(): listbox_a2.insert(tk.END, f"{p['nombre']} - ${p['precio']:.2f}")
        
        listbox_a3.delete(0, tk.END)
        for p in almacen_3.mostrar(): listbox_a3.insert(tk.END, f"{p['nombre']} - ${p['precio']:.2f}")

    def agregar_producto_admin():
        nombre = entry_nombre.get().strip()
        precio_str = entry_precio.get().strip()
        if not nombre or not precio_str:
            messagebox.showwarning("Advertencia", "Ingrese nombre y precio")
            return
            
        try:
            precio = float(precio_str)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un valor numérico")
            return
            
        producto_obj = {"nombre": nombre, "precio": precio}
        almacen_sel = var_almacen.get()
        
        if almacen_sel == "Almacen 1":
            almacen_1.agregar(producto_obj)
        elif almacen_sel == "Almacen 2":
            almacen_2.agregar(producto_obj)
        elif almacen_sel == "Almacen 3":
            almacen_3.agregar(producto_obj)
            
        entry_nombre.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        actualizar_almacenes()

    tk.Button(frame_add, text="Agregar", command=agregar_producto_admin).grid(row=0, column=6, padx=5)
    
    actualizar_almacenes()
    
    tk.Button(root, text="Volver", command=lambda: main_menu(root), width=20).pack(pady=10)

def prompt_admin_password(root):
    for widget in root.winfo_children():
        widget.destroy()
        
    tk.Label(root, text="Acceso de Administrador", font=("Arial", 16)).pack(pady=20)
    tk.Label(root, text="Ingrese la clave:").pack(pady=5)
    
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)
    
    def check_password():
        if password_entry.get() == "admin123":  # Clave de ejemplo
            show_admin_menu(root)
        else:
            messagebox.showerror("Error", "Clave incorrecta")
            
    tk.Button(root, text="Ingresar", command=check_password, width=20).pack(pady=10)
    tk.Button(root, text="Volver", command=lambda: main_menu(root), width=20).pack(pady=5)

def main_menu(root):
    for widget in root.winfo_children():
        widget.destroy()
        
    tk.Label(root, text="Seleccione su Perfil", font=("Arial", 16)).pack(pady=20)
    tk.Button(root, text="Usuario", command=lambda: show_user_menu(root), width=20, height=2).pack(pady=10)
    tk.Button(root, text="Administrador", command=lambda: prompt_admin_password(root), width=20, height=2).pack(pady=10)

def main():
    root = tk.Tk()
    root.title("Asistente de Compras")
    root.geometry("800x600")
    
    main_menu(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
