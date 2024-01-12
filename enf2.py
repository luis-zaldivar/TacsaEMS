# Importamos las librerías necesarias
import re  # Para operaciones con expresiones regulares
from datetime import datetime  # Para manipular fechas y horas

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


# Función para buscar en las tuplas dentro de un rango de tiempo específico
def buscar_en_tupla(lista_tuplas, hora_inicio, hora_fin):
    hora_inicio=hora_inicio+".000"
    hora_fin=hora_fin+".999"
    formato_hora = '%H:%M:%S.%f'  # Formato para la hora

    # Convertimos las horas de inicio y fin a objetos de tiempo
    hora_inicio_dt = datetime.strptime(hora_inicio, formato_hora).time()
    hora_fin_dt = datetime.strptime(hora_fin, formato_hora).time()

    resultados = []  # Lista para almacenar los resultados que cumplen con el rango de tiempo

    # Iteramos sobre las tuplas buscando las horas que estén dentro del rango especificado
    for t in lista_tuplas:
        separator = t[0].split(";")  # Separamos la hora de la tupla
        try:
            hora_actual = datetime.strptime(separator[1], formato_hora).time()  # Convertimos la hora actual a objeto de tiempo
            if hora_inicio_dt <= hora_actual <= hora_fin_dt:  # Verificamos si la hora está dentro del rango
                resultados.append(t)  # Si está en el rango, la añadimos a los resultados
        except ValueError:
            continue  # En caso de error, continuamos con la siguiente iteración

    return resultados  # Retornamos las tuplas que cumplen con el rango de tiempo


def depuracion(ListTupla):
    if ListTupla==[]:
        print("No hay datos que depurar")
    else:
        for i in range(len(FindTime)):
            # Crear un diccionario con pares de clave-valor a partir de la tupla
            FindTime[i] = {'Fecha y Hora': FindTime[i][0], 'Otro Campo': FindTime[i][1]}
            
        for i in range(len(FindTime)):
            if "*"in(FindTime[i].get('Otro Campo')):
                DataClear=re.split(r'\d\*',FindTime[i].get('Otro Campo'))
                FindTime[i]['Otro Campo'] = DataClear[0]
            else: break

# Código principal
if __name__ == "__main__":
    archivo_entrada = "ems.cap"  # Nombre del archivo de entrada
    archivo_salida = "ems_limpio.txt"  # Nombre del archivo de salida
    depurar_archivo(archivo_entrada, archivo_salida)
    a=depurar_archivo
    eliminar_texto_previo(archivo_entrada, archivo_salida)  # Eliminamos texto previo al patrón en el archivo de entrada
    salida = separar_por_formato('ems_limpio.txt')  # Separamos el contenido del archivo limpio por el formato de fecha y hora
    FindTime = buscar_en_tupla(salida, '14:13:59', '14:14:47')  # Buscamos en las tuplas dentro de un rango de tiempo
    depuracion(FindTime)