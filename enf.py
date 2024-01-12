# Importamos las librerías necesarias
import re  # Para operaciones con expresiones regulares
from datetime import datetime, timedelta  # Para manipular fechas y horas


# Función para eliminar texto previo a cierto patrón y guardar el resultado en un nuevo archivo
def eliminar_texto_previo(archivo_entrada, archivo_salida):
    # Leemos todas las líneas del archivo de entrada
    with open(archivo_entrada, 'r') as archivo_entrada:
        lineas = archivo_entrada.readlines()    

    encontrado = False  # Variable para controlar si se ha encontrado el patrón
    nuevas_lineas = []  # Lista para almacenar las líneas que cumplen con el patrón

    # Iteramos sobre cada línea del archivo
    for linea in lineas:
        # Si encontramos un patrón específico en la línea
        if re.search(r'\d{2}-\d{2}-\d{2};\d{2}:\d{2}:\d{2}.\d{3}', linea):
            encontrado = True  # Indicamos que se ha encontrado el patrón
            nuevas_lineas.append(linea)  # Agregamos la línea que coincide con el patrón
        # Si ya se encontró el patrón y la línea no coincide, la agregamos igualmente
        elif encontrado:
            nuevas_lineas.append(linea)

    # Escribimos las líneas encontradas en el archivo de salida
    with open(archivo_salida, 'w') as archivo_salida:
        archivo_salida.writelines(nuevas_lineas)

def depurar_archivo(archivo_entrada, archivo_salida):
    with open(archivo_entrada, 'r') as archivo_entrada:
        contenido = archivo_entrada.read()

    # Utilizamos una expresión regular para eliminar bloques entre '8*' y '7* r'
    contenido_depurado = re.sub(r'8\*.*?7\* r', '', contenido, flags=re.DOTALL)

    with open(archivo_salida, 'w') as archivo_salida:
        archivo_salida.write(contenido_depurado)


# Función para separar el contenido del archivo por un formato específico de fecha y hora
def separar_por_formato(archivo):
    with open(archivo, 'r') as file:
        contenido = file.read()
        # Utilizamos expresiones regulares para encontrar patrones que coincidan con el formato de fecha y hora
        patrones = re.findall(r'\d{2}-\d{2}-\d{2};\d{2}:\d{2}:\d{2}\.\d+', contenido)
        # Usamos la función split con los patrones encontrados para separar la información
        datos_separados = re.split(r'\d{2}-\d{2}-\d{2};\d{2}:\d{2}:\d{2}\.\d+', contenido)
        # Eliminamos los espacios en blanco y elementos vacíos
        datos_separados = [dato.strip() for dato in datos_separados if dato.strip()]
        # Combinamos los patrones y los datos separados en una lista de tuplas
        lista_final = list(zip(patrones, datos_separados))
        return lista_final

# Función para buscar en las tuplas desde la hora de inicio y avanzar un segundo más
def buscar_en_tupla(lista_tuplas, hora_inicio):
    hora_inicio = hora_inicio + ".000"
    formato_hora = '%d-%m-%y;%H:%M:%S.%f'  # Ajustamos el formato para incluir la fecha
    hora_inicio_dt = datetime.strptime(hora_inicio, formato_hora)

    # Encontramos la tupla más cercana
    tupla_mas_cercana = min(lista_tuplas, key=lambda tupla: abs(datetime.strptime(tupla[0], formato_hora) - hora_inicio_dt))

    # Calculamos la hora de inicio para tomar desde un segundo después
    hora_inicio_nueva = datetime.strptime(tupla_mas_cercana[0], formato_hora) + timedelta(seconds=1)

    # Filtramos las tuplas que están a partir de la nueva hora de inicio
    resultados = [tupla for tupla in lista_tuplas if datetime.strptime(tupla[0], formato_hora) >= hora_inicio_nueva and datetime.strptime(tupla[0], formato_hora) <= hora_inicio_nueva + timedelta(minutes=1)]

    if not resultados:
        print(f"No se encontraron datos desde un segundo después de la hora más cercana: {hora_inicio_nueva.strftime(formato_hora)}")

    return resultados




def depuracion(FindTime):
    if FindTime == []:
        print("No hay datos que depurar")
    else:
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
                    print("ok2")
                # Convierte la fecha y hora a cadena antes de imprimir
                print(str(FindTime[i].get('Fecha y Hora')))
        else:
            print("No se encontraron datos en el rango de tiempo especificado.")
    return FindTime


# Código principal
if __name__ == "__main__":
    archivo_entrada = "ems.cap"  # Nombre del archivo de entrada
    archivo_salida = "ems_limpio.txt"  # Nombre del archivo de salida
    depurar_archivo(archivo_entrada, archivo_salida)
    eliminar_texto_previo(archivo_entrada, archivo_salida)  # Eliminamos texto previo al patrón en el archivo de entrada
    salida = separar_por_formato('ems_limpio.txt')  # Separamos el contenido del archivo limpio por el formato de fecha y hora
    FindTime = buscar_en_tupla(salida, '24-01-11;14:13:59')  # Ajustamos el formato de la hora # Buscamos en las tuplas desde la hora de inicio
    
    FindTime=depuracion(FindTime)
    
    
    
    
    
