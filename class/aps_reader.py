import cv2
import pytesseract

class PlacaDetector:
    def __init__(self, video_path, cascade_path, tesseract_path):
        """
        Inicializa o detector de placas e configurações necessárias.
        :param video_path: Caminho para o arquivo de vídeo.
        :param cascade_path: Caminho para o classificador Haar Cascade.
        :param db_path: Caminho para o banco de dados SQLite.
        :param tesseract_path: Caminho para o executável do Tesseract.
        """
        self.video_path = video_path
        self.cascade_path = cascade_path
        self.tesseract_path = tesseract_path
        self.placa_cascade = cv2.CascadeClassifier(cascade_path)
        self.array_placas = []
        # Configuração do Tesseract
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def processar_frame(self, frame):
        """Processa um quadro do vídeo, detectando placas e usando OCR."""
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        placas = self.placa_cascade.detectMultiScale(cinza, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in placas:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_placa = frame[y:y + h, x:x + w]
            texto_placa = pytesseract.image_to_string(roi_placa, config='--psm 8')  # Modo 8: trata a imagem como uma única palavra
            texto_placa = texto_placa.strip().replace(" ", "")  # Limpar espaços em branco e caracteres indesejados
            
            if texto_placa:
                self.array_placas.append(texto_placa)
        return frame

    def executar(self):
        """Exibe o vídeo e realiza a detecção de placas."""
        cap = cv2.VideoCapture(self.video_path)

        # Verificar se o vídeo foi aberto corretamente
        if not cap.isOpened():
            print("Erro ao abrir o arquivo de vídeo")
            exit()
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

        # Definir FPS para processar apenas alguns quadros por segundo
        fps = 10  # Ajuste conforme necessário
        frame_counter = 0
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frame_counter += 1
            if frame_counter % fps != 0:
                continue

            frame_com_placas = self.processar_frame(frame)
            cv2.imshow('Detecção de Placas', frame_com_placas)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()