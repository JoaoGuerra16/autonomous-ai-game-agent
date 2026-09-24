import cv2

# Função para melhorar o contraste e o pré-processamento para OCR
def preprocess_for_ocr(image):
    # Converter para tons de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Binarização usando o método de Otsu
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh
