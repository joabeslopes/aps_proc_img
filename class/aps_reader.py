import cv2
import pytesseract
import sqlite3


class PlacaDetector:
    def __init__(self, video_path, cascade_path, db_path, tesseract_path):
        """
        Inicializa o detector de placas e configurações necessárias.

        :param video_path: Caminho para o arquivo de vídeo.
        :param cascade_path: Caminho para o classificador Haar Cascade.
        :param db_path: Caminho para o banco de dados SQLite.
        :param tesseract_path: Caminho para o executável do Tesseract.
        """
        self.video_path = video_path
        self.cascade_path = cascade_path
        self.db_path = db_path
        self.tesseract_path = tesseract_path
        self.placa_cascade = cv2.CascadeClassifier(cascade_path)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # Configuração do Tesseract
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def verificar_placa_no_banco(self, placa):
        """Verifica se a placa existe no banco de dados."""
        self.cursor.execute("SELECT * FROM veiculos WHERE placa = ?", (placa,))
        resultado = self.cursor.fetchone()
        if resultado:
            print(f"Placa encontrada: {resultado}")
        else:
            print("Placa não encontrada no banco de dados.")

    def processar_frame(self, frame):
        """Processa um quadro do vídeo, detectando placas e usando OCR."""
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        placas = self.placa_cascade.detectMultiScale(cinza, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in placas:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_placa = frame[y:y + h, x:x + w]

            texto_placa = pytesseract.image_to_string(roi_placa,
                                                      config='--psm 8')  # Modo 8: trata a imagem como uma única palavra
            texto_placa = texto_placa.strip().replace(" ", "")  # Limpar espaços em branco e caracteres indesejados
            print(f"Placa detectada: {texto_placa}")

            if texto_placa:
                self.verificar_placa_no_banco(texto_placa)
        return frame

    def exibir_video(self):
        """Exibe o vídeo e realiza a detecção de placas."""
        cap = cv2.VideoCapture(self.video_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_com_placas = self.processar_frame(frame)
            cv2.imshow('Detecção de Placas', frame_com_placas)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def liberar_recurso(self):
        """Libera os recursos após o processamento."""
        self.conn.close()

    def executar(self):
        """Método principal para rodar o processo de detecção de placas."""
        self.exibir_video()
        self.liberar_recurso()


# Exemplo de como usar a classe
video_path = 'video/EVENTO CARRO.mp4'
cascade_path = 'haarcascades/haarcascade_russian_plate_number.xml'
db_path = 'banco_de_dados.db'
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

detector = PlacaDetector(video_path, cascade_path, db_path, tesseract_path)
detector.executar()
