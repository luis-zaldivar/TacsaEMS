si queremos no usar el main el codigo que de la siguiente manera:

archivo_entrada = "ems.cap"  # Nombre del archivo de entrada
archivo_salida = "ems_limpio.txt"  # Nombre del archivo de salida
depurar_archivo(archivo_entrada, archivo_salida)
eliminar_texto_previo(archivo_entrada, archivo_salida)  # Eliminamos texto previo al patrón en el archivo de entrada
salida = separar_por_formato('ems_limpio.txt')  # Separamos el contenido del archivo limpio por el formato de fecha y hora
FindTime = buscar_en_tupla(salida, '14:13:59')  # Buscamos en las tuplas desde la hora de inicio

# Verificamos si hay resultados antes de realizar la depuración
if FindTime:
    print("Resultados encontrados.")
    # Iteramos sobre las tuplas para crear un diccionario con pares de clave-valor
    for i in range(len(FindTime)):
        FindTime[i] = {'Fecha y Hora': FindTime[i][0], 'Otro Campo': FindTime[i][1]}
# Iteramos nuevamente para realizar la depuración
    for i in range(len(FindTime)):
        if "*" in FindTime[i].get('Otro Campo'):
            DataClear = re.split(r'\d\*', FindTime[i].get('Otro Campo'))
            FindTime[i]['Otro Campo'] = DataClear[0]
        else:
            break
else:
    print("No se encontraron datos en el rango de tiempo especificado.")
