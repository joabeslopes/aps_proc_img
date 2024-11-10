import cv2

# Caminho para o arquivo XML do Haar Cascade para placas
cascade_path = 'haarcascades/haarcascade_russian_plate_number.xml'
placa_cascade = cv2.CascadeClassifier(cascade_path)

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

    # Exibir o vídeo com as placas detectadas
    cv2.imshow('Detecção de Placas', frame)

    # Verificar se a tecla 'q' foi pressionada ou a janela foi fechada
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or cv2.getWindowProperty('Detecção de Placas', cv2.WND_PROP_VISIBLE) < 1:
        break

# Liberar o objeto de captura e fechar as janelas
cap.release()
cv2.destroyAllWindows()
