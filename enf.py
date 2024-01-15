import re
from datetime import datetime, timedelta


def read_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def write_lines(file_path, lines):
    with open(file_path, 'w') as file:
        file.writelines(lines)

def eliminar_texto_previo(archivo_entrada, archivo_salida):
    lines = read_lines(archivo_entrada)
    encontrado = False
    nuevas_lineas = []

    for linea in lines:
        if re.search(r'\d{2}-\d{2}-\d{2};\d{2}:\d{2}:\d{2}.\d{3}', linea):
            encontrado = True
            nuevas_lineas.append(linea)
        elif encontrado:
            nuevas_lineas.append(linea)

    write_lines(archivo_salida, nuevas_lineas)

def depurar_archivo(archivo_entrada, archivo_salida):
    with open(archivo_entrada, 'r') as archivo_entrada:
        contenido = archivo_entrada.read()

    contenido_depurado = re.sub(r'8\*.*?7\* r', '', contenido, flags=re.DOTALL)

    with open(archivo_salida, 'w') as archivo_salida:
        archivo_salida.write(contenido_depurado)

def separar_por_formato(archivo):
    lines = read_lines(archivo)
    contenido = ''.join(lines)  # Combina las líneas en una cadena
    patrones = re.findall(r'\d{2}-\d{2}-\d{2};\d{2}:\d{2}:\d{2}\.\d+', contenido)
    datos_separados = re.split(r'\d{2}-\d{2}-\d{2};\d{2}:\d{2}:\d{2}\.\d+', contenido)
    datos_separados = [dato.strip() for dato in datos_separados if dato.strip()]
    lista_final = list(zip(patrones, datos_separados))
    return lista_final


def buscar_en_tupla(lista_tuplas, hora_inicio, milisegundos_futuros):
    hora_inicio = hora_inicio + ".000"
    formato_hora = '%d-%m-%y;%H:%M:%S.%f'
    hora_inicio_dt = datetime.strptime(hora_inicio, formato_hora)
    print("Hora de inicio ajustada:", hora_inicio_dt)
    
    tupla_mas_cercana = min(lista_tuplas, key=lambda tupla: abs(datetime.strptime(tupla[0], formato_hora) - hora_inicio_dt))
    print("Hora más cercana en la lista:", tupla_mas_cercana[0])

    hora_inicio_nueva = datetime.strptime(tupla_mas_cercana[0], formato_hora) + timedelta(milliseconds=milisegundos_futuros)
    print("Hora de inicio después de ajuste:", hora_inicio_nueva)

    resultados = [tupla for tupla in lista_tuplas if hora_inicio_nueva <= datetime.strptime(tupla[0], formato_hora) <= hora_inicio_nueva + timedelta(milliseconds=1)]

    if not resultados:
        print(f"No se encontraron datos desde un segundo después de la hora más cercana: {hora_inicio_nueva.strftime(formato_hora)}")

    return resultados



def depuracion(find_time):
    if not find_time:
        print("No hay datos que depurar")
    else:
        print("Resultados encontrados.")
        for i, tupla in enumerate(find_time):
            find_time[i] = {'Fecha y Hora': tupla[0], 'Otro Campo': tupla[1]}
            if "*" in find_time[i]['Otro Campo']:
                data_clear = re.split(r'\d\*', find_time[i]['Otro Campo'])
                find_time[i]['Otro Campo'] = data_clear[0]
            print(str(find_time[i]['Fecha y Hora']))

    return find_time

if __name__ == "__main__":
    archivo_entrada = "EMS CLASICO.txt"
    archivo_salida = "ems_limpio1.txt"
    depurar_archivo(archivo_entrada, archivo_salida)
    eliminar_texto_previo(archivo_entrada, archivo_salida)
    salida = separar_por_formato('ems_limpio1.txt')
    find_time = buscar_en_tupla(salida, '24-01-04;09:15:11', 1000)  # Ampliar el rango a 1000 milisegundos (1 segundo)
                                                                    # '24-01-11;14:13:59'
    find_time = depuracion(find_time)
