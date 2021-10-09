from modelCursor import ModelCursor
from pymongo import MongoClient

class Model:
    """ 
        Prototipo de la clase modelo
        Copiar y pegar tantas veces como modelos se deseen crear (cambiando
        el nombre Model, por la entidad correspondiente), o bien crear tantas
        clases como modelos se deseen que hereden de esta clase. Este segundo 
        metodo puede resultar mas compleja
    """
  
    
    required_vars = []
    admissible_vars = []
    lista = []
   
    db = None
    col = None


    def __init__(self, **kwargs):

      


        self.__dict__.update(kwargs)   
        pass 


    def save(self):
        
        
        pass 

    def set( **kwargs):
        
        lista = []
        dicc = {"telefono":68900}
        for x in dicc:
            lista.append(x)
        print(lista)
        #self.__dict__.update(kwargs)  
        pass 
        
    @classmethod
    def find(cls, filter):
        
        """ Devuelve un cursor de modelos        
        """ 
        for x in cls.col.find():
            print(x)

        
        # cls es el puntero a la clase
        pass 

    @classmethod
    def init_class(cls, db, vars_path="model_name.vars"):
        
        """ Inicializa las variables de clase en la inicializacion del sistema.
            Argumentos:
            db (MongoClient) -- Conexion a la base de datos.
            vars_path (str) -- ruta al archivo con la definicion de variables
            del modelo.
        """
        
        client = MongoClient('localhost')
        cls.db = client['ProyectoPrimer_bbdd']
        cls.col = cls.db['prueba4']

       
        print(client.list_database_names())

        


        # cls es el puntero a la clase
        pass 

if __name__ == '__main__':

    Model.init_class(Model.db, "redES.json")
    Model.find("leo")
    Model.set()
    Model.find("")
    pass #No olvidar eliminar esta linea una vez implementado
