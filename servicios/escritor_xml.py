import xml.etree.ElementTree as ET
from xml.dom import minidom # Usado para darle un formato "bonito" (indentado) al XML de salida

class EscritorXML:

    @staticmethod
    def escribir(lista_campos, ruta_archivo):
        """
        Genera un archivo XML a partir de la lista de campos agrícolas procesados,
        utilizando la librería ElementTree para una construcción robusta.
        """
        # Crear el elemento raíz <camposAgricolas>
        root = ET.Element("camposAgricolas")

        # Iterar sobre cada campo en nuestra ListaEnlazada
        i = 0
        while i < lista_campos.getTam():
            campo = lista_campos.obtener(i)
            
            # Crear el elemento <campo> con sus atributos
            campo_node = ET.SubElement(root, "campo", {
                "id": campo.getId(),
                "nombre": campo.getNombre()
            })

            # --- 1. Construir <estacionesBaseReducidas> ---
            estaciones_reducidas_node = ET.SubElement(campo_node, "estacionesBaseReducidas")
            grupos = campo.grupos
            
            j = 0
            while j < grupos.getTam():
                grupo = grupos.obtener(j)
                indices_grupo = grupo.getIndices()
                
                primer_indice = indices_grupo.obtener(0)
                primera_estacion_del_grupo = campo.getEstaciones().obtener(primer_indice)
                id_reducido = primera_estacion_del_grupo.getId()
                
                nombres_concatenados = ""
                k = 0
                while k < indices_grupo.getTam():
                    indice_actual = indices_grupo.obtener(k)
                    estacion_actual = campo.getEstaciones().obtener(indice_actual)
                    nombres_concatenados += estacion_actual.getNombre()
                    if k < indices_grupo.getTam() - 1:
                        nombres_concatenados += ", "
                    k += 1
                
                ET.SubElement(estaciones_reducidas_node, "estacion", {
                    "id": id_reducido,
                    "nombre": nombres_concatenados
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
                        primer_indice_grupo = grupo.getIndices().obtener(0)
                        id_estacion_reducida = campo.getEstaciones().obtener(primer_indice_grupo).getId()
                        
                        frecuencia_node = ET.SubElement(sensor_node, "frecuencia", {
                            "idEstacion": id_estacion_reducida
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
                        primer_indice_grupo = grupo.getIndices().obtener(0)
                        id_estacion_reducida = campo.getEstaciones().obtener(primer_indice_grupo).getId()

                        frecuencia_node = ET.SubElement(sensor_node, "frecuencia", {
                            "idEstacion": id_estacion_reducida
                        })
                        frecuencia_node.text = str(frecuencia_reducida)
                    j += 1
                k += 1
            
            i += 1

        # --- Escribir el árbol XML al archivo ---
        try:
            # Convertir el árbol de ElementTree a un string de bytes
            xml_string_bytes = ET.tostring(root, 'utf-8')
            
            # Usar minidom para "que se visualice mejor" el XML con indentación
            reparsed = minidom.parseString(xml_string_bytes)
            pretty_xml_string = reparsed.toprettyxml(indent="    ")

            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(pretty_xml_string)
            return True
        except Exception as e:
            print(f"Error al escribir el archivo XML de salida: {e}")
            return False

              


    
    

    
