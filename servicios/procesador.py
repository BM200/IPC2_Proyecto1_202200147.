from modelos.lista import ListaEnlazada
from modelos.campo import CampoAgricola
from modelos.matriz import Matriz
from modelos.grupo import Grupo

class Procesador: # CAMBIO: Nombre de la clase ajustado

    @staticmethod
    def _encontrar_indice_estacion(lista_estaciones, id_estacion_buscado):
        tam = lista_estaciones.getTam()
        i = 0
        while i < tam:
            estacion = lista_estaciones.obtener(i)
            if estacion.getId() == id_estacion_buscado:
                return i
            i += 1
        return None

    @staticmethod
    def _crear_matrices_frecuencia(campo):
        lista_estaciones = campo.getEstaciones()
        lista_sensores_suelo = campo.getSensoresSuelo()
        lista_sensores_cultivo = campo.getSensoresCultivo()

        num_estaciones = lista_estaciones.getTam()
        num_sensores_suelo = lista_sensores_suelo.getTam()
        num_sensores_cultivo = lista_sensores_cultivo.getTam()

        F_ns = Matriz(num_estaciones, num_sensores_suelo)
        F_nt = Matriz(num_estaciones, num_sensores_cultivo)

        j = 0 
        while j < num_sensores_suelo:
            sensor = lista_sensores_suelo.obtener(j)
            frecuencias_sensor = sensor.getFrecuencias()
            
            k = 0
            while k < frecuencias_sensor.getTam():
                frecuencia = frecuencias_sensor.obtener(k)
                i = Procesador._encontrar_indice_estacion(lista_estaciones, frecuencia.getIdEstacion())
                if i is not None:
                    F_ns.set(i, j, frecuencia.getValor())
                k += 1
            j += 1
        
        j = 0
        while j < num_sensores_cultivo:
            sensor = lista_sensores_cultivo.obtener(j)
            frecuencias_sensor = sensor.getFrecuencias()

            k = 0
            while k < frecuencias_sensor.getTam():
                frecuencia = frecuencias_sensor.obtener(k)
                i = Procesador._encontrar_indice_estacion(lista_estaciones, frecuencia.getIdEstacion())
                if i is not None:
                    F_nt.set(i, j, frecuencia.getValor())
                k += 1
            j += 1
            
        campo.F_ns = F_ns
        campo.F_nt = F_nt

    @staticmethod
    def _crear_matrices_patrones(campo):
        """
        Metodo que crea las matrices de patrones Fp[n,s] y Fp[n,t] a partir
        de las matrices de frecuencias existentes en el campo. 
        """
        F_ns = campo.F_ns
        F_nt = campo.F_nt

        num_filas_ns = F_ns.getFilas()
        num_cols_ns = F_ns.getColumnas()
        num_filas_nt = F_nt.getFilas()
        num_cols_nt = F_nt.getColumnas()
        #crea las nuevaas matrices de patrones Fp ns y nt
        
        Fp_ns = Matriz(num_filas_ns, num_cols_ns)
        Fp_nt = Matriz(num_filas_nt, num_cols_nt)

        #llenar la matriz de patrones de suelo

        i=0
        while i< num_filas_ns:
            j=0
            while j < num_cols_ns:
                if F_ns.get(i, j) > 0:
                    Fp_ns.set(i, j, 1)
                j += 1
            i += 1
        #llenar la matriz de patrones de cultivo
        i = 0
        while i < num_filas_nt:
            j=0 
            while j < num_cols_nt:
                if F_nt.get(i,j) >0:
                    Fp_nt.set(i,j, 1)
                j += 1
            i += 1
            #se guardan las matrices generadas en el objeto campo
        campo.Fp_ns = Fp_ns
        campo.Fp_nt = Fp_nt



    @staticmethod
    def procesar(lista_campos):
        if not lista_campos or lista_campos.getTam() == 0:
            print("No hay campos para procesar.")
            return

        print("\nIniciando procesamiento de campos...")
        
        i = 0
        while i < lista_campos.getTam():
            campo = lista_campos.obtener(i)
            print(f"\n--- Procesando Campo: {campo.getNombre()} ---")
            
            Procesador._crear_matrices_frecuencia(campo)

            Procesador._crear_matrices_patrones(campo)
            
            # TODO: Aquí llamaremos a las futuras funciones para crear patrones y agrupar
            
            print(f"Matriz de Frecuencia Suelo (F[n,s]) para {campo.getId()}:")
            print(campo.F_ns.imprimir())
            
            #Imprimir la nueva matriz de patrones para verificar
            print(f"\nMatriz de Patrones Suelo (Fp[n,s]) para {campo.getId()}:")
            print(campo.Fp_ns.imprimir())

            print(f"\nMatriz de Frecuencia Cultivo (F[n,t]) para {campo.getId()}:")
            print(campo.F_nt.imprimir())
            
            # Imprimir la nueva matriz de patrones para verificar
            print(f"\nMatriz de Patrones Cultivo (Fp[n,t]) para {campo.getId()}:")
            print(campo.Fp_nt.imprimir())
                  
            i += 1