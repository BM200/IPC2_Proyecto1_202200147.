# En modelos/lista.py

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

    def reemplazar(self, indice, nuevo_dato):
        if indice < 0 or indice >= self._tam:
           
            return False

        aux = self._cabeza
        i = 0
        while i < indice:
            aux = aux.getSiguiente()
            i += 1
        aux.setDato(nuevo_dato)
       
        return True

    def getTam(self): 
        return self._tam