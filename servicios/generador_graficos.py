from graphviz import Source

class GeneradorGraficos:
    
    @staticmethod
    def generar_dot_matriz(matriz, nombre_matriz):
        """
        Toma un objeto Matriz de nuestro modelo y lo convierte en un string
        en formato DOT de Graphviz para renderizarlo como una tabla.
        """
        if matriz is None:
            return None

        #  construir el string DOT
        # shape=plaintext nos permite usar una "etiqueta" con formato de tabla HTML

        dot_string = f'digraph {nombre_matriz} {{\n'
        dot_string += '    node [shape=plaintext];\n'
        dot_string += f'    label="{nombre_matriz}";\n' # Título del grafo
        dot_string += '    matriz_node [label=<\n'
        dot_string += '        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">\n'
        
        # Iteramos sobre nuestra matriz para crear las filas y celdas de la tabla
        i = 0
        while i < matriz.getFilas():
            dot_string += '            <TR>\n' # Inicio de una fila de la tabla
            j = 0
            while j < matriz.getColumnas():
                valor = matriz.get(i, j)
                dot_string += f'                <TD>{valor}</TD>\n' # Celda de la tabla
                j += 1
            dot_string += '            </TR>\n' # Fin de la fila
            i += 1
            
        dot_string += '        </TABLE>\n'
        dot_string += '    >];\n'
        dot_string += '}\n'
        return dot_string

    @staticmethod
    def renderizar_matriz(matriz, nombre_matriz):
        """
        Toma una matriz, genera su código DOT y la renderiza en un archivo de imagen,
        luego intenta abrirla.
        """
        dot_code = GeneradorGraficos.generar_dot_matriz(matriz, nombre_matriz)
        if dot_code is None:
            print("La matriz seleccionada no existe o no ha sido generada.")
            return

        try:
            # se Crea un objeto Source con el código DOT
            # Lo guardará como 'nombre_matriz.gv' y 'nombre_matriz.gv.png'
            s = Source(dot_code, filename=nombre_matriz, format='png')
            
            # Renderiza la imagen y la abre
            s.view()
            print(f"Gráfica generada y abierta. Busca el archivo '{nombre_matriz}.gv.png'")
        except Exception as e:
            print("\nError al generar la gráfica. ¿Instalaste Graphviz y lo añadiste al PATH del sistema?")
            print(f"Detalle del error: {e}")