import pandas as pd
from preprocessing_service import Preprocesamiento
import json
import pprint
from model_word2vec_service import ModelWord2Vec

df = pd.read_csv("../DATASET_ENTRENAMIENTO.csv", encoding='latin-1')
comments = list(df["text"])
classes =  list(df["class"])


# df_prueba_chelsea = df_prueba_chelsea.append({'Nombre': 'Vaughn', 'Numero de camiseta':'33'}, ignore_index=True)
comment_0 = comments[0]
preprocesamiento = Preprocesamiento()

w2v = ModelWord2Vec()
df_cve = pd.read_csv('../coseno.csv')
columns = list(df_cve.columns)[2:]

# Lectura beck
beck_data_preprocessing = {}
try:
    if open('./JSON/items_preprocessing.json', 'r'):
        beck_data_preprocessing = json.loads(
            open('./JSON/items_preprocessing.json', 'r', encoding='utf-8').read())
except Exception as e:
    print(f'Error: {e}')

class_comment = 0
for comment in comments:
  try:
    print(f'Comentario: {class_comment + 1}/{len(comments)}')
    new_comment = {}
    contador = 0
    new_comment["Comentario"] = comment
    comment_preprocesado = preprocesamiento.preprocesamiento_con_ortografia(
        comment)
    new_comment["Comentario Preprocesado"] = comment_preprocesado
    w2v.add_corpus(comment_preprocesado)
    for item in beck_data_preprocessing.keys():
      for result in beck_data_preprocessing[item].keys():
        new_comment[columns[contador]] = w2v.get_cosine_similarity(comment_preprocesado, beck_data_preprocessing[item][result]["data"])
        contador += 1      

    # Add to dataframe
    new_comment["Clase"] =  classes[class_comment]
    df_cve = df_cve.append(new_comment, ignore_index=True)
    class_comment += 1
  except Exception as e: 
    print(f'Error en el comentario {class_comment} omitiendo...')
    print(e)
    class_comment += 1
    continue

df_cve.to_csv('test.csv', index=False, encoding="utf-8")