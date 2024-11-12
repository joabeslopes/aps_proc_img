import os
import sys

sys.path.insert(0, os.path.dirname(__file__)+'/class')

import aps_db as database
import aps_reader as reader

cascade_path = 'haarcascades/haarcascade_russian_plate_number.xml'

image_path = 'data/foto1.jpeg'

detector = reader.PlacaDetector(image_path, cascade_path)

db = database.DbManager()

detector.executar()

result = None

for possivel_placa in detector.array_placas:
    placa = db.tratamento_string(possivel_placa)
    result = db.busca_no_banco(placa)
    if not result == None:
        break

if not result == None:
    print(f"Sucesso: encontrou a placa")
else:
    print(f"Erro: nao encontrou a placa")