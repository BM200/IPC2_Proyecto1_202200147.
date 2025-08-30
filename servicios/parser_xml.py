import xml.etree.ElementTree as ET
from modelos.campo import CampoAgricola
from modelos.estacion import EstacionBase
from modelos.sensor import SensorSuelo, SensorCultivo
from modelos.frecuencia import Frecuencia
from modelos.lista import ListaEnlazada

class ParserXML:
    @staticmethod
    def parse(ruta):
        try:
            # Intenta parsear el archivo. Si la ruta es incorrecta o el XML está mal formado,
            # esto lanzará un error que será capturado por el bloque 'except'.
            tree = ET.parse(ruta)
            root = tree.getroot()
            
            listaCampos = ListaEnlazada()

            # El bucle for...in... aquí es aceptable porque opera sobre los objetos
            # temporales de la librería ET, no sobre nuestras estructuras de datos.
            for nodoCampo in root.findall("campo"):
                c = CampoAgricola(nodoCampo.get("id"), nodoCampo.get("nombre"))

                estacionesNode = nodoCampo.find("estacionesBase")
                if estacionesNode is not None:
                    for eNode in estacionesNode.findall("estacion"):
                        c.getEstaciones().agregar(EstacionBase(eNode.get("id"), eNode.get("nombre")))

                sensoresSueloNode = nodoCampo.find("sensoresSuelo")
                if sensoresSueloNode is not None:
                    for sNode in sensoresSueloNode.findall("sensorS"):
                        s = SensorSuelo(sNode.get("id"), sNode.get("nombre"))
                        for fNode in sNode.findall("frecuencia"):
                            s.agregarFrecuencia(Frecuencia(fNode.get("idEstacion"), int(fNode.text)))
                        c.getSensoresSuelo().agregar(s)

                sensoresCultivoNode = nodoCampo.find("sensoresCultivo")
                if sensoresCultivoNode is not None:
                    for tNode in sensoresCultivoNode.findall("sensorT"):
                        t = SensorCultivo(tNode.get("id"), tNode.get("nombre"))
                        for fNode in tNode.findall("frecuencia"):
                            t.agregarFrecuencia(Frecuencia(fNode.get("idEstacion"), int(fNode.text)))
                        c.getSensoresCultivo().agregar(t)

                listaCampos.agregar(c)

            return listaCampos

        except FileNotFoundError:
            # Este error es específico: la ruta del archivo no existe.
            print(f"\n¡ERROR DE PARSEO! No se pudo encontrar el archivo en la ruta: '{ruta}'")
            print("Por favor, verifique que la ruta es correcta y el archivo existe.")
            return None # Retorna None para que el main.py sepa que la carga falló.
        
        except ET.ParseError as e:
            # Este error ocurre si el archivo existe pero su contenido no es un XML válido.
            print(f"\n¡ERROR DE PARSEO! El archivo '{ruta}' está mal formado y no se puede leer.")
            print(f"Detalle del error: {e}")
            return None
            
        except Exception as e:
            # Captura cualquier otro error inesperado durante el parseo.
            print(f"\n¡ERROR INESPERADO DURANTE EL PARSEO!")
            print(f"Tipo de Error: {type(e).__name__}")
            print(f"Mensaje: {e}")
            return None