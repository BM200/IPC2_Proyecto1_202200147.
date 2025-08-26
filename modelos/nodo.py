class Nodo:
    def __init__(self, dato):
        self._dato = dato
        self._siguiente = None

    def getDato(self): return self._dato
    def setDato(self, dato): self._dato = dato

    def getSiguiente(self): return self._siguiente
    def setSiguiente(self, nodo): self._siguiente = nodo
