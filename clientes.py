import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Conectar a la base de datos
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Woodkid35712/",
        database="clientesdb"
    )

# Función para refrescar la tabla con los usuarios actuales
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    connection = connect_db()
    cursor = connection.cursor()

    query = "SELECT * FROM usuarios"
    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        tree.insert("", tk.END, values=row)

    cursor.close()
    connection.close()

# Función para crear un usuario
def create_user():
    nombres = entry_nombres.get()
    apellidos = entry_apellidos.get()
    sexo = combobox_sexo.get()

    if not (nombres and apellidos and sexo):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    query = "INSERT INTO usuarios (nombres, apellidos, sexo) VALUES (%s, %s, %s)"
    values = (nombres, apellidos, sexo)
    cursor.execute(query, values)
    connection.commit()

    messagebox.showinfo("Éxito", f"Usuario {nombres} {apellidos} agregado con éxito.")
    
    cursor.close()
    connection.close()
    clear_entries()
    refresh_table()

# Función para actualizar un usuario
def update_user():
    user_id = entry_id.get()
    nuevos_nombres = entry_nombres.get()
    nuevos_apellidos = entry_apellidos.get()
    nuevo_sexo = combobox_sexo.get()

    if not (user_id and nuevos_nombres and nuevos_apellidos and nuevo_sexo):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    query = "UPDATE usuarios SET nombres = %s, apellidos = %s, sexo = %s WHERE id = %s"
    values = (nuevos_nombres, nuevos_apellidos, nuevo_sexo, user_id)
    cursor.execute(query, values)
    connection.commit()

    messagebox.showinfo("Éxito", f"Usuario con ID {user_id} actualizado con éxito.")

    cursor.close()
    connection.close()
    clear_entries()
    refresh_table()

# Función para eliminar un usuario
def delete_user():
    user_id = entry_id.get()

    if not user_id:
        messagebox.showerror("Error", "El ID es obligatorio.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    query = "DELETE FROM usuarios WHERE id = %s"
    cursor.execute(query, (user_id,))
    connection.commit()

    messagebox.showinfo("Éxito", f"Usuario con ID {user_id} eliminado con éxito.")

    cursor.close()
    connection.close()
    clear_entries()
    refresh_table()

# Limpiar los campos de entrada
def clear_entries():
    entry_id.delete(0, tk.END)
    entry_nombres.delete(0, tk.END)
    entry_apellidos.delete(0, tk.END)
    combobox_sexo.set('')

# Crear la ventana principal
window = tk.Tk()
window.title("CRUD Usuarios - Tkinter")
window.geometry("600x400")

# Frame izquierdo para los formularios CRUD
frame_form = tk.Frame(window)
frame_form.pack(side=tk.LEFT, padx=10, pady=10)

# Etiquetas y campos de entrada
label_id = tk.Label(frame_form, text="ID (para actualizar/eliminar)")
label_id.pack(pady=5)
entry_id = tk.Entry(frame_form)
entry_id.pack(pady=5)

label_nombres = tk.Label(frame_form, text="Nombres")
label_nombres.pack(pady=5)
entry_nombres = tk.Entry(frame_form)
entry_nombres.pack(pady=5)

label_apellidos = tk.Label(frame_form, text="Apellidos")
label_apellidos.pack(pady=5)
entry_apellidos = tk.Entry(frame_form)
entry_apellidos.pack(pady=5)

# Menú desplegable para seleccionar Sexo (M/F)
label_sexo = tk.Label(frame_form, text="Sexo")
label_sexo.pack(pady=5)
combobox_sexo = ttk.Combobox(frame_form, values=["Masculino", "Femenino"])
combobox_sexo.pack(pady=5)

# Botones de acciones CRUD
btn_create = tk.Button(frame_form, text="Crear", command=create_user)
btn_create.pack(pady=5)

btn_update = tk.Button(frame_form, text="Actualizar", command=update_user)
btn_update.pack(pady=5)

btn_delete = tk.Button(frame_form, text="Eliminar", command=delete_user)
btn_delete.pack(pady=5)

# Frame derecho para la tabla de usuarios
frame_table = tk.Frame(window)
frame_table.pack(side=tk.RIGHT, padx=10, pady=10)

# Definir las columnas de la tabla
columns = ("ID", "Nombres", "Apellidos", "Sexo")

# Crear la tabla (Treeview)
tree = ttk.Treeview(frame_table, columns=columns, show="headings")
tree.heading("ID", text="ID")
tree.heading("Nombres", text="Nombres")
tree.heading("Apellidos", text="Apellidos")
tree.heading("Sexo", text="Sexo")

# Ajustar el tamaño de las columnas
tree.column("ID", width=50)
tree.column("Nombres", width=100)
tree.column("Apellidos", width=100)
tree.column("Sexo", width=50)

# Agregar barra de desplazamiento a la tabla
scrollbar = ttk.Scrollbar(frame_table, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree.pack()

# Refrescar la tabla al iniciar la aplicación
refresh_table()

# Ejecutar la ventana principal
window.mainloop()
