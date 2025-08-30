import os
from servicios.parser_xml import ParserXML
from servicios.procesador import Procesador
from servicios.escritor_xml import EscritorXML
from servicios.generador_graficos import GeneradorGraficos

def mostrarMenu():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Cargar archivo XML de entrada")
    print("2. Procesar datos")
    print("3. Escribir archivo XML de salida")
    print("4. Mostrar datos del estudiante")
    print("5. Generar gráfica")
    print("6. Salir")
    opcion = input("Seleccione una opción: ")
    return opcion

def main():
    campos = None
    procesado = False
    directorio_proyecto = os.getcwd()
    
    while True:
        opcion = mostrarMenu()

        if opcion == "1":
            # ... (sin cambios)
            ruta_sugerida = os.path.join(directorio_proyecto, 'datos', 'archivo_entrada.xml')
            print(f"Ingrese ruta del archivo XML de entrada (ej: {ruta_sugerida})")
            ruta = input("> ")
            campos = ParserXML.parse(ruta)
            if campos and campos.getTam() > 0:
                print(f"Archivo cargado correctamente. Se encontraron {campos.getTam()} campos.")
                procesado = False
            else:
                print("Error al cargar el archivo.")
                campos = None

        elif opcion == "2":
            # ... (sin cambios)
            if campos is None: continue
            Procesador.procesar(campos)
            procesado = True
            print("\nProcesamiento completado.")

        elif opcion == "3":
            # ... (sin cambios)
            if campos is None or not procesado: continue
            nombre_archivo = input("Ingrese el nombre para el archivo de salida (ej: salida.xml): ")
            ruta_salida_final = os.path.join(directorio_proyecto, 'datos', nombre_archivo)
            print(f"\nSe guardará el archivo en: {ruta_salida_final}")
            if EscritorXML.escribir(campos, ruta_salida_final):
                print(f"Archivo de salida generado exitosamente.")
            else:
                print("Hubo un error al generar el archivo de salida.")

        elif opcion == "4":
            # ... (sin cambios)
            print("\n--- DATOS DEL ESTUDIANTE ---")
            print("Nombre: Mario Rodrigo Balam Churunel")
            print("Carné: 202200147")
            print("Curso: Introducción a la Programación y Computación 2")
            print("Semestre: 4to. Semestre")
            print("-----------------------------")

        elif opcion == "5":
            if not procesado:
                print("Debe procesar los datos (Opción 2) antes de generar una gráfica.")
                continue
            
            # 1. Seleccionar el campo
            print("\n--- Seleccione un Campo Agrícola para Graficar ---")
            i = 0
            while i < campos.getTam():
                print(f"{i + 1}. {campos.obtener(i).getNombre()}")
                i += 1
            try:
                opcion_campo = int(input("> ")) - 1
                campo_seleccionado = campos.obtener(opcion_campo)
                if campo_seleccionado is None: raise ValueError()
            except (ValueError, IndexError):
                print("Opción de campo inválida.")
                continue
            
            # 2. Seleccionar el tipo de matriz (F, Fp, Fr)
            print("\n--- ¿Qué tipo de matriz desea graficar? ---")
            print("1. Matriz de Frecuencia (F)")
            print("2. Matriz de Patrones (Fp)")
            print("3. Matriz Reducida (Fr)")
            opcion_tipo = input("> ")
            
            # --- SE AÑADE CORRECCIÓN: AÑADIR SUBMENÚ PARA ELEGIR SUELO O CULTIVO ---
            if opcion_tipo in ['1', '2', '3']:
                print("\n--- ¿Para Sensores de Suelo o de Cultivo? ---")
                print("1. Suelo")
                print("2. Cultivo")
                opcion_sensor = input("> ")

                matriz_a_graficar = None
                nombre_grafica = ""
                id_campo = campo_seleccionado.getId()

                if opcion_tipo == '1': # Frecuencia
                    if opcion_sensor == '1':
                        matriz_a_graficar = campo_seleccionado.F_ns
                        nombre_grafica = f"F_ns_Campo_{id_campo}"
                    elif opcion_sensor == '2':
                        matriz_a_graficar = campo_seleccionado.F_nt
                        nombre_grafica = f"F_nt_Campo_{id_campo}"
                
                elif opcion_tipo == '2': # Patrones
                    if opcion_sensor == '1':
                        matriz_a_graficar = campo_seleccionado.Fp_ns
                        nombre_grafica = f"Fp_ns_Campo_{id_campo}"
                    elif opcion_sensor == '2':
                        matriz_a_graficar = campo_seleccionado.Fp_nt
                        nombre_grafica = f"Fp_nt_Campo_{id_campo}"

                elif opcion_tipo == '3': # Reducida
                    if opcion_sensor == '1':
                        matriz_a_graficar = campo_seleccionado.Fr_ns
                        nombre_grafica = f"Fr_ns_Campo_{id_campo}"
                    elif opcion_sensor == '2':
                        matriz_a_graficar = campo_seleccionado.Fr_nt
                        nombre_grafica = f"Fr_nt_Campo_{id_campo}"
                
                if matriz_a_graficar and nombre_grafica:
                    GeneradorGraficos.renderizar_matriz(matriz_a_graficar, nombre_grafica)
                else:
                    print("Opción de sensor inválida.")
            else:
                print("Opción de tipo de matriz inválida.")

        elif opcion == "6":
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()