import psycopg2

# Función para conectarse a la base de datos
def connect():
    conn = psycopg2.connect(
        host="localhost",
        database="Lab11",
        user="postgres",
        password="Diego2250"
    )
    return conn

# Función 1
def search_pc(velocidad, ram):
    try:
        conn = connect()
        cur = conn.cursor()
        
        # Inicia la transacción
        cur.execute("BEGIN;")
        
        # Busca las PCs con la velocidad y RAM especificadas
        cur.execute("SELECT modelo, precio FROM PC WHERE velocidad = %s AND ram = %s;", (velocidad, ram))
        
        # Recupera los resultados y los imprime
        rows = cur.fetchall()
        if len(rows) > 0:
            print("Se encontraron las siguientes PCs:")
            for row in rows:
                print("Modelo:", row[0], "Precio:", row[1])
        else:
            print("No se encontraron PCs con esa velocidad y RAM.")
        
        # Confirma la transacción
        cur.execute("COMMIT;")
        
    except psycopg2.Error as e:
        # Si ocurre un error, cancela la transacción
        print("Error en la transacción:", e)
        cur.execute("ROLLBACK;")
        
    finally:
        # Cierra la conexión a la base de datos
        cur.close()
        conn.close()

# Función 2
def delete_pc(modelo):
    try:
        conn = connect()
        cur = conn.cursor()
        
        # Inicia la transacción
        cur.execute("BEGIN;")
        
        # Elimina la tupla correspondiente al modelo de las tablas PC y Producto
        cur.execute("DELETE FROM PC WHERE modelo = %s;", (modelo,))
        cur.execute("DELETE FROM Producto WHERE modelo = %s;", (modelo,))
        if cur.rowcount == 0:
            print("El modelo no existe.")
        else:
            print("Tupla eliminada correctamente.")
        
        # Confirma la transacción
        cur.execute("COMMIT;")
        
    except psycopg2.Error as e:
        # Si ocurre un error, cancela la transacción
        print("Error en la transacción:", e)
        cur.execute("ROLLBACK;")
        
    finally:
        # Cierra la conexión a la base de datos
        cur.close()
        conn.close()

# Función 3
def decrease_price(modelo):
    try:
        conn = connect()
        cur = conn.cursor()

        # verificamos si existe el modelo en la tabla PC
        cur.execute("SELECT modelo FROM PC WHERE modelo = %s", (modelo,))
        if cur.fetchone() is None:
            print("El número de modelo no existe.")
            return

        # disminuimos el precio en $100.00
        cur.execute("UPDATE PC SET precio = precio - 100 WHERE modelo = %s", (modelo,))
        conn.commit()
        print("El precio se ha disminuido en $100.00.")

    except psycopg2.Error as e:
        conn.rollback()
        print("Error en la transacción:", e)

    finally:
        cur.close()
        conn.close()

# Función 4
def check_and_insert(fabricante, modelo, velocidad, ram, disco, precio, tipo):
    try:
        conn = connect()
        cur = conn.cursor()

        # verificamos si existe un modelo con las mismas características
        cur.execute("SELECT modelo FROM PC WHERE modelo = %s AND velocidad = %s AND ram = %s AND disco = %s AND precio = %s",
                    (modelo, velocidad, ram, disco, precio))
        if cur.fetchone() is not None:
            print("Ya existe un producto con esas características.")
            return

        # insertamos el nuevo modelo en las tablas Producto y PC
        cur.execute("INSERT INTO Producto VALUES (%s, %s, %s)", (fabricante, modelo, tipo, ))
        cur.execute("INSERT INTO PC VALUES (%s, %s, %s, %s, %s)", (modelo, velocidad, ram, disco, precio, ))
        conn.commit()
        print("Se ha insertado un nuevo modelo.")

    except psycopg2.Error as e:
        conn.rollback()
        print("Error en la transacción:", e)

    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    while True:
        print("\n¿Qué acción deseas realizar?")
        print("1. Buscar PCs por velocidad y RAM.")
        print("2. Eliminar un modelo de la tabla PC y Producto.")
        print("3. Disminuir el precio de un modelo en $100.00.")
        print("4. Verificar si existe un modelo y agregarlo si no existe.")
        print("5. Salir.")
        opcion = input("Opción: ")
        if opcion == "1":
            velocidad = input("Velocidad: ")
            ram = input("RAM: ")
            search_pc(velocidad, ram)
        elif opcion == "2":
            modelo = input("Modelo: ")
            delete_pc(modelo)
        elif opcion == "3":
            modelo = input("Modelo: ")
            decrease_price(modelo)
        elif opcion == "4":
            fabricante = input("Fabricante: ")
            modelo = input("Modelo: ")
            velocidad = input("Velocidad: ")
            ram = input("RAM: ")
            disco = input("Disco: ")
            precio = input("Precio: ")
            tipo = input("Tipo: ")
            check_and_insert(fabricante, modelo, velocidad, ram, disco, precio, tipo)
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")
