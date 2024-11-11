import cv2
import easyocr

class PlacaDetector:
    def __init__(self, image_path, cascade_path):
        """
        Inicializa o detector de placas e configurações necessárias.
        :param image_path: Caminho para a imagem.
        :param cascade_path: Caminho para o classificador Haar Cascade.
        """
        self.image_path = image_path
        self.cascade_path = cascade_path
        self.placa_cascade = cv2.CascadeClassifier(cascade_path)
        self.array_placas = []
        self.ocr = easyocr.Reader(['pt'])

    def processar_imagem(self, img):
        """Processa a imagem, detectando placas e usando OCR."""
        cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        placas = self.placa_cascade.detectMultiScale(cinza, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        roi_placa = None
        for (x, y, w, h) in placas:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_placa = img[y:y + h, x:x + w]
        if roi_placa.any():
            return roi_placa
        else:
            return img

    def executar(self):
        """Carrega a imagem e realiza a detecção de placas."""
        # Carregar a imagem
        img = cv2.imread(self.image_path)

        if img is None:
            print("Erro ao carregar a imagem")
            return
        
        img_placa = self.processar_imagem(img)
        result = self.ocr.readtext(img_placa)

        for n in result:
            self.array_placas.append(n[1])
            print(f"possivel placa lida: {n[1]}")

        # Exibir a imagem com as placas detectadas
        cv2.imshow('Deteccao de Placas', img_placa)

        # Aguardar até que o usuário feche a janela
        cv2.waitKey(0)
        cv2.destroyAllWindows()