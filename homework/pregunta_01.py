# pylint: disable=import-outside-toplevel

import pandas as pd

def pregunta_01():
  '''
  Construya y retorne un dataframe de Pandas a partir del archivo
  'files/input/clusters_report.txt'. Los requierimientos son los siguientes:
  - El dataframe tiene la misma estructura que el archivo original.
  - Los nombres de las columnas deben ser en minusculas, reemplazando los
    espacios por guiones bajos.
  - Las palabras clave deben estar separadas por coma y con un solo
    espacio entre palabra y palabra.
  '''
  with open('files/input/clusters_report.txt') as file: # Importar el archivo
    lines = file.read()

  lines = lines.replace('.', '')
  lines = lines.split('\n')                             # División de lines por \n (lines es un string que contiene todo el archivo)

  columns1 = lines[0].strip().replace(' ', '_')                   # Primera parte de las columnas
  columns2 = lines[1].ljust(len(columns1), '_').replace(' ', '_') # Segunda parte da las columnas

  mayusculas = []           # Proceso de extracción de columnas
  for letter in columns1:
    if letter.isupper():
      mayusculas.append(letter)
  for letter in list(set(mayusculas)):
    columns1 = columns1.replace(letter, f'¿{letter}')
  columns1 = columns1.split('¿')
  col = []
  for word in columns1:
    if word == '':
      continue
    col.append(word)
  start = 0
  columns = []
  for i in range(len(col)):
    end = start + len(col[i])
    columns.append(col[i] + columns2[start:end])
    start = end
  columns = list(map(lambda x: '_'.join([parte for parte in x.strip('_').lower().split('_') if parte != '']), columns))
  # Fin del proceso de extracción del nombre de columnas (muy arcaico y sin explicación - Nada mantenible)
  
  data = {key: [] for key in columns}     # Diccionario para la creación del DataFrame
  cont = -1                               # Contador para identificar qué linea pertenece a qué cluster
  for line in lines[4:]:                  # Lectura de las líneas que son contenido del DF en el archivo
    split_line = line.split()             # split() de cada línea
    if len(line.split()) == 0:            # Comprobar que la línea no sea vacía
      continue                            # en caso de ser vacía, se salta a la siguiente
    if split_line[0].isdigit():           # Comprobar si la línea comienza con un dígito,
      cont += 1                           # en caso de serlo, es porque es el comienzo de un cluster
      data[columns[0]].append(int(split_line[0]))  # Asignar los valores a cada columna
      data[columns[1]].append(int(split_line[1]))
      data[columns[2]].append(float(split_line[2].replace(',','.')))
      data[columns[3]].append('')
      clave = ' '.join(split_line[4:])    # En clave se almacena el valor de la columna 'principales_palabras_clave' de cada línea
    else:
      clave = ' ' + ' '.join(split_line)
    data[columns[3]][cont] += clave       # Se añade el valor de clave al cluster correspondiente
  return pd.DataFrame(data = data)        # Se retorna el DF con los datos extraídos