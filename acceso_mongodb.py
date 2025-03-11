from pymongo import MongoClient
from urllib.parse import quote_plus
import getpass
from Tarea import Tarea

# Para el ejemplo, crearemos una lista de tareas (será la que insertemos en MongoDB)
# En producción, estos datos o bien los obtenemos de un fichero JSON o bien de otro servicio que los proporcione
tareas = [
    Tarea("Instalar_Java", "C:\\Software\\install_java.exe", True, ["eq23", "eq12", "server11", "server2"], "Semanal"),
    Tarea("Instalar_Adobe_Reader", "C:\\Software\\install_reader.ps", False, ["eq50", "serverrdp"], "Mensual"),
    Tarea("Instalar_Python", "C:\\Software\\install_python.py", False, ["dis_e", "equipo_ora"], "Diaria"),
    Tarea("Instalar_Zip", "C:\\Software\\zip.bat", True, ["*"], "Diaria")    
]

# Solicitamos los datos de conexión al servidor MongoDB
servidorMongoDB = input("Introduzca la IP o nombre DNS del servidor MongoDB (por defecto localhost): ")
if servidorMongoDB == "":
    servidorMongoDB ="localhost"
puerto = input("Introduzca el puerto de conexión al servidor MongoDB (Por defecto 27017): ")
if puerto == "":
    puerto = "27017"
bd = input("Introduzca el nombre de la base de datos (debe existir, por defecto bdproyectoa): ")
if bd == "":
    bd = "bdproyectoa"
coleccion = input("Introduzca el nombre de la colección (debe existir en la BD, por defecto bdproyectoa): ")
if coleccion == "":
    coleccion = "bdproyectoa"
usuario = input("Introduzca el usuario de conexión: ")
contrasena = getpass.getpass("Introduzca la contraseña: ")

# Establecemos la URI de conexión con el servidor MongoDB
# Usamos el método quote_plus para hacer más seguro el acceso y limpiar de posibles caracteres no deseados
uri = "mongodb://%s:%s@%s:%s" % (
        quote_plus(usuario), quote_plus(contrasena), servidorMongoDB, puerto)
    
try:
    # Conexión al servidor MongoDB pasándole los datos de conexión
    conMongo = MongoClient(uri)
    
    # Abrimos la base de datos "bdproyectoa" (debe existir en el servidor MongoDB)
    bdMongo = conMongo[bd]
    
    # Abrimos la colección "bdproyectoa" de la base de datos "bdproyectoa" (debe existir en MongoDB)
    colMongo = bdMongo[coleccion]
    
    try:
        # INSERTAR DOCUMENTOS (Tareas)
        # Hacer el equivalente a un insert en bases de datos relacionales SQL
        # Insertamos cada documento (tarea) y mostramos el ID asociado en MongoDB
        print("Insertando documentos en MongoDB...")
        for tarea in tareas:
            resultadoInsertar = colMongo.insert_one(tarea.coleccionTareaMongoDB())
            print(f"ID de documento insertado: {resultadoInsertar.inserted_id}")
        
        
        # MOSTRAR DOCUMENTOS (Tareas)
        # Hacer el equivalente a un Select en bases de datos relacionales SQL
        # Filtramos para mostrar sólo las tareas activas
        print("Mostrando documentos de colección con filtro en MongoDB...")
        curMongo = colMongo.find({"activa":True})
        for tarea in curMongo:
            print (f"{tarea["nombre"]:20} {tarea["periodicidad"]:20} {tarea["accion"]}")
            
        # ACTUALIZAR DOCUMENTOS (Tareas)
        # Hacer el equivalente a un Update en bases de datos relacionales SQL
        # Filtramos para actualizar el valor de la periodicidad para las tareas activas=true
        print("Actualizando documentos de colección con filtro en MongoDB...")
        resultadoActualizar = colMongo.update_many(
            {"activa": True},
            {"$set":
                {"periodicidad": "Anual"}
            }, upsert=True
        )
        print(f"Documentos modificados: {resultadoActualizar.modified_count}")
        
        # ELIMINAR DOCUMENTOS (Tareas)
        # Hacer el equivalente a un Delete en bases de datos relacionales SQL
        # Filtramos para eliminar los documentos con periodicidad "Diaria" y activos = True
        print("Eliminando documentos de colección con filtro en MongoDB...")
        resultadoEliminar = colMongo.delete_many(
            {"activa": False,
            "periodicidad": "Diaria"}
        )
        print(f"Documentos eliminados: {resultadoEliminar.deleted_count}")        
        
        # Cerramos la conexión con el servidor MongoDB    
        conMongo.close()
    except Exception as e:
        print(f"Error al realizar acción en MongoDB: {e}")
        
except Exception as e:
    print(f"Error al conectar al sevidor MongoDB [{servidorMongoDB}]: {e}")