"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------

Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.


"""
import pandas as pd


def ingest_data():

    #
    # Inserte su código aquí
    #
    import re
    indice = -1

    df = pd.read_fwf('clusters_report.txt', skiprows=4, 
                    names = ['cluster', 
                            'cantidad_de_palabras_clave', 
                            'porcentaje_de_palabras_clave', 
                            'principales_palabras_clave'], 
                    widths = [9,16,16,77])


    line = '' # variable para almacenar el texto a añadir

    for index, row in df.iterrows():
        if index == 0 or not pd.isna(row['cluster']):
            indice = index # guardar el índice de la fila en donde se añadirán las demás
        else:
            # si no hay espacio antes, lo añade
            if df.iloc[index-1, 3][-1] != ' ':
                line += ' '
            # si la línea termina en . lo elimina
            if row['principales_palabras_clave'][-1] == '.':
                row['principales_palabras_clave'] = row['principales_palabras_clave'][:-1]
            line += row['principales_palabras_clave']
            df.iloc[indice, 3] += line
            line = ''
        
        df.iloc[indice, 3] = re.sub('\s{2,}', ' ', df.iloc[indice, 3]) # usando regex reemplazar los más de dos espacios por un solo espacio entre palabras

    # eliminar las filas vacías, reiniciar los índices y eliminar la columna índice resultante
    df.dropna(axis = 0, inplace = True)
    df.reset_index(inplace=True)
    df.drop(axis=1, labels='index', inplace=True)

    for index, row in df.iterrows():
        df.iloc[index, 2] = float(row['porcentaje_de_palabras_clave'][:-2].replace(',', '.'))

    return df

print(ingest_data())
