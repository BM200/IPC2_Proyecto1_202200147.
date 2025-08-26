from .nodo import Nodo

class ListaEnlazada:
    def __init__(self):
        self._cabeza = None
        self._tam = 0

    def agregar(self, dato):
        nuevo = Nodo(dato)
        if self._cabeza is None:
            self._cabeza = nuevo
        else:
            aux = self._cabeza
            while aux.getSiguiente() is not None:
                aux = aux.getSiguiente()
            aux.setSiguiente(nuevo)
        self._tam += 1

    def obtener(self, indice):
        if indice < 0 or indice >= self._tam:
            return None
        aux = self._cabeza
        i = 0
        while i < indice:
            aux = aux.getSiguiente()
            i += 1
        return aux.getDato()

    def __iter__(self):
        aux = self._cabeza
        while aux is not None:
            yield aux.getDato()
            aux = aux.getSiguiente()

    def getTam(self): return self._tam
