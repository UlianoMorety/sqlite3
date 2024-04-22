import sqlite3

# Conexión a la base de datos (crea un archivo "recetario.db")
conn = sqlite3.connect("recetario.db")
cursor = conn.cursor()
def crearTabla():
# Creación de la tabla "Categorías"
    cursor.execute("""
        CREATE TABLE if not exists Categorias (
            id INTEGER PRIMARY KEY,
            nombre TEXT
        )
    """)

    # Creación de la tabla "Recetas"
    cursor.execute("""
        CREATE TABLE if not exists Recetas (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            instrucciones TEXT,
            id_categoria INTEGER,
            FOREIGN KEY (id_categoria) REFERENCES Categorias(id)
        )
    """)

    # Creación de la tabla "Ingredientes"
    cursor.execute("""
        CREATE TABLE if not exists Ingredientes (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            unidad TEXT
        )
    """)

    # Creación de la tabla intermedia "Recetas_Ingredientes", para vincular las recetas con los ingredientes.
    cursor.execute("""
        CREATE TABLE if not exists Recetas_Ingredientes(
            id_receta INTEGER,
            id_ingrediente INTEGER,
            FOREIGN KEY (id_receta) REFERENCES Recetas(id),
            FOREIGN KEY (id_ingrediente) REFERENCES Ingredientes(id)
        )
    """)

    # Cierre de la conexión
    conn.close()

def  agregar_receta():
    
    # Apertura de la base de datos y creación de un cursor
    conn = sqlite3.connect('recetario.db')
    cursor = conn.cursor()
    
    # Inserción de los valores en la tabla "Recetas"
    nombre =input('Introduzca el nombre de la receta: ')
    instrucciones =input('Introduzca el las intrucciones de la receta: ')
    categoria = int(input('Indique a que categoría pertenece la receta (1-Entrantes, 2-Platos Principales, 3-Postres, 4-Otros)'))
    ID_Receta = cursor.execute("INSERT INTO recetas VALUES (?, ?, ?, ?)", (None, nombre, instrucciones, categoria)).lastrowid
    
    # Cierre de la conexión y regreso del id de la receta insertada
    conn.commit()

def actualizar_receta():
     # Apertura de la base de datos y creación de un cursor
    conn = sqlite3.connect('recetario.db')
    cursor = conn.cursor()

    # Actualizar receta
    receta_id=int(input('Ingrese el ID de la receta a editar: '))
    nombre = input('Nuevo nombre para la receta: ')
    nueva_instruccion = input('Nuevas instrucciones para la receta: ')

    # Verificamos si se quiere cambiar algo o solo mostrarlo
    accion = input('Desea ver los detalles de esta receta? s/n ')

    if accion =='s':
        print('\nDetalle de la receta:\n')
        print('ID: ', receta_id)
        print('Nombre: ',nombre)
        
        # Mostramos las instrucciones originales
        sql_query = "SELECT * FROM recetas WHERE id= ?" (receta_id,)
        registros = cursor.execute(sql_query).fetchall()
        for fila in registros:
            print('Instrucciones Originales: ',fila[1])
            
        # Si hay nuevas instrucciones las agregamos
        if nueva_instruccion!='':
            print("\nSe van a agregar las siguientes instrucciones")
            print(nueva_instruccion+'\n')

            # Agregando las instrucciones a la BDD
            instrucciones = fila[1]+ '\n'+nueva_instruccion
            cursor.execute("UPDATE Recetas SET Instrucciones=? WHERE id=?", (instrucciones,receta_id))

        else:
            print('No se han agregado nuevas instrucciones.\n')

        # Guardamos los cambios en la BDD y cerramos conexión
        conn.commit()

    elif accion=='n':
        print('\nSolo muestro los detalles de esta receta\n')
        print('ID: ', receta_id)
        print('Nombre: ',nombre)

def eliminar_receta():
    # Apertura de la base de datos y creación de un cursor
    conn = sqlite3.connect('recetario.db')
    cursor = conn.cursor()

    id_receta = int(input("ID de la receta a eliminar: "))
    conn.execute("DELETE FROM recetas WHERE id = ?", (id_receta,))
    conn.commit()
    print("Receta eliminada correctamente.")

def ver_recetas():
     # Apertura de la base de datos y creación de un cursor
    conn = sqlite3.connect('recetario.db')
    cursor = conn.cursor()

    # Función para ver el listado de recetas   
    cursor = conn.execute("SELECT id, nombre FROM Recetas")
    print("Listado de recetas:")
    for row in cursor:
        print(f"ID: {row[0]}, Nombre: {row[1]}")

def buscar_receta():
     # Apertura de la base de datos y creación de un cursor
    conn = sqlite3.connect('recetario.db')
    cursor = conn.cursor()

    # Función para buscar ingredientes y pasos de una receta
    palabra_clave = input("Ingrese palabra clave para buscar en ingredientes o instrucciones: ")
    cursor = conn.execute("SELECT id, nombre, instrucciones FROM recetas WHERE nombre LIKE ? OR instrucciones LIKE ?", ('%'+palabra_clave+'%', '%'+palabra_clave+'%'))
    print("Resultados de la búsqueda:")
    for row in cursor:
        print(f"ID: {row[0]}, Nombre: {row[1]}\ninstrucciones: {row[2]}\n")

# Función principal
def main():
    crearTabla()
   
    while True:
        print("\n--- Menú ---")
        print("a) Agregar nueva receta")
        print("c) Actualizar receta existente")
        print("d) Eliminar receta existente")
        print("e) Ver listado de recetas")
        print("f) Buscar ingredientes y pasos de receta")
        print("g) Salir")

        opcion = input("Seleccione una opción: ").lower()

        if opcion == 'a':
            agregar_receta()
        elif opcion == 'c':
            actualizar_receta()
        elif opcion == 'd':
            eliminar_receta()
        elif opcion == 'e':
            ver_recetas()
        elif opcion == 'f':
            buscar_receta()
        elif opcion == 'g':
            print("¡Hasta luego!")
            conn.close()
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    conn = sqlite3.connect('recetario.db')
    main()
    conn.close()
