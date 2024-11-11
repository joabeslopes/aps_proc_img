import cv2
import pytesseract

class PlacaDetector:
    def __init__(self, image_path, cascade_path, tesseract_path):
        """
        Inicializa o detector de placas e configurações necessárias.
        :param image_path: Caminho para a imagem.
        :param cascade_path: Caminho para o classificador Haar Cascade.
        :param tesseract_path: Caminho para o executável do Tesseract.
        """
        self.image_path = image_path
        self.cascade_path = cascade_path
        self.tesseract_path = tesseract_path
        self.placa_cascade = cv2.CascadeClassifier(cascade_path)
        self.array_placas = []
        # Configuração do Tesseract
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def processar_imagem(self, img):
        """Processa a imagem, detectando placas e usando OCR."""
        cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        placas = self.placa_cascade.detectMultiScale(cinza, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in placas:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_placa = img[y:y + h, x:x + w]
            texto_placa = pytesseract.image_to_string(roi_placa, config='--psm 8')  # Modo 8: trata a imagem como uma única palavra
            texto_placa = texto_placa.strip().replace(" ", "")  # Limpar espaços em branco e caracteres indesejados
            
            if texto_placa:
                self.array_placas.append(texto_placa)
                print(f"Placa detectada: {texto_placa}")
        return img

    def executar(self):
        """Carrega a imagem e realiza a detecção de placas."""
        # Carregar a imagem
        img = cv2.imread(self.image_path)

        if img is None:
            print("Erro ao carregar a imagem")
            return
        
        img_com_placas = self.processar_imagem(img)
        
        # Exibir a imagem com as placas detectadas
        cv2.imshow('Detecção de Placas', img_com_placas)

        # Aguardar até que o usuário feche a janela
        cv2.waitKey(0)
        cv2.destroyAllWindows()