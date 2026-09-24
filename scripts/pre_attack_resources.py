import cv2
from ultralytics import YOLO
import numpy as np
import pyautogui
import time
from paddleocr import PaddleOCR
from config.settings import *
from core.process_ocr import preprocess_for_ocr

# Inicializar OCR (PaddleOCR)
ocr = PaddleOCR(use_angle_cls=False, lang='en')  

# Carregar o modelo YOLO
model = YOLO('weights/best.pt')
# Função principal
def main():
    print("Bot iniciado. Pressione Ctrl + C para parar.")

    try:
        while True:
            # Captura o ecrã
            screenshot = pyautogui.screenshot()
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Realiza a detecção com o YOLO
            resultados = model(img)
            valores = {"ValueCoin": 0, "ValueElixir": 0, "ValueElixirNegro": 0}
            botao_next = None

            for result in resultados:
                for box in result.boxes:
                    score = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]

                    # Mostrar as caixas de detecção para depuração
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Caixa vermelha

                    # Verificar se a confiança está abaixo do limite
                    if score < CONFIDENCE_THRESHOLD:
                        continue

                    if class_name in RESOURCE_CLASSES:
                        # Extrair a região de interesse (ROI)
                        roi = img[y1:y2, x1:x2]
                        roi = cv2.resize(roi, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)

                        # Pré-processamento para OCR 
                        processed_roi = preprocess_for_ocr(roi)
                        
                        # Executar PaddleOCR no ROI processado
                        ocr_result = ocr.ocr(processed_roi, cls=False)

                        # Filtrar números detectados no OCR
                        numero_detectado = "0"
                        if ocr_result and ocr_result[0]:
                            raw_text = ocr_result[0][0][1][0]
                            numero_detectado = ''.join(filter(str.isdigit, raw_text)) or "0"

                        # Exibir resultados do OCR
                        print(f"{class_name} ({score:.2f}): {numero_detectado}")

                        # Atribuir o valor detectado ao tipo de recurso
                        try:
                            valores[class_name] = int(numero_detectado)
                        except ValueError:
                            valores[class_name] = 0  # Se falhar na conversão, atribui 0

                    elif class_name == "Next":
                        # Identifica o botão "Next"
                        botao_next = (int((x1 + x2) / 2), int((y1 + y2) / 2))

            # Exibir os valores detectados
            soma_total = sum(valores.values())
            print(f"Valores detectados: {valores} | Total: {soma_total}")

            # Se o loot for abaixo do mínimo, clicar no botão "Next"
            if soma_total < MIN_LOOT and botao_next:
                print("Loot abaixo do mínimo. Pulando base...")
                print(soma_total)
                pyautogui.moveTo(botao_next[0], botao_next[1], duration=0.3)
                pyautogui.click()
            else:
                print(soma_total)
                print("Loot suficiente! Pronto para atacar ou aguardar.")

            # Aguardar antes da próxima captura
            time.sleep(SCREEN_CAPTURE_INTERVAL)

    except KeyboardInterrupt:
        print("Bot finalizado pelo utilizador.")

# Executar a função principal
if __name__ == "__main__":
    main()
