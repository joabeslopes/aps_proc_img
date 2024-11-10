import cv2
import pytesseract
from aps_db import BancoDeDados  # Importa a classe de banco de dados

# Caminho para o arquivo XML do Haar Cascade para placas
cascade_path = 'haarcascades/haarcascade_russian_plate_number.xml'
placa_cascade = cv2.CascadeClassifier(cascade_path)

# Configuração do Tesseract (ajuste o caminho conforme necessário)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Caminho do banco de dados
db_path = 'banco_de_dados.db'

# Inicializa a classe de banco de dados
banco = BancoDeDados(db_path)

# Abrir o vídeo com VideoCapture
cap = cv2.VideoCapture('video/EVENTO CARRO.mp4')

# Verificar se o vídeo foi aberto corretamente
if not cap.isOpened():
    print("Erro ao abrir o arquivo de vídeo")
    exit()

# Reduz a resolução do vídeo para otimizar o processamento
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

# Definir FPS para processar apenas alguns quadros por segundo
fps = 10  # Ajuste conforme necessário
frame_counter = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("Erro ao ler o quadro ou fim do vídeo.")
        break

    frame_counter += 1
    if frame_counter % fps != 0:
        continue

    # Converter o quadro para escala de cinza, necessário para Haar Cascade
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar placas no quadro
    placas = placa_cascade.detectMultiScale(cinza, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Percorrer as placas detectadas e desenhar retângulos
    for (x, y, w, h) in placas:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi = frame[y:y + h, x:x + w]

        # Usar OCR para ler o texto da placa
        texto_placa = pytesseract.image_to_string(roi, config='--psm 8')  # Modo 8: trata a imagem como uma única palavra
        texto_placa = texto_placa.strip().replace(" ", "")  # Limpar espaços em branco e caracteres indesejados
        print(f"Placa detectada: {texto_placa}")

        # Verificar no banco de dados
        if texto_placa:
            banco.verificar_placa(texto_placa)

    # Exibir o vídeo com as placas detectadas
    cv2.imshow('Detecção de Placas', frame)

    # Verificar se a tecla 'q' foi pressionada ou a janela foi fechada
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or cv2.getWindowProperty('Detecção de Placas', cv2.WND_PROP_VISIBLE) < 1:
        break

# Liberar o objeto de captura e fechar as janelas
cap.release()
cv2.destroyAllWindows()

# Fechar a conexão com o banco de dados
banco.close()
