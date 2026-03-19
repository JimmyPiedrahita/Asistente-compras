import tkinter as tk
from tkinter import ttk, messagebox
from listas import ListaDoblementeEnlazada, ListaSimple

# Instancia global de la lista doblemente enlazada para las compras del usuario
lista_compras = ListaDoblementeEnlazada()

# Instancias de listas simples para los almacenes
almacen_1 = ListaSimple()
almacen_2 = ListaSimple()
almacen_3 = ListaSimple()

# Colores y fuentes
BG_COLOR = "#f4f4f9"
PRIMARY_COLOR = "#4a90e2"
SECONDARY_COLOR = "#333333"
FONT_TITLE = ("Helvetica", 20, "bold")
FONT_NORMAL = ("Helvetica", 12)

def show_user_menu(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg=BG_COLOR)
    
    # Header
    header = tk.Frame(root, bg=PRIMARY_COLOR)
    header.pack(fill=tk.X)
    tk.Label(header, text="Compras - Usuario", font=FONT_TITLE, bg=PRIMARY_COLOR, fg="white", pady=15).pack()
    
    # Body
    body = tk.Frame(root, bg=BG_COLOR)
    body.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
    
    # Top controls
    frame_controls = tk.Frame(body, bg=BG_COLOR)
    frame_controls.pack(pady=10)
    tk.Label(frame_controls, text="Nuevo Producto:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=0, column=0, padx=5)
    entrada_producto = ttk.Entry(frame_controls, font=FONT_NORMAL, width=25)
    entrada_producto.grid(row=0, column=1, padx=10)
    
    # List box frame
    frame_list = tk.Frame(body, bg=BG_COLOR)
    frame_list.pack(pady=5, fill=tk.X)
    tk.Label(frame_list, text="Mi Lista de Compras:", font=("Helvetica", 14, "bold"), bg=BG_COLOR).pack(anchor="w")
    listbox_compras = tk.Listbox(frame_list, font=FONT_NORMAL, height=6, bg="white", selectbackground=PRIMARY_COLOR)
    listbox_compras.pack(fill=tk.X, pady=5)
    
    def actualizar_lista():
        listbox_compras.delete(0, tk.END)
        for producto in lista_compras.mostrar():
            listbox_compras.insert(tk.END, producto)
            
    def agregar_producto():
        producto = entrada_producto.get().strip()
        if producto:
            lista_compras.agregar_al_final(producto)
            entrada_producto.delete(0, tk.END)
            actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Ingrese el nombre del producto")

    def eliminar_producto():
        seleccion = listbox_compras.curselection()
        if seleccion:
            producto = listbox_compras.get(seleccion[0])
            borrado = lista_compras.eliminar(producto)
            if borrado: actualizar_lista()
        else:
            producto = entrada_producto.get().strip()
            if producto:
                borrado = lista_compras.eliminar(producto)
                if borrado:
                    entrada_producto.delete(0, tk.END)
                    actualizar_lista()
                else:
                    messagebox.showwarning("No encontrado", "Ese producto no esta en la lista")
            else:
                messagebox.showwarning("Advertencia", "Seleccione un producto o nombre para eliminar")

    ttk.Button(frame_controls, text="Agregar", command=agregar_producto).grid(row=0, column=2, padx=5)
    ttk.Button(frame_controls, text="Eliminar", command=eliminar_producto).grid(row=0, column=3, padx=5)
    
    actualizar_lista()

    def buscar_mejor_precio():
        res_a1, res_a2, res_a3 = ListaSimple(), ListaSimple(), ListaSimple()

        for producto in lista_compras.mostrar():
            p_lower = producto.lower()
            mejor_almacen, mejor_precio = None, float('inf')

            for p1 in almacen_1.mostrar():
                if p1["nombre"].lower() == p_lower and p1["precio"] < mejor_precio:
                    mejor_precio = p1["precio"]
                    mejor_almacen = 1

            for p2 in almacen_2.mostrar():
                if p2["nombre"].lower() == p_lower and p2["precio"] < mejor_precio:
                    mejor_precio = p2["precio"]
                    mejor_almacen = 2

            for p3 in almacen_3.mostrar():
                if p3["nombre"].lower() == p_lower and p3["precio"] < mejor_precio:
                    mejor_precio = p3["precio"]
                    mejor_almacen = 3

            if mejor_almacen == 1: res_a1.agregar({"nombre": producto, "precio": mejor_precio})
            elif mejor_almacen == 2: res_a2.agregar({"nombre": producto, "precio": mejor_precio})
            elif mejor_almacen == 3: res_a3.agregar({"nombre": producto, "precio": mejor_precio})

        listbox_resultados.delete(0, tk.END)

        if not res_a1.esta_vacia():
            listbox_resultados.insert(tk.END, "--- Almacen 1 ---")
            for p in res_a1.mostrar(): listbox_resultados.insert(tk.END, f"  {p['nombre']} - ${p['precio']:.2f}")
        
        if not res_a2.esta_vacia():
            listbox_resultados.insert(tk.END, "--- Almacen 2 ---")
            for p in res_a2.mostrar(): listbox_resultados.insert(tk.END, f"  {p['nombre']} - ${p['precio']:.2f}")

        if not res_a3.esta_vacia():
            listbox_resultados.insert(tk.END, "--- Almacen 3 ---")
            for p in res_a3.mostrar(): listbox_resultados.insert(tk.END, f"  {p['nombre']} - ${p['precio']:.2f}")

    tk.Label(body, text="Resultados de Busqueda:", font=("Helvetica", 14, "bold"), bg=BG_COLOR).pack(anchor="w", pady=(20,0))
    ttk.Button(body, text="Buscar mejores precios", command=buscar_mejor_precio).pack(pady=5, anchor="w")
    
    listbox_resultados = tk.Listbox(body, font=("Consolas", 11), height=8, bg="#eef2f5")
    listbox_resultados.pack(fill=tk.X, pady=5)

    ttk.Button(body, text="Volver al Menu", command=lambda: main_menu(root)).pack(pady=10)

def show_admin_menu(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg=BG_COLOR)
        
    header = tk.Frame(root, bg=PRIMARY_COLOR)
    header.pack(fill=tk.X)
    tk.Label(header, text="Panel de Administracion", font=FONT_TITLE, bg=PRIMARY_COLOR, fg="white", pady=15).pack()
    
    body = tk.Frame(root, bg=BG_COLOR)
    body.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
    
    # Add form
    frame_add = ttk.LabelFrame(body, text="Agregar Nuevo Producto en Almacen")
    frame_add.pack(pady=10, fill=tk.X)
    
    tk.Label(frame_add, text="Nombre:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=0, column=0, padx=10, pady=10)
    entry_nombre = ttk.Entry(frame_add, font=FONT_NORMAL, width=15)
    entry_nombre.grid(row=0, column=1)
    
    tk.Label(frame_add, text="Precio:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=0, column=2, padx=10, pady=10)
    entry_precio = ttk.Entry(frame_add, font=FONT_NORMAL, width=8)
    entry_precio.grid(row=0, column=3)
    
    tk.Label(frame_add, text="Almacen:", font=FONT_NORMAL, bg=BG_COLOR).grid(row=0, column=4, padx=10, pady=10)
    opciones = ["Almacen 1", "Almacen 2", "Almacen 3"]
    var_almacen = tk.StringVar(value=opciones[0])
    ttk.OptionMenu(frame_add, var_almacen, opciones[0], *opciones).grid(row=0, column=5)
    
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
            messagebox.showerror("Error", "Precio numerico")
            return
        producto_obj = {"nombre": nombre, "precio": precio}
        alm = var_almacen.get()
        if alm == "Almacen 1": almacen_1.agregar(producto_obj)
        elif alm == "Almacen 2": almacen_2.agregar(producto_obj)
        elif alm == "Almacen 3": almacen_3.agregar(producto_obj)
            
        entry_nombre.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        actualizar_almacenes()

    ttk.Button(frame_add, text="Guardar", command=agregar_producto_admin).grid(row=0, column=6, padx=15)
    
    # Visualizacion almacenes
    tk.Label(body, text="Inventario de Almacenes:", font=("Helvetica", 14, "bold"), bg=BG_COLOR).pack(anchor="w", pady=5)
    frame_lists = tk.Frame(body, bg=BG_COLOR)
    frame_lists.pack(fill=tk.BOTH, expand=True)
    frame_lists.columnconfigure(0, weight=1)
    frame_lists.columnconfigure(1, weight=1)
    frame_lists.columnconfigure(2, weight=1)
    
    tk.Label(frame_lists, text="Almacen 1", bg=BG_COLOR, font=FONT_NORMAL).grid(row=0, column=0, pady=5)
    listbox_a1 = tk.Listbox(frame_lists, font=("Consolas", 10), height=12)
    listbox_a1.grid(row=1, column=0, padx=5, sticky="nsew")
    
    tk.Label(frame_lists, text="Almacen 2", bg=BG_COLOR, font=FONT_NORMAL).grid(row=0, column=1, pady=5)
    listbox_a2 = tk.Listbox(frame_lists, font=("Consolas", 10), height=12)
    listbox_a2.grid(row=1, column=1, padx=5, sticky="nsew")
    
    tk.Label(frame_lists, text="Almacen 3", bg=BG_COLOR, font=FONT_NORMAL).grid(row=0, column=2, pady=5)
    listbox_a3 = tk.Listbox(frame_lists, font=("Consolas", 10), height=12)
    listbox_a3.grid(row=1, column=2, padx=5, sticky="nsew")
    
    actualizar_almacenes()
    ttk.Button(body, text="Volver al Menu", command=lambda: main_menu(root)).pack(pady=15)

def prompt_admin_password(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg=BG_COLOR)
        
    frame_login = tk.Frame(root, bg="white", padx=40, pady=40, relief="groove", bd=2)
    frame_login.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(frame_login, text="Admin", font=FONT_TITLE, bg="white").pack(pady=(0, 20))
    tk.Label(frame_login, text="Clave de acceso:", font=FONT_NORMAL, bg="white").pack()
    
    password_entry = ttk.Entry(frame_login, show="*", font=FONT_NORMAL)
    password_entry.pack(pady=10)
    password_entry.focus()
    
    def check_password(event=None):
        if password_entry.get() == "admin123":
            show_admin_menu(root)
        else:
            messagebox.showerror("Error", "Clave incorrecta")
            
    root.bind('<Return>', check_password)
    
    ttk.Button(frame_login, text="Ingresar", command=check_password).pack(pady=5, fill=tk.X)
    ttk.Button(frame_login, text="Cancelar", command=lambda: main_menu(root)).pack(fill=tk.X)

def main_menu(root):
    root.unbind('<Return>')
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg=BG_COLOR)
    
    # Welcome hero
    hero = tk.Frame(root, bg=PRIMARY_COLOR, height=150)
    hero.pack(fill=tk.X)
    hero.pack_propagate(False)
    
    tk.Label(hero, text="Asistente de Compras", font=("Helvetica", 28, "bold"), fg="white", bg=PRIMARY_COLOR).pack(expand=True)
    
    body = tk.Frame(root, bg=BG_COLOR)
    body.pack(expand=True, fill=tk.BOTH)
    
    cards_frame = tk.Frame(body, bg=BG_COLOR)
    cards_frame.place(relx=0.5, rely=0.4, anchor="center")
    
    tk.Label(cards_frame, text="Seleccione su Perfil", font=("Helvetica", 16), bg=BG_COLOR).pack(pady=20)
    
    s = ttk.Style()
    s.configure("Action.TButton", font=("Helvetica", 12, "bold"), padding=10)
    
    ttk.Button(cards_frame, text="Ingresar como Usuario", command=lambda: show_user_menu(root), style="Action.TButton", width=25).pack(pady=10)
    ttk.Button(cards_frame, text="Administrar Almacenes", command=lambda: prompt_admin_password(root), style="Action.TButton", width=25).pack(pady=10)

def main():
    root = tk.Tk()
    root.title("Asistente de Compras Inteligente")
    root.geometry("850x650")
    
    # Configure styling
    style = ttk.Style(root)
    style.theme_use('clam')
    
    main_menu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
