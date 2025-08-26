from .lista import ListaEnlazada
from .frecuencia import Frecuencia

class Sensor:
    def __init__(self, id_, nombre):
        self._id = id_
        self._nombre = nombre
        self._frecuencias = ListaEnlazada()

    def getId(self): return self._id
    def getNombre(self): return self._nombre
    def getFrecuencias(self): return self._frecuencias

    def agregarFrecuencia(self, f: Frecuencia):
        self._frecuencias.agregar(f)


class SensorSuelo(Sensor):
    pass

class SensorCultivo(Sensor):
    pass
