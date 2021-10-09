from pymongo import MongoClient

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
                command_cursor (CommandCursor) -- Cursor de pymongo
        """
        self.model_class = model_class
        self.command_cursor = command_cursor
        pass 
        
    def next(self):
        """ Devuelve el siguiente documento en forma de modelo
        """
        
        pass

    @property
    def alive(self):
        """True si existen más modelos por devolver, False en caso contrario
        """
        pass 
