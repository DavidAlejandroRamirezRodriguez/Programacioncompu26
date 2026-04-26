def cargar_datos(ruta):
    #Se crea una lista para guardar las filas
    datos = []
    #Abrimos el archivo
    try:
        with open(ruta, encoding="utf-8") as archivo:
            archivo.readline() 
        # Recorremos el archivo linea por linea, maximo 50 filas
            for i, linea in enumerate(archivo):
                if i >= 50:
                    break
                linea = linea.strip()# eliminamos espacios
                columnas = linea.split(",")# Dividimos la linea en columnas
                if len(columnas) >= 9:
                    datos.append(columnas)# Guardamos las filas en la lista
        return datos
    except FileNotFoundError:
        print(f"El archivo {ruta} no existe en este directorio")
        return []
def buscar(datos, termino):
    contador = 0
    # Variable que guarda la cantidad de concidencias
    for fila in datos:    
        # Convertimos la fila en un solo string
        # Ejemplo: ["Juan", "20", "Bogota"] → "Juan,20,Bogota"
        fila_completa = ",".join(fila)
        # Ignoramos mayusculas y minusculas
        if termino.lower() in fila_completa.lower():
            # Imprimimos la fila encontrada
            print(fila)
            contador += 1
            # Sumamos 1 al contador

    print(f"Se encontraron {contador} registros.")
    # Mostramos el total de coincidencias encontradas

def convertir(valor_str):
    valor_str = valor_str.strip().upper() #quita los espacios en blanco y lo pone en mayusculas 
    
    #como el valor es un string se pone esta condicion para regresar un float y poderlo utilizar
    if valor_str == '' or valor_str == '0':
        return 0.0
    #defini esta variable para poder pasar los numeros a float
    multiplicador = 1
    
    #se revisa con que letra termina y se le asigna el multiplicador para dejar el número plano
    if valor_str.endswith('B'): #si termina con B
        multiplicador = 1000000000
    #corte el texto para quitar la última letra '16.8B'='16.8'
        valor_str = valor_str[:-1] 
    elif valor_str.endswith('M'):
        multiplicador = 1000000
        valor_str = valor_str[:-1]
    elif valor_str.endswith('K'):
        multiplicador = 1000
        valor_str = valor_str[:-1]
        
    #converti el texto a decimal y lo multiplicamos
    #defini la variable para que pase de str a float y se multiplique por el valor correspondiente segun su letra 
    #Falto un bloque try-except para que no colapse si hay un texto que no es legible
    try:
        valor_final = float(valor_str) * multiplicador
        return valor_final
    except ValueError:
        return 0.0

def filtrar_por_vistas(ruta_archivo):
    #Esta función permite filtrar videos en base al umbral de vistas definido por el usuario
    print("\n" + "-"*30)
    print("FILTRADO PERSONALIZADO")
    print("-"*30)
    try:
        # Pedimos el umbral al usuario. Usamos float porque las vistas pueden tener decimales (ej. 16.8)
        umbral = float(input("Ingrese el mínimo de vistas a buscar: "))
        
        # Abrimos el archivo usando la ruta que recibe la función
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            
            # Saltamos la primera línea (encabezado) para no procesar texto como número
            next(archivo)
            
            contador_encontrados = 0
            print(f"\nBuscando videos con {umbral} o más vistas...")
            
            # Bucle para recorrer el archivo línea por línea
            for linea in archivo:
                # Quitamos el salto de línea al final y separamos por comas
                columnas = linea.strip().split(',')
                
                # Verificamos que la línea tenga todas las columnas para evitar errores
                if len(columnas) < 9:
                    continue
                
                # Extraemos datos usando índices:
                # [1] es el título (2da columna)
                # [-2] es la penúltima columna donde están las vistas
                titulo = columnas[1]
                vistas_texto = columnas[-2]
                
                # Convertimos el texto a número usando la función convertir de mi compañero
                # Esto es necesario para poder hacer la comparación matemática
                vistas_numericas = convertir(vistas_texto)
                
                # Evaluamos la condición de filtrado
                if vistas_numericas >= umbral:
                    print(f" * ENCONTRADO: {titulo} ({vistas_numericas} vistas)")
                    contador_encontrados += 1
            
            # Resumen final de la búsqueda
            if contador_encontrados > 0:
                print(f"\nSe encontraron {contador_encontrados} resultados.")
            else:
                print("\nNo hay videos que superen ese número de vistas.")
                
    except ValueError:
        # Si el usuario escribe letras en lugar de números, el programa no se cierra
        print("\nERROR: Debe ingresar un valor numérico válido.")
        
#Función principal para calcular
def procesar_estadisticas(datos):
    # CAMBIO: La función ahora recibe la matriz 'datos' en memoria, no la ruta del disco.
    
    contador = 0 
    # Cree las variables acumuladoras para guardar el número más alto, el más bajo y la suma de todos y el contador para saber cuántas filas proceso.
    max_val_vistas = 0.0
    min_val_vistas = 0.0
    sumatoria_vistas = 0.0
    
    #Cree las variables de estado para los likes y los nombres de los videos.
    max_val_likes = 0.0
    min_val_likes = 0.0
    sumatoria_likes = 0.0
    nombre_max_vistas = ""
    nombre_min_vistas = ""
    nombre_max_likes = ""
    nombre_min_likes = ""
    
    # Identifique el encabezado(primer fila) que son los titulos y estos no se procesan como números
    
    # Hice esto para que el primer número procesado se convierta en el primer mínimo y el primer máximo
    es_primer_dato = True
    
    # Abri el archivo de forma normal
    # CAMBIO:Ya no abrimps el archivo físico. Iteramos directamente sobre la memoria RAM.
    for columnas in datos:
        
        # Valido que la fila no este rota o vacia para que no de error
        if len(columnas) < 9:
            continue
            
        nombre_video = columnas[1]#extrae el nombre del video que está en la segunda posición
        vistas_str = columnas[-2]# accede a la penultima columna
        likes_str = columnas[-1]#accede a la última columna para los likes
        
        #Llama a la función de transformar el texto a un número de vistas y likes
        valor_numerico_vistas = convertir(vistas_str)
        valor_numerico_likes = convertir(likes_str)
        
        ##Condicion que faltaba para que el primer numero sea el mas grande y el mas pequeño de los numeros
        if es_primer_dato == True:
            # Si es el primer dato que se lee, es el mayor y el menor a la vez.
            max_val_vistas = valor_numerico_vistas
            min_val_vistas = valor_numerico_vistas
            
            #Inicia en la primera pasada las variables de likes y de los nombres
            max_val_likes = valor_numerico_likes
            min_val_likes = valor_numerico_likes
            nombre_max_vistas = nombre_video
            nombre_min_vistas = nombre_video
            nombre_max_likes = nombre_video
            nombre_min_likes = nombre_video
            
            #Esto es porque como la fila tiene los titulos de las columnas pues no se pueden procesar ni nos interesa que se procese
            es_primer_dato = False 
        else:
            # y sii no es el primero, se compara con los que ya se tienen guardados
            if valor_numerico_vistas > max_val_vistas:
                max_val_vistas = valor_numerico_vistas
                nombre_max_vistas = nombre_video

            if valor_numerico_vistas < min_val_vistas:
                min_val_vistas = valor_numerico_vistas
                nombre_min_vistas = nombre_video

            if valor_numerico_likes > max_val_likes:
                max_val_likes = valor_numerico_likes
                nombre_max_likes = nombre_video
            
            if valor_numerico_likes < min_val_likes:
                min_val_likes = valor_numerico_likes
                nombre_min_likes = nombre_video
                
        #Suma el valor actual al total que ya esta acomulado y se suma 1 al contador de registros.
        sumatoria_vistas = sumatoria_vistas + valor_numerico_vistas
        sumatoria_likes = sumatoria_likes + valor_numerico_likes
        contador = contador + 1
            
    # Se divide la suma total entre el número de filas procesadas
    promedio_vistas = 0.0
    promedio_likes = 0.0
    if contador > 0:
        promedio_vistas = sumatoria_vistas / contador
        promedio_likes = sumatoria_likes / contador
        
    # Envia los resultados finalaes listos para usarlos fuera de la función
    # ahora hice que retornara un diccionario que es necesario para manejar muchas variables sin que
    # se cruzen los datos
    return {
        "max_v": max_val_vistas, "nom_max_v": nombre_max_vistas,
        "min_v": min_val_vistas, "nom_min_v": nombre_min_vistas,
        "max_l": max_val_likes, "nom_max_l": nombre_max_likes,
        "min_l": min_val_likes, "nom_min_l": nombre_min_likes,
        "prom_v": promedio_vistas, "prom_l": promedio_likes,
        "contador": contador
    }
    #Ya esta el contador, el promedioo el return que envia los resultados finales.a
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
             if len(columna) < 9:
                 continue
             lectura_idioma = columna[-6].upper()
               
             #contamos las veces que aparece un idioma por linea
             if lectura_idioma == idioma_search:
                 ocurrencias_user += 1
             else:
                 continue
             # agregamos a nuestro diccionario el valor y ocurrecias del idioma que digito el usuario
         idioma_search = idioma_search.capitalize()
         dic_ocurrencias_user[idioma_search.capitalize()] = ocurrencias_user
         

         # esta función devuelve cuantas veces aparece el idioma solicitado
         return  sorted(dic_ocurrencias_user.items())
                  
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
            if len(columna) < 9:
                continue
            lectura_idioma = columna[-6].upper()
            if lectura_idioma.capitalize() not in idiomas_org:
                idiomas_org[lectura_idioma.capitalize()] = 1
                
            else:
                idiomas_org[lectura_idioma.capitalize()] += 1 
        return sorted(idiomas_org.items(), key= lambda items: items[1], reverse= True)

def tipos_contenido(ruta_archivo):
    conteos_tipo = {}
    es_encabezado = True

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if es_encabezado:
                es_encabezado = False
                continue
            
            columnas = linea.strip().split(",")
            # Validación de seguridad para evitar desbordamiento de índices
            if len(columnas) < 9:
                continue
                
            # Extraemos el tipo de contenido (índice 4)
            tipo = columnas[4].strip().capitalize()
            
            if tipo not in conteos_tipo:
                conteos_tipo[tipo] = 1
            else:
                conteos_tipo[tipo] += 1
                
    # Retornamos la lista ordenada de mayor a menor frecuencia
    resultado_ordenado = sorted(conteos_tipo.items(), key=lambda x: x[1], reverse=True)
    return resultado_ordenado

def ejecutar_menu():
    ruta = "youtube_pequeño.csv"
    datos_sistema = cargar_datos(ruta)

    if not datos_sistema:
        return

    while True:
        print("\n" + "="*45)
        print("         DATA LAB - GESTIÓN DE VIDEOS")
        print("="*45)
        print("1. Buscar registros por término")
        print("2. Ver estadísticas generales (Vistas/Likes)")
        print("3. Filtrar por umbral de vistas")
        print("4. Analizar frecuencia de un idioma")
        print("5. Ver resumen de todos los idiomas")
        print("6. Salir")
        print("="*45)

        opcion = input("Selecciona una opción (1-6): ")

        if opcion == '1':
            termino = input("Ingresa el término a buscar: ")
            buscar(datos_sistema, termino)

        elif opcion == '2':
            res = procesar_estadisticas(datos_sistema)
            if res:
                print(f"\n--- RESUMEN ESTADÍSTICO (Top 50) ---")
                print(f"MÁS VISTO: {res['nom_max_v']} ({res['max_v']:,.0f})")
                print(f"MENOS VISTO: {res['nom_min_v']} ({res['min_v']:,.0f})")
                print(f"PROMEDIO VISTAS: {res['prom_v']:,.2f}")
                print(f"TOTAL VIDEOS: {res['contador']}")

        elif opcion == '3':
            filtrar_por_vistas(ruta)

        elif opcion == '4':
            target = input("¿Qué idioma desea contabilizar? ")
            resultado = idioma(ruta, target)
            for idioma_nom, cantidad in resultado:
                if cantidad != 1:
                    print(f"- Existen {cantidad} videos en {idioma_nom}")
                else:
                    print(f"- Existe {cantidad} video en {idioma_nom}")

        elif opcion == '5':
            resumen = idiomas(ruta)
            print("\nDISTRIBUCIÓN POR IDIOMA:")
            for idioma_nom, cantidad in resumen:
                print(f"- {idioma_nom}: {cantidad} videos")

        elif opcion == '6':
            print("\nSaliendo del sistema.")
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")

if __name__ == "__main__":
    ejecutar_menu()
