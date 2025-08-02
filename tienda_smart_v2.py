
import sqlite3
from colorama import init, Fore, Back, Style



categorias = ("Eléctricos","Iluminación","Sensores","Electrodomesticos","Audio y Video","Salud")    
init(autoreset=True)
def menu():
    try:
        print(Fore.BLUE + "Bienvenidos a la tienda Smart Por favor, Elija una opción: ")
       # print(Style.RESET_ALL)
        opciones = ("Agregar un producto","Mostrar todos los productos de la tienda","Buscar un producto","Borrar un producto","Modificar producto","Salir del programa")    
        for numero, opcion in enumerate(opciones, start=1):
            print(f"   {numero}: {opcion}")
        entrada = input(Fore.GREEN + "Ingrese un numero de opción deseada: ")
        entrada.strip().lstrip("-").isdigit()
        return int(entrada)
    except ValueError:
        print(Back.RED + "Por favor, ingrese una número válido.") 
        #print(Style.RESET_ALL)



def ejecutar_db(consulta,parametros=(),fetch=False,fetchone=False):
    """
        Ejecuta consultas SQL a la base de datos
        Parametros:
            consulta: query SQL
            parametros: tupla de parametros
            fetch: booleano indica si tengo que devolver fetchall
            fetchone: booleano indica si tengo que devolver fetchone
    """
    try:
        with sqlite3.connect("inventario.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute(consulta,parametros)

            if fetch:
                resultado = cursor.fetchall()
            elif fetchone:
                resultado = cursor.fetchone()
            else:
                resultado = None
                        
            conexion.commit()            
            
            return resultado
    except sqlite3.Error as e:
        conexion.rollback()
        global sin_problema
        sin_problema = True
        print("Se devuelven lo cambios por un error.")
        print(f"Error en la consulta:{e}")
    

def inicializar_db():
    consulta_sql = """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT(100) NOT NULL,  
            descripcion TEXT(10000) NOT NULL,          
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,            
            categoria TEXT(50) NOT NULL
        )
    """
    ejecutar_db(consulta_sql)

    
def agregar_producto():    
    print(Style.BRIGHT + "Vamos a agregar un nuevo producto")
    nombre = corroborar_nombre()
    descripcion = input("Ingrese la descripción del producto: ").strip()
    print("Cantidad del producto")
    cantidad = corroborar_numero_entero()
    precio= corroborar_precio()
    categoria = elegir_categoria()
    
    insert_sql = "INSERT INTO productos (nombre,descripcion,cantidad,precio,categoria) VALUES (?,?,?,?,?)"
    parametros = (nombre,descripcion,cantidad,precio,categoria) #tupla
    ejecutar_db(insert_sql,parametros)
    if sin_problema == False:
        print(Fore.GREEN +"Producto agregado!") 
       
  
def corroborar_nombre():
    while True:
        nombre = input("Ingrese nombre: ").strip()
        if len(nombre) > 0:
            return nombre
        else:
            print("El nombre no puede estar vacio, por favor ingrese nuevamente.")    

def corroborar_numero_entero():
    """
        Funcion que valida el ingreso de un numero entero
        Retorno:
            int: numero  
    """
    while True:
        try:
            numero = int(input("Ingrese un numero: "))
            if numero >= 0:
                return numero
            else:
                print("El numero ingresado no puede tener un valor negativo, ingrese nuevamente.")
        except ValueError:
            print("Por favor ingrese un valor numerico.")
        except Exception as e:
            print(f"El error es: {e}")

def corroborar_precio():
    """
        Funcion que valida el ingreso de un precio, su valor debe ser mayor a 0
    """
    while True:
        try:
            precio = float(input("Ingrese el precio: $"))
            if precio >= 0:
                return precio
            else:
                print("El precio no puede tener un valor negativo, ingrese nuevamente.")
        except ValueError:
            print("Por favor ingrese un valor numerico.")
        except Exception as e:
            print(f"El error es: {e}")

def elegir_categoria():
    while True:
        try:      
            for numero, opcion in enumerate(categorias, start=1):
                print(f"   {numero}: {opcion}")
            n_categoria = input(Fore.GREEN + "Ingrese el numero de la categoria: ")
            print(Style.RESET_ALL)
            n_categoria.strip().lstrip("-").isdigit()
            posicion = int(n_categoria)
            if posicion > 0 and posicion <= len(categorias): 
                for num, opc in enumerate(categorias, start=1):       
                    if num == posicion:
                        return opc
            else:
                print(Back.RED + "Por favor, ingrese una número de acuerdo a las categorias.")
        except ValueError:
            print(Back.RED + "Por favor, ingrese una número válido.") 
        except Exception as e:
                print(f"El error es: {e}")
    

def mostar_inventario():
    """
        Muestra la lista del inventario si contiene elementos
        
    """
    select_sql = "SELECT * FROM productos"
    #Llamo a la funcion con parametros nombrados.
    inventario = ejecutar_db(consulta=select_sql,fetch=True)
    if len(inventario)>0:        
        visualizar_productos(inventario)
    else:
        print(Back.RED + "No hay Productos")

def visualizar_productos(inventario):
    
    cabecera = f"{'Id':<5} |{'Nombre':<30} |{'Descripción':<50} |{'Cantidad':<10} |{'Precio':<10} |{'Categoria':<20}"
    print(cabecera)  
    print("-"*len(cabecera))  
    for i in inventario:   
        print(f"{i[0]:<5} |{i[1]:<30} |{i[2]:<50} |{i[3]:<10} |{i[4]:<10} |{i[5]:<20}")    
    print("-"*len(cabecera))


def buscar_producto():
    print("Menu de busqueda")
    while True:
        menu_busqueda = """
            Buscar productos mediante:

            1. ID
            2. Nombre
            3. Categoria

            Presione 4 para volver

            """
        print(menu_busqueda)
        busqueda = corroborar_numero_entero()
        if busqueda>0 and busqueda<=4:
            if busqueda == 1:
                print(f"Ingrese el {Style.BRIGHT} NUMERO DEL ID {Style.RESET_ALL} del producto a buscar ")
                num = corroborar_numero_entero()
                resultado = buscar_por_id(num)
                if resultado:
                    producto = [resultado]  # Convertimos tupla a lista de una sola tupla
                else:
                    producto = []
                #print(producto)
                #visualizar_productos(producto)
            elif busqueda == 2:
                producto = buscar_producto_nombre()
               # visualizar_productos(producto)

            elif busqueda == 3:
                cat = elegir_categoria()
                producto = buscar_producto_categoria(cat)
               # visualizar_productos(producto)
            elif busqueda == 4:
                break
            else:
                print("Opción no es valida")

            if len(producto)>0:        
                visualizar_productos(producto)
                break
            else:
                print(f"{Back.YELLOW}{Fore.RED}{Style.BRIGHT} No se encuentra el producto en el inventario")
        else:
            print(f"{Back.YELLOW}{Fore.RED}{Style.BRIGHT} Elija una opcion del 1 al 3")

def buscar_por_id(id_inventario):
    """
        Funcion que busca un producto por su id en la base de datos
        Parametros:
            int: id 
        Retorna:
            inventario: tupla
    """
    sql_busqueda = "SELECT * FROM productos WHERE id = ?"
    parametros = (id_inventario,) #tupla
    producto = ejecutar_db(consulta=sql_busqueda,parametros=parametros,fetchone=True)
    return producto

def buscar_producto_nombre():
    nombre_busqueda = corroborar_nombre()
    sql_busqueda = " SELECT * FROM productos WHERE LOWER(nombre) LIKE LOWER(?)"
    parametros = (f"%{nombre_busqueda}%",)
    articulo = ejecutar_db(consulta=sql_busqueda,parametros=parametros,fetch=True)
    return articulo

def buscar_producto_categoria(categoria):

    """Funcion para buscar todos los productos de la categoria que ingreses"""

    sql_busqueda = " SELECT * FROM productos WHERE LOWER(categoria) LIKE LOWER(?)"
    parametros = (f"%{categoria}%",)
    articulo = ejecutar_db(consulta=sql_busqueda,parametros=parametros,fetch=True)
    return articulo

def eliminar_producto():
    sub_menu = """
Esta opcion es para proceder a eliminar un producto, debe ingresar el numero de ID del producto que usted desea eliminar 

Si no sabe el id ingrese a la opcion buscar producto del menu inicial

"""
    print(sub_menu)
    sabe_id = input(f"Usted sabe el id del producto? (s/n): ").strip().lower()
    if sabe_id == 's':
        id = corroborar_numero_entero()
        producto = buscar_por_id(id)
        if not producto:
            print(f"No se encontro el producto con ID: {id}")
            return

        #Se solicita confirmacion para eliminacion
        confirmacion = input(f"Esta seguro que desea eliminar el producto con ID:{id}? (s/n)").strip().lower()
        if confirmacion == 's':
            eliminar(id)            
        elif confirmacion == 'n':
            print('Se cancela la eliminación.')
        else:
            print(Fore.RED + "La tetra que ingreso es incorrecta")
    elif sabe_id == 'n':
        buscar_producto()
        print("Si usted ya sabe el ID")
        ya_sabe_id = corroborar_numero_entero()
        produ = buscar_por_id(ya_sabe_id)
        if not produ:
            print(f"Parece que ingreso mal el numero de ID: {ya_sabe_id}")
            return

        #Se solicita confirmacion para eliminacion
        confirmacion = input(f"Esta seguro que desea eliminar el producto con ID:{ya_sabe_id}? (s/n): ").strip().lower()
        if confirmacion == 's':
            eliminar(ya_sabe_id)            
        elif confirmacion == 'n':
            print('Se cancela la eliminación.')
        else:
            print(Fore.RED + "La tetra que ingreso es incorrecta")
    else:
        print(Fore.RED + "La tetra que ingreso es incorrecta")

def eliminar(id):
    sql_eliminar = "DELETE FROM productos WHERE id = ?"
    parametros = (id,) #tupla
    ejecutar_db(sql_eliminar,parametros)
    print("Producto eliminado con éxito")

def modificar_producto():
    cabecera = ('Id','Nombre','Descripción','Cantidad','Precio','Categoria')
    """
        Actualizar un producto buscando previamente por su nombre seleccionando por su ID
    """
    print("Buscar producto a modificar por ID")
    # id = corroborar_numero_entero()
    # busqueda = [buscar_por_id(id)]
    # if len(busqueda) == 0:
    #     print("No se encontraron producto indicado.")
    #     return
    # print('Productos encontrados:')
    # resultado = [busqueda]
    # visualizar_productos(busqueda)
    print(Fore.YELLOW + "Ingrese el id del producto a actualizar")
    id = corroborar_numero_entero()
    producto_modificar = buscar_por_id(id)
    if not producto_modificar:
        print(f"No se encontro un producto con ID {id}")
        return
    if producto_modificar:
        producto = [producto_modificar]  # Convertimos tupla a lista de una sola tupla
    else:
        producto = []
    visualizar_productos(producto)
    
    for i in range(1,len(cabecera)):
        respuesta = input(f"Desea modificar el {cabecera[i]}?(s/n) ").strip().lower()
        if respuesta == 's':
            if cabecera[i] == cabecera[1]:
                nuevo_nombre = corroborar_nombre()
            elif cabecera[i] == cabecera[2]:
                nueva_decripcion= input("Ingrese la nueva descripción del producto: ").strip()
            elif cabecera[i] == cabecera[3]:
                nueva_cantidad = corroborar_numero_entero()
            elif cabecera[i] == cabecera[4]:
                nuevo_precio = corroborar_precio()
            elif cabecera[i] == cabecera[5]:
                nueva_categoria = elegir_categoria()
        else:
            if cabecera[i] == cabecera[1]:
                nuevo_nombre = producto_modificar[i]
            elif cabecera[i] == cabecera[2]:
                nueva_decripcion= producto_modificar[i]
            elif cabecera[i] == cabecera[3]:
                nueva_cantidad = producto_modificar[i]
            elif cabecera[i] == cabecera[4]:
                nuevo_precio = producto_modificar[i]
            elif cabecera[i] == cabecera[5]:
                nueva_categoria = producto_modificar[i]
    
    sql_modificar = """
                UPDATE productos
                SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
                WHERE id = ?
            """    
    parametros = (nuevo_nombre,nueva_decripcion,nueva_cantidad,nuevo_precio,nueva_categoria,id)
    ejecutar_db(sql_modificar,parametros)    
    

      

        
###################################### PROGRAMA PRINCIPAL ######################################
inicializar_db() #Se crea la bace de dato con esta función
sin_problema = False
while True:
    entrada = menu()
    
    if entrada:
        opcion= entrada
        if opcion == 1:
            agregar_producto()          
            
        elif opcion == 2:
            mostar_inventario()             

        elif opcion == 3:
           buscar_producto()
         
        elif opcion == 4:
            eliminar_producto()

        elif opcion == 5:
            modificar_producto()
        elif opcion == 6:
            print(Back.BLUE + "Hasta la próxima" )
            #print(Style.RESET_ALL)
            break

        
        elif opcion > 6:
            print(Back.RED + "No existe esta opción")
           # print(Style.RESET_ALL)
        
   

    else:
        print(Back.RED + "Error: No has ingresado un número entero.")
        #print(Style.RESET_ALL)
