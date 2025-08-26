class EstacionBase:
    def __init__(self, id_, nombre):
        self._id = id_
        self._nombre = nombre

    def getId(self): return self._id
    def getNombre(self): return self._nombre
    
