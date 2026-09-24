import os
import cv2
from ultralytics import YOLO
from config.settings import CONFIDENCE_THRESHOLD, TESTING_DETECTIONS_DIR, TESTING_IMAGES_DIR

# Carregar o modelo
model = YOLO('weights/best.pt')

# Caminho para as imagens capturadas
input_path = TESTING_IMAGES_DIR
output_path = TESTING_DETECTIONS_DIR
class_names = model.names

# Processar todas as imagens do diretório de captura
for file in os.listdir(input_path):
    if file.lower().endswith((".jpg", ".png")):
        image = cv2.imread(os.path.join(input_path, file))
        results = model.predict(source=image, conf=0.1)  # gerar previsões acima da confiança definida

        output_filename = f"prediction_{file}"
        output_filepath = os.path.join(output_path, output_filename)

        # Salvar as previsões (se necessário)
        for result in results:
            result.save(filename=output_filepath)
            print(f"Resultados Previsão para {file}:")
            boxes = result.boxes.xyxy.cpu().numpy()  # Bounding boxes (x_min, y_min, x_max, y_max)
            scores = result.boxes.conf.cpu().numpy()  # Score de confiança
            labels = result.boxes.cls.cpu().numpy()  # Índice da classe

            for i in range(len(boxes)):
                class_id = labels[i]
                class_label = class_names[class_id] if class_id in class_names else "Desconhecido"

                print(f"--- Objeto {i+1} ---")
                print(f"Class: {class_label} (ID: {class_id})")
                print(f"Coordenadas Bounding Box: {boxes[i]}")
                print(f"Confiança: {scores[i]:.4f}")
                print("-------------------")
