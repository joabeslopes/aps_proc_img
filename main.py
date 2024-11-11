import os
import sys

sys.path.insert(0, os.path.dirname(__file__)+'/class')

import aps_db as db
import aps_reader as reader

cascade_path = 'haarcascades/haarcascade_russian_plate_number.xml'

image_path = 'data/placa_3.png'

tesseract_path = r'/usr/bin/tesseract' # Linux
#tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Windows

detector = reader.PlacaDetector(image_path, cascade_path, tesseract_path)

detector.executar()