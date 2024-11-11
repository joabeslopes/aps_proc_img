import os
import sys

sys.path.insert(0, os.path.dirname(__file__)+'/class')

import aps_db as db
import aps_reader as reader

cascade_path = 'haarcascades/haarcascade_russian_plate_number.xml'

image_path = 'data/foto4.jpeg'

detector = reader.PlacaDetector(image_path, cascade_path)

detector.executar()