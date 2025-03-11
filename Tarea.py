# Definimos la clase tarea
class Tarea:
    # Constructor de la clase
    def __init__(self, nombre, accion, activa, alcance, periodicidad):
        self.nombre = nombre
        self.accion = accion
        self.activa = activa
        self.alcance = alcance
        self.periodicidad = periodicidad
    
    # Definiremos un método para convertir la clase Tarea en diccionario, entendible por MongoDB
    def coleccionTareaMongoDB (self):
        return {
            "nombre":self.nombre,
            "accion":self.accion,
            "activa": self.activa,
            "alcance":self.alcance,
            "periodicidad":self.periodicidad
        }
        
    def __str__(self):
        return f"Tarea: {self.nombre} | Acción: {self.accion} | Activa: {self.activa} | Alcance: {self.alcance} | Periodicidad: {self.periodicidad}"