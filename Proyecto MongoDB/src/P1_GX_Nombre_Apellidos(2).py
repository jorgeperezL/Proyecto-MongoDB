from paramiko import file
from gym.envs import kwargs
from pip._internal.network.session import user_agent
import pymongo
import json
import bson
__author__ = 'jorge_perez y miguel_abdon'

from pymongo import MongoClient, command_cursor, GEO2D
from geopy.geocoders import Nominatim


def getCityGeoJSON(address):
    """ Devuelve las coordenadas de una direcciion a partir de un str de la direccion
    Cuidado, la API tiene un limite de peticiones.
    Argumentos:
        address (str) -- Direccion
    Return:
        (str) -- GeoJSON
        
    """
    geolocator = Nominatim(user_agent = 'app')
    location = geolocator.geocode(address)
    #TODO
    geojson = {"type": "Point", "coordinates" : [location.latitude,location.longitude]}
    return geojson
    
    # Devolver GeoJSON de tipo punto con la latitud y longitud almacenadas
    # en las variables location.latitude y location.longitude

class ModelCursor:
    """ Cursor para iterar sobre los documentos del resultado de una
    consulta. Los documentos deben ser devueltos en forma de objetos
    modelo.
    """

    def __init__(self, model_class, command_cursor):
        """ Inicializa ModelCursor
        Argumentos:
            model_class (class) -- Clase para crear los modelos del 
            documento que se itera.
            command_cursor (CommandCursor) -- Cursor de pymongo respuesta mongoDB.
        """
        self.model_class = model_class
        self.command_cursor = command_cursor
    
    def next(self):
        """ Devuelve el siguiente documento en forma de modelo
        """
        #TODO   
        return self.model_class(**self.command_cursor.next())

    @property
    def alive(self):
        return self.command_cursor.alive
        
class Model:
    """ Prototipo de la clase modelo
        Copiar y pegar tantas veces como modelos se deseen crear (cambiando
        el nombre Model, por la entidad correspondiente), o bien crear tantas
        clases como modelos se deseen que hereden de esta clase. Este segundo 
        metodo puede resultar mas compleja
    """
    required_vars = []
    admissible_vars = []
    db = None

    def __init__(self, **kwargs):      
        #for required in cls.required_vars:  
            #if required in kwargs:
                #self.__dict__.update(kwargs)
                #print("Coleccion creada")
            #else:
                #print("Coleccion no creada")      
        for required in self.required_vars:
            if not kwargs.get(required.lower()):
                print("Falta Campo requerido")
                return          
        self.__dict__.update(kwargs)

    def save(self):
        for required in self.required_vars:
            if self.__dict__.get(required.lower()) is None:
                print("Coleccion no guardada en base de datos")
                return
                       
        if self.db.find({"ref": self.ref}).count() > 0:
            self.db.update({"ref": self.ref}, self.__dict__)
            print("Se ha actualizado")
        else:
            self.db.insert_one(self.__dict__)
            print("Coleccion guardada en base de datos")

    def set(self, **kwargs):
        self.__dict__.update(kwargs)
    
    @classmethod
    def find(cls, filter):
        """ Devuelve un cursor de modelos        
        """ 
        modelo_cursor = ModelCursor(cls,cls.db.find(filter))
                
        return modelo_cursor

        # cls es el puntero a la clase

    @classmethod
    def init_class(cls, db, vars_path="model_name.vars"):
        """ Inicializa las variables de clase en la inicializacion del sistema.
        Argumentos:
            db (MongoClient) -- Conexion a la base de datos.
            vars_path (str) -- ruta al archivo con la definicion de variables
            del modelo.
        """      
        cls.db = db;
        with open(vars_path) as f:
            mylist = f.read().splitlines() 
            cls.required_vars = mylist[0].split(" ")
            cls.admissible_vars = mylist[1].split(" ")
            #print(lines[0])     
            #required_vars = lines[0].split(" ")
            #admissible_vars = lines[1].split(" ")
            
            #print(required_vars)
            #print(admissible_vars)
           
        
        #TODO
        # cls es el puntero a la clase


# Q1: Listado de todas las compras de un cliente
latitud = -73.9667
longitud = 40.78

Q1 = [{"$match":{"ciudad.ciudad":"huelva"}},{"$project":{"nombre":1,"ciudad":1}}]
Q2 = [{"$match":{"$or":[{"estudios.universidad":"UPM"},{"estudios.universidad":"UAM"}]}},{"$project":{"nombre":1}}]
Q3 = [{"$match":{"ciudad.ciudad":{"$exists":True}}},{"$group":{"_id":"$ciudad", "personas":{"$sum":1}}},{"$project":{"ciudad":1}}]
Q4 = [{"$geoNear": {"near": { "type": "Point", "coordinates": [ latitud, longitud ] },"spherical": True,"distanceField": "calcDistance"}}]
Q5 = [{"$match":{"estudios.fin":{"$gte":"2017-01-01"}}},{"$out":{"db":"p1", "coll":"list_2017"}}]
Q6 = []
Q7 = []

# Q2: etc...
class Univeridad(Model):
    pass

class Empresa(Model):
    pass

class Persona(Model):
    pass

objetos = ['','','']

def persona_diccionario():
    diccionary = {}
    dni_inp = input("DNI: ")
    if bool(dni_inp):
        diccionary['ref'] = dni_inp 
    nombre_inp = input("Nombre: ")
    if bool(nombre_inp):
        diccionary['nombre'] = {}
        diccionary['nombre']['nombre'] = nombre_inp
        apellido_inp = input("Apellido: ")
        if bool(apellido_inp):
            diccionary['nombre']['apellido'] = apellido_inp
    universidad_inp = input("Universidad: ")
    if bool(universidad_inp):
        diccionary['estudios'] = []
        dict1 = {}
        dict1['universidad'] = universidad_inp 
        inicio_inp = input("Inicio: ")
        if bool(inicio_inp):
            dict1['inicio'] = inicio_inp
        fin_inp = input("Fin: ")
        if bool(fin_inp):
            dict1['fin'] = fin_inp 
        diccionary['estudios'].append(dict1)   
    ciudad_inp = input("Ciudad:")
    if bool(ciudad_inp):
        diccionary['ciudad'] = {}
        diccionary['ciudad']['ciudad'] = ciudad_inp
        diccionary['ciudad']['loc'] = getCityGeoJSON(ciudad_inp)
    empresa_inp = input("Empresa:")
    if bool(empresa_inp):
        diccionary['trabajo'] = []
        dict1 = {}
        dict1['empresa'] = empresa_inp 
        inicio_inp = input("Inicio: ")
        if bool(inicio_inp):
            dict1['inicio'] = inicio_inp
        fin_inp = input("Fin: ")
        if bool(fin_inp):
            dict1['fin'] = fin_inp 
        diccionary['trabajo'].append(dict1)    
    
    return diccionary

def persona_diccionario_buscar():
    diccionary = {}
    dni_inp = input("DNI: ")
    if bool(dni_inp):
        diccionary['ref'] = dni_inp 
    nombre_inp = input("Nombre: ")
    if bool(nombre_inp):
        diccionary["nombre.nombre"] = nombre_inp
    apellido_inp = input("Apellido: ")
    if bool(apellido_inp):
        diccionary["nombre.apellido"]= apellido_inp
    universidad_inp = input("Universidad: ")
    if bool(universidad_inp):
        diccionary["estudios.universidad"] = universidad_inp 
    inicio_inp = input("Inicio: ")
    if bool(inicio_inp):
        diccionary["estudios.inicio"] = inicio_inp
    fin_inp = input("Fin: ")
    if bool(fin_inp):
        diccionary["estudios.fin"] = fin_inp   
    ciudad_inp = input("Ciudad: ")
    if bool(ciudad_inp):
        diccionary["ciudad.ciudad"] = ciudad_inp
    empresa_inp = input("Empresa:")
    if bool(empresa_inp):
        diccionary["trabajo.empresa"] = empresa_inp
    inicio_inp = input("Inicio: ")
    if bool(inicio_inp):
        diccionary["trabajo.inicio"] = inicio_inp
    fin_inp = input("Fin: ")
    if bool(fin_inp):
        diccionary["trabajo.fin"] = fin_inp     
    
    return diccionary


def empresa_diccionario():
    diccionary = {}
    nif_inp = input("Nif: ")
    if bool(nif_inp):
        diccionary['ref'] = nif_inp 
    nombre_inp = input("Nombre: ")
    if bool(nombre_inp):
        diccionary['nombre'] = nombre_inp
        
    return diccionary
        
    
    

def crear():
    print("1-Persona")
    print("2-Empresa")
    print("3-Universidad")
    opcion = int(input("Elige una opcion: "))
        
    if opcion == 1:
        diccionary = persona_diccionario()
        persona = Persona(**diccionary)
        
        if bool(persona.__dict__):
            objetos[0] = persona 
                   
    if opcion == 2:
        diccionary = empresa_diccionario()
        empresa = Empresa(**diccionary)
        
        if bool(empresa.__dict__):
            objetos[1] = empresa
        
    if opcion == 3:
        diccionary = empresa_diccionario()
        universidad = Univeridad(**diccionary)
        
        if bool(universidad.__dict__):
            objetos[2] = universidad
            
    if opcion < 1 or opcion > 3:
        print('Numero mal puestos')
            
            
def actualizar():
    print("1-Persona")
    print("2-Empresa")
    print("3-Universidad")
    opcion = int(input("Elige una opcion: "))
        
    if opcion == 1:
        diccionary = persona_diccionario()        
        persona = objetos[0]
        persona.set(**diccionary)
               
    if opcion == 2:
        diccionary = empresa_diccionario()
        empresa = objetos[1]
        empresa.set(**diccionary)
        
    if opcion == 3:
        diccionary = empresa_diccionario()
        universidad = objetos[2]
        universidad.set(**diccionary)
        
    if opcion < 1 or opcion > 3:
        print('Numero mal puestos')
    
            
def guardar():
    print("1-Persona")
    print("2-Empresa")
    print("3-Universidad")
    opcion = int(input("Elige una opcion: "))
        
    if opcion == 1:       
        persona = objetos[0]
        persona.save()
               
    if opcion == 2:
        empresa = objetos[1]
        empresa.save()
        
    if opcion == 3:
        universidad = objetos[2]
        universidad.save()
        
    if opcion < 1 or opcion > 3:
        print('Numero mal puestos')
        
def buscar():
    print("1-Persona")
    print("2-Empresa")
    print("3-Universidad")
    opcion = int(input("Elige una opcion: "))
        
    if opcion == 1:  
        diccionary = persona_diccionario_buscar()    
        cursor = Persona.find(diccionary)
        return cursor
               
    if opcion == 2:
        diccionary = empresa_diccionario()
        cursor = Empresa.find(diccionary)
        return cursor
        
    if opcion == 3:
        diccionary = empresa_diccionario()
        cursor = Univeridad.find(diccionary)
        return cursor
        
    if opcion < 1 or opcion > 3:
        print('Numero mal puestos')
        
def consultas_predeterminadas():
    print("1-Listado de todas las personas de Huelva")
    print("2-Listado de todas personas que han estudiado en la UPM o UAM")
    print("3-Listado de las diferentes ciudades en las que se encuentran las personas")
    print("4-Listado de las 10 personas más cercanas a unas coordenadas determinadas.")
    print("5-Guarda  en  una  tabla  nueva  el  listado  de  las  personas  que  ha  terminado  alguno  de  sus estudios en el 2017 o después")
    print("6-Calcular  el  número  medio  de  estudios  realizados  por  las  personas  que  han  trabajado  o trabajan en la UPM")
    print("7-Listado de las tres universidades que más veces aparece como centro de estudios de las personas registradas. Mostrar universidad y el número de veces que aparece")
    
    opcion = int(input("Escribe una opcion: "))
    
    if opcion == 1:
        results = Persona.db.aggregate(Q1)
        return results
    if opcion == 2:
        results = Persona.db.aggregate(Q2)
        return results
    if opcion == 3:
        results = Persona.db.aggregate(Q3)
        return results
    if opcion == 4:
        global latitud 
        latitud= float(input("Escribe latitud: "))
        global longitud
        longitud = float(input("Escribe longitud: "))
        results = Persona.db.aggregate(Q4)
        return results
    if opcion == 5:
        results = Persona.db.aggregate(Q5)
        print("Coleccion list_2017 Creada")
        return results
    if opcion == 6:
        results = Persona.db.aggregate(Q6)
        return results
    if opcion == 7:
        results = Persona.db.aggregate(Q7)
        return results
    if opcion < 1 or opcion > 7:
        print('Numero mal puestos')
        

def consola():
    semaforo = True
    while (semaforo):
        print("1 - Crear")
        print("2 - Actualizar")
        print("3 - Guardar")
        print("4 - Buscar")
        print("5 - Consultas predeterminadas")
        print("6 - Salir")
        
        opcion = int(input("Elige una opcion: "))
        
        if opcion == 1:
            crear()
        if opcion == 2:
            actualizar()
        if opcion == 3:
            guardar()
        if opcion == 4:
            cursor = buscar()
            while cursor.alive:
                objeto = cursor.next()
                print(objeto.__dict__)
        if opcion == 5:
            results = consultas_predeterminadas()
            for doc in results:
                print(doc)
        if opcion == 6:
            semaforo = False
        if opcion < 1 or opcion > 6:
            print("Error")
        
def iniciacion_mongodb(): 
    client = MongoClient('localhost')
    client.p1
    Univeridad.init_class(client.p1.universidad, 'universidad.txt')
    Empresa.init_class(client.p1.empresa, 'empresa.txt')
    Persona.init_class(client.p1.persona, 'persona.txt')
    client.p1.persona.create_index([("ciudad.loc", pymongo.GEOSPHERE)])
    
def elementos_prueba():
    persona1 = {
    "ref": "51542506N",
    "nombre": { "nombre": "Jorge", "apellido": "Perez" },
    "estudios": [
      { "universidad": "utad", "inicio": "2014-04-01", "fin": "2019-05-04" }
    ],
    "ciudad": {
      "ciudad": "madrid",
      "loc": { "type": "Point", "coordinates": [ 40.4167047, -3.7035825 ] }
    },
    "trabajo": [
      { "empresa": "Accenture", "inicio": "2014-06-23", "fin": "2017-12-12" }
    ]
    }
    persona2 = {
    "ref": "51672506N",
    "nombre": { "nombre": "Miguel", "apellido": "Abdon" },
    "estudios": [
      { "universidad": "UPM", "inicio": "2013-04-12", "fin": "2015-06-12" }
    ],
    "ciudad": {
      "ciudad": "huelva",
      "loc": { "type": "Point", "coordinates": [ 37.2575874, -6.9484945 ] }
    },
    "trabajo": [
      { "empresa": "Everis", "inicio": "2018-04-23", "fin": "2021-04-12" }
    ]
    }
    persona3 = {
    "ref": "51547706N",
    "nombre": { "nombre": "Miguel", "apellido": "Herencia" },
    "estudios": [
      { "universidad": "UAM", "inicio": "2015-05-12", "fin": "2019-07-12" }
    ],
    "ciudad": {
      "ciudad": "huelva",
      "loc": { "type": "Point", "coordinates": [ 37.2575874, -6.9484945 ] }
    },
    "trabajo": [
      { "empresa": "Everis", "inicio": "2012-05-25", "fin": "2016-07-12" }
    ]
    }
    persona4 = {
    "ref": "51511506N",
    "nombre": { "nombre": "Manuel", "apellido": "Perez" },
    "estudios": [
      { "universidad": "UAM", "inicio": "2011-11-12", "fin": "2015-10-12" }
    ],
    "ciudad": {
      "ciudad": "toledo",
      "loc": { "type": "Point", "coordinates": [ 39.8560679, -4.0239568 ] }
    },
    "trabajo": [
      { "empresa": "Indra", "inicio": "2015-09-11", "fin": "2020-07-12" }
    ]
    }
    persona5 = {
    "ref": "51588806N",
    "nombre": { "nombre": "Pablo", "apellido": "Perez" },
    "estudios": [
      { "universidad": "UPM", "inicio": "2011-11-12", "fin": "2017-04-12" }
    ],
    "ciudad": {
      "ciudad": "madrid",
      "loc": { "type": "Point", "coordinates": [ 40.4167047, -3.7035825 ] }
    },
    "trabajo": [
      { "empresa": "Everis", "inicio": "2015-05-11", "fin": "2019-07-12" }
    ]
    }
    
    Persona(**persona1).save()
    Persona(**persona2).save()
    Persona(**persona3).save()
    Persona(**persona4).save()
    Persona(**persona5).save()

    empresa1 = {
    "ref": "1234",
    "nombre": "Accenture"
    }
    
    empresa2 = {
    "ref": "5678",
    "nombre": "Everis"
    }
    
    empresa3 = {
    "ref": "1470",
    "nombre": "Indra"
    }
    
    Empresa(**empresa1).save()
    Empresa(**empresa2).save()
    Empresa(**empresa3).save()
    
    centro1 = {
    "ref": "1234A",
    "nombre": "UAM"
    }
    
    centro2 = {
    "ref": "5678B",
    "nombre": "UPM"
    }
    
    Univeridad(**centro1).save()
    Univeridad(**centro2).save()
    


if __name__ == '__main__':
    
    iniciacion_mongodb()
    elementos_prueba()
    consola()
    

