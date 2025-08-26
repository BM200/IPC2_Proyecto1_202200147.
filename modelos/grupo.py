from .lista import ListaEnlazada

class Grupo:
    def __init__(self, clave):
        self._clave = clave
        self._indices = ListaEnlazada()
        self._nombreAgrupado = ""
        self._idReducida = ""

    def getClave(self): return self._clave
    def getIndices(self): return self._indices
    def agregarIndice(self, i): self._indices.agregar(i)

    def setNombreAgrupado(self, nombre): self._nombreAgrupado = nombre
    def getNombreAgrupado(self): return self._nombreAgrupado

    def setIdReducida(self, idr): self._idReducida = idr
    def getIdReducida(self): return self._idReducida
