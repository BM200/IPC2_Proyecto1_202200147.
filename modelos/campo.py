from .lista import ListaEnlazada

class CampoAgricola:
    def __init__(self, id_, nombre):
        self._id = id_
        self._nombre = nombre
        self._estaciones = ListaEnlazada()
        self._sensoresSuelo = ListaEnlazada()
        self._sensoresCultivo = ListaEnlazada()

        self.F_ns = None
        self.F_nt = None
        self.Fp_ns = None
        self.Fp_nt = None
        self.Fr_ns = None
        self.Fr_nt = None
        self.grupos = None

    def getId(self): return self._id
    def getNombre(self): return self._nombre
    def getEstaciones(self): return self._estaciones
    def getSensoresSuelo(self): return self._sensoresSuelo
    def getSensoresCultivo(self): return self._sensoresCultivo
