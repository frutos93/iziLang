class Funcion:
    
    def __init__(self, nombre, tipo, params, scope):
        self.__nombre = nombre
        self.__tipo = tipo
        self.__params = params
        self.__scope = scope

    def getNombre(self):
        return self.__nombre

    def getTipo(self):
        return self.__tipo

    def getScope(self):
        return self.__scope

    def getParams(self):
        return self.__params
