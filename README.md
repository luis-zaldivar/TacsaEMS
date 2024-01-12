si queremos no usar el main el codigo que de la siguiente manera:

```python
archivo_entrada = "ems.cap"  # Nombre del archivo de entrada
archivo_salida = "ems_limpio.txt"  # Nombre del archivo de salida
depurar_archivo(archivo_entrada, archivo_salida)
eliminar_texto_previo(archivo_entrada, archivo_salida)  # Eliminamos texto previo al patrón en el archivo de entrada
salida = separar_por_formato('ems_limpio.txt')  # Separamos el contenido del archivo limpio por el formato de fecha y hora    
FindTime = buscar_en_tupla(salida, '14:13:59')  # Buscamos en las tuplas desde la hora de inicio
depuracion(FindTime)
```