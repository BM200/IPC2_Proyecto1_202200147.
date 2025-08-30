import xml.etree.ElementTree as ET
from xml.dom import minidom # Usado para darle un formato "bonito" (indentado) al XML de salida
import os
class EscritorXML:

    @staticmethod
    def escribir(lista_campos, ruta_archivo):
        """
        Genera un archivo XML a partir de la lista de campos agrícolas procesados,
        utilizando la librería ElementTree para una construcción robusta.
        """
        # --- VERIFICACIÓN DE RUTA ---
        try:
            directorio = os.path.dirname(ruta_archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)
        except Exception as e:
            print(f"¡ERROR CRÍTICO! No se pudo verificar o crear el directorio para la ruta de salida.")
            print(f"Detalle del error: {e}")
            return False
            
        # --- CONSTRUCCIÓN DEL XML ---
        root = ET.Element("camposAgricolas")

        # Iterar sobre cada campo en nuestra ListaEnlazada
        i = 0
        while i < lista_campos.getTam():
            campo = lista_campos.obtener(i)
            
            campo_node = ET.SubElement(root, "campo", {
                "id": campo.getId(),
                "nombre": campo.getNombre()
            })

            # 1. Construir estacionesBaseReducidas ---
            estaciones_reducidas_node = ET.SubElement(campo_node, "estacionesBaseReducidas")
            grupos = campo.grupos
            
            j = 0
            while j < grupos.getTam():
                grupo = grupos.obtener(j)
                # Leemos los datos directamente del objeto Grupo ya procesado
                ET.SubElement(estaciones_reducidas_node, "estacion", {
                    "id": grupo.getIdReducida(),
                    "nombre": grupo.getNombreAgrupado()
                })
                j += 1

            # --- 2. Construir <sensoresSuelo> ---
            sensores_suelo_node = ET.SubElement(campo_node, "sensoresSuelo")
            sensores_suelo = campo.getSensoresSuelo()
            Fr_ns = campo.Fr_ns

            k = 0 # Iterador para sensores (columnas)
            while k < sensores_suelo.getTam():
                sensor = sensores_suelo.obtener(k)
                sensor_node = ET.SubElement(sensores_suelo_node, "sensorS", {
                    "id": sensor.getId(),
                    "nombre": sensor.getNombre()
                })
                
                j = 0 # Iterador para grupos (filas)
                while j < grupos.getTam():
                    frecuencia_reducida = Fr_ns.get(j, k)
                    if frecuencia_reducida > 0:
                        grupo = grupos.obtener(j)
                        # Leemos el ID reducido directamente del objeto Grupo
                        frecuencia_node = ET.SubElement(sensor_node, "frecuencia", {
                            "idEstacion": grupo.getIdReducida()
                        })
                        frecuencia_node.text = str(frecuencia_reducida)
                    j += 1
                k += 1

            # --- 3. Construir <sensoresCultivo> ---
            sensores_cultivo_node = ET.SubElement(campo_node, "sensoresCultivo")
            sensores_cultivo = campo.getSensoresCultivo()
            Fr_nt = campo.Fr_nt

            k = 0
            while k < sensores_cultivo.getTam():
                sensor = sensores_cultivo.obtener(k)
                sensor_node = ET.SubElement(sensores_cultivo_node, "sensorT", {
                    "id": sensor.getId(),
                    "nombre": sensor.getNombre()
                })

                j = 0
                while j < grupos.getTam():
                    frecuencia_reducida = Fr_nt.get(j, k)
                    if frecuencia_reducida > 0:
                        grupo = grupos.obtener(j)
                        # Leemos el ID reducido directamente del objeto Grupo
                        frecuencia_node = ET.SubElement(sensor_node, "frecuencia", {
                            "idEstacion": grupo.getIdReducida()
                        })
                        frecuencia_node.text = str(frecuencia_reducida)
                    j += 1
                k += 1
            
            i += 1

        # --- ESCRITURA EN ARCHIVO ---
        try:
            xml_string_bytes = ET.tostring(root, 'utf-8')
            reparsed = minidom.parseString(xml_string_bytes)
            pretty_xml_string = reparsed.toprettyxml(indent="    ")

            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(pretty_xml_string)
            return True
        except Exception as e:
            print(f"\n¡¡¡ SE PRODUJO UN ERROR DURANTE LA ESCRITURA DEL ARCHIVO !!!")
            print(f"Tipo de Error: {type(e).__name__}")
            print(f"Mensaje de Error: {e}")
            return False
              


    
    

    
