#función para contar el numero de ocurrencias del idioma que indico el usuario

def idioma(ruta_archivo,idioma_user):
     
    
    idioma_search = idioma_user.strip().upper()
     
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
           
           # Tenemos que recorrer cada fila solo por la columna de idiomas
           
         dic_ocurrencias_user = {}
         es_encabezado = True
         ocurrencias_user = 0
         for linea in archivo:
                 
             #saltamos la aplicación del codigo a la primera fila que corresponde al encabezado
             if es_encabezado:
                es_encabezado = False
                continue
             #creamos la variable que vamos a analizar
             columna = linea.strip().split(",")
             lectura_idioma = columna[4].upper()
               
             #contamos las veces que aparece un idioma por linea
             if lectura_idioma == idioma_search:
                 ocurrencias_user += 1
             else:
                 continue
             # agregamos a nuestro diccionario el valor y ocurrecias del idioma que digito el usuario
         idioma_search = idioma_search.capitalize()
         dic_ocurrencias_user[idioma_search.capitalize()] = ocurrencias_user

         # esta función devuelve cuantas veces aparece el idioma solicitado
         return dic_ocurrencias_user

def idiomas(ruta_archivo):
    
    #estos son los idiomas que aparecen en nuestro archivo PEQUEÑO

    idiomas_org = {}
    es_encabezado = True

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:

        for lineas in archivo:

            if es_encabezado:
                es_encabezado = False
                continue
             #creamos la variable que vamos a analizar
            columna = lineas.strip().split(",")
            lectura_idioma = columna[4].upper()
            if lectura_idioma.capitalize() not in idiomas_org:
                idiomas_org[lectura_idioma.capitalize()] = 1
                
            else:
                idiomas_org[lectura_idioma.capitalize()] += 1 
        return sorted(idiomas_org.items())

# Función para agrupar y contar por tipo de contenido (Jim)
def tipos_contenido(ruta_archivo):
    conteos_tipo = {}
    es_encabezado = True

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if es_encabezado:
                es_encabezado = False
                continue
            
            columnas = linea.strip().split(",")
            # Según tu imagen, content_type es la columna índice 4
            tipo = columnas[4].strip().capitalize()
            
            if tipo not in conteos_tipo:
                conteos_tipo[tipo] = 1
            else:
                conteos_tipo[tipo] += 1
                
    # Ordenar de mayor a menor frecuencia como pide la guía
    resultado_ordenado = sorted(conteos_tipo.items(), key=lambda x: x[1], reverse=True)
    return resultado_ordenado
