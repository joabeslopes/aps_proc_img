import os
import sys

sys.path.insert(0, os.path.dirname(__file__)+'/class')

import aps_db as database
import aps_reader as reader

cascade_path = 'haarcascades/haarcascade_russian_plate_number.xml'

image_path = 'data/foto4.jpeg'

db = database.DbManager()

detector = reader.PlacaDetector(image_path, cascade_path)
detector.executar()

result = None

for possivel_placa in detector.array_placas:
    result = db.busca_no_banco(possivel_placa)
    if not result == None:
        break

if not result == None:
    placa_encontrada = result[0][1] # linha 0 coluna placa
    print(f"Sucesso: encontrou a placa {placa_encontrada} no banco")
else:
    print(f"Erro: nao encontrou a placa")

db.encerra_conexao()