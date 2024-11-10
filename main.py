import os
import sys

sys.path.insert(0, os.path.dirname(__file__)+'/class')

import aps_db as db
import aps_reader as reader

cascade_path = 'haarcascades/haarcascade_russian_plate_number.xml'

video_path = 'video/video_teste.mp4'

tesseract_path = '/usr/bin/tesseract'

detector = reader.PlacaDetector(video_path, cascade_path, tesseract_path)

detector.executar()

for placa in detector.array_placas:
    print(f"placa encontrada: {placa}")