from modelos.lista import ListaEnlazada
from modelos.campo import CampoAgricola
from modelos.matriz import Matriz
from modelos.grupo import Grupo

class Procesador:

    @staticmethod
    def _encontrar_indice_estacion(lista_estaciones, id_estacion_buscado):
        """
        Busca una estación por su ID en una ListaEnlazada de estaciones y devuelve su índice.
        Retorna None si no la encuentra.
        """
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
        """
        AQUI, SE Crea y llena las matrices de frecuencia F[n,s] y F[n,t] para un campo agrícola.
        """
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
        Crea las matrices de patrones Fp[n,s] y Fp[n,t] a partir de las 
        matrices de frecuencia existentes en el campo.
        """
        F_ns = campo.F_ns
        F_nt = campo.F_nt
        
        num_filas_ns = F_ns.getFilas()
        num_cols_ns = F_ns.getColumnas()
        num_filas_nt = F_nt.getFilas()
        num_cols_nt = F_nt.getColumnas()

        Fp_ns = Matriz(num_filas_ns, num_cols_ns)
        Fp_nt = Matriz(num_filas_nt, num_cols_nt)
        
        i = 0
        while i < num_filas_ns:
            j = 0
            while j < num_cols_ns:
                if F_ns.get(i, j) > 0:
                    Fp_ns.set(i, j, 1)
                j += 1
            i += 1
            
        i = 0
        while i < num_filas_nt:
            j = 0
            while j < num_cols_nt:
                if F_nt.get(i, j) > 0:
                    Fp_nt.set(i, j, 1)
                j += 1
            i += 1
            
        campo.Fp_ns = Fp_ns
        campo.Fp_nt = Fp_nt

    @staticmethod
    def _comparar_filas_patron(campo, indice_fila1, indice_fila2):
        """
        Compara dos filas en ambas matrices de patrones.
        Retorna True si son idénticas, False en caso contrario.
        """
        Fp_ns = campo.Fp_ns
        Fp_nt = campo.Fp_nt

        j = 0
        while j < Fp_ns.getColumnas():
            if Fp_ns.get(indice_fila1, j) != Fp_ns.get(indice_fila2, j):
                return False
            j += 1
            
        j = 0
        while j < Fp_nt.getColumnas():
            if Fp_nt.get(indice_fila1, j) != Fp_nt.get(indice_fila2, j):
                return False
            j += 1
            
        return True

    @staticmethod
    def _lista_contiene(lista, valor_buscado):
        """
        Reemplaza el operador 'in' para nuestra ListaEnlazada.
        Retorna True si el valor se encuentra en la lista, False en caso contrario.
        """
        i = 0
        while i < lista.getTam():
            if lista.obtener(i) == valor_buscado:
                return True
            i += 1
        return False

    @staticmethod
    def _agrupar_estaciones(campo):
        """
        Agrupa las estaciones basándose en la similitud de sus patrones, 
        sin utilizar listas nativas de Python.
        """
        num_estaciones = campo.getEstaciones().getTam()
        if num_estaciones == 0:
            campo.grupos = ListaEnlazada()
            return

        indices_agrupados = ListaEnlazada()
        lista_de_grupos = ListaEnlazada()

        i = 0
        while i < num_estaciones:
            if Procesador._lista_contiene(indices_agrupados, i):
                i += 1
                continue
            
            nuevo_grupo = Grupo(f"grupo_{i}")
            nuevo_grupo.agregarIndice(i)
            indices_agrupados.agregar(i)

            j = i + 1
            while j < num_estaciones:
                if not Procesador._lista_contiene(indices_agrupados, j):
                    if Procesador._comparar_filas_patron(campo, i, j):
                        nuevo_grupo.agregarIndice(j)
                        indices_agrupados.agregar(j)
                j += 1
            
            lista_de_grupos.agregar(nuevo_grupo)
            i += 1
        
        campo.grupos = lista_de_grupos

    @staticmethod
    def _crear_matrices_reducidas(campo):
        """
        Crea las matrices reducidas Fr[n,s] y Fr[n,t] sumando 
        las frecuencias de las estaciones en cada grupo.
        """
        grupos = campo.grupos
        F_ns = campo.F_ns
        F_nt = campo.F_nt

        num_grupos = grupos.getTam()
        num_sensores_suelo = F_ns.getColumnas()
        num_sensores_cultivo = F_nt.getColumnas()

        Fr_ns = Matriz(num_grupos, num_sensores_suelo)
        Fr_nt = Matriz(num_grupos, num_sensores_cultivo)

        i = 0 
        while i < num_grupos:
            grupo_actual = grupos.obtener(i)
            indices_del_grupo = grupo_actual.getIndices()
            
            j = 0 
            while j < num_sensores_suelo:
                suma_frecuencias = 0
                k = 0 
                while k < indices_del_grupo.getTam():
                    indice_estacion_original = indices_del_grupo.obtener(k)
                    suma_frecuencias += F_ns.get(indice_estacion_original, j)
                    k += 1
                
                Fr_ns.set(i, j, suma_frecuencias)
                j += 1
            i += 1
            
        i = 0
        while i < num_grupos:
            grupo_actual = grupos.obtener(i)
            indices_del_grupo = grupo_actual.getIndices()
            j = 0
            while j < num_sensores_cultivo:
                suma_frecuencias = 0
                k = 0
                while k < indices_del_grupo.getTam():
                    indice_estacion_original = indices_del_grupo.obtener(k)
                    suma_frecuencias += F_nt.get(indice_estacion_original, j)
                    k += 1
                
                Fr_nt.set(i, j, suma_frecuencias)
                j += 1
            i += 1

        campo.Fr_ns = Fr_ns
        campo.Fr_nt = Fr_nt

    @staticmethod
    def procesar(lista_campos):
        """
        Función principal que ejecuta todos los pasos del procesamiento para cada campo.
        """
        if not lista_campos or lista_campos.getTam() == 0:
            print("No hay campos para procesar.")
            return

        print("\nIniciando procesamiento de campos...")
        
        i = 0
        while i < lista_campos.getTam():
            campo = lista_campos.obtener(i)
            print(f"\n--- Procesando Campo: {campo.getNombre()} ---")
            
            # Ejecutar todos los pasos en orden
            Procesador._crear_matrices_frecuencia(campo)
            Procesador._crear_matrices_patrones(campo)
            Procesador._agrupar_estaciones(campo)
            Procesador._crear_matrices_reducidas(campo)
            
            # --- Salida de Verificación ---
            print("Grupos de estaciones encontrados:")
            if campo.grupos.getTam() > 0:
                k = 0
                while k < campo.grupos.getTam():
                    grupo = campo.grupos.obtener(k)
                    indices = grupo.getIndices()
                    linea_grupo = f"Grupo {k+1}: Índices ["
                    m = 0
                    while m < indices.getTam():
                        linea_grupo += str(indices.obtener(m))
                        if m < indices.getTam() - 1:
                            linea_grupo += ", "
                        m += 1
                    linea_grupo += "]"
                    print(linea_grupo)
                    k += 1
            else:
                print("No se formaron grupos.")

            print(f"\nMatriz Reducida Suelo (Fr[n,s]):")
            print(campo.Fr_ns.imprimir())
            
            print(f"\nMatriz Reducida Cultivo (Fr[n,t]):")
            print(campo.Fr_nt.imprimir())
            
            i += 1