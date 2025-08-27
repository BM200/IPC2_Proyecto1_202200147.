from .lista import ListaEnlazada

class Matriz:
    def __init__(self, filas, columnas, valorInicial=0):
        
        if filas < 0 or columnas < 0:
            raise ValueError("Las dimensiones de la matriz no pueden ser negativas")
        self._filas = filas
        self._columnas = columnas
        self._datos = ListaEnlazada()
        
        i = 0
        while i < filas:
            fila = ListaEnlazada()
            j = 0
            while j < columnas:
                fila.agregar(valorInicial)
                j += 1
            self._datos.agregar(fila)
            i += 1
            
    def _obtenerFila(self, i):
        return self._datos.obtener(i) # Esto ahora puede devolver None

    def set(self, i, j, valor):
        """
        Este método ahora retorna True si la operación fue exitosa,
        y False si los índices estaban fuera de rango.
        """
        if i < 0 or i >= self._filas:
            return False # Índice de fila inválido
        
        fila = self._obtenerFila(i)
        
        if fila is not None:
            # El método reemplazar ya devuelve True o False
            return fila.reemplazar(j, valor)
        
        return False

    def get(self, i, j):
        """
        Este método ahora retorna el valor o None si los índices
        estaban fuera de rango.
        """
        if i < 0 or i >= self._filas:
            return None # Índice de fila inválido
            
        fila = self._obtenerFila(i)
        
        if fila is not None:
            # El método obtener ya devuelve el dato o None
            return fila.obtener(j)
        
        return None

    def getFilas(self):
        return self._filas

    def getColumnas(self):
        return self._columnas

    def imprimir(self):
        resultado = ""
        i = 0
        while i < self._filas:
            # el bucle con getFilas(), el índice 'i' siempre será válido.
            fila = self._datos.obtener(i)
            cadena_fila = ""
            j = 0
            while j < self._columnas:
                if j > 0:
                    cadena_fila += " "
                
                # Lo mismo para el índice 'j'
                valor = fila.obtener(j)
                cadena_fila += str(valor)
                j += 1
            
            resultado += cadena_fila
            if i < self._filas - 1:
                resultado += "\n"
            i += 1
        return resultado