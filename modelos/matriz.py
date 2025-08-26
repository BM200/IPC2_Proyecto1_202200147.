class Matriz:
    def __init__(self, filas, columnas, valorInicial=0):
        self._filas = filas
        self._columnas = columnas
        self._datos = [[valorInicial for _ in range(columnas)] for _ in range(filas)]

    def set(self, i, j, valor): self._datos[i][j] = valor
    def get(self, i, j): return self._datos[i][j]

    def getFilas(self): return self._filas
    def getColumnas(self): return self._columnas
