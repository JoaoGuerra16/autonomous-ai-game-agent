import time, os, cv2
from core.screen import capture_screen
from core.detector import predict
from core.interaction import click_on
from config.settings import COLECTING_CLASSES, CONFIDENCE_THRESHOLD, DETECTIONS_DIR

model = predict.__globals__['model']

def main():
    while True:
        img, timestamp, img_width, img_height = capture_screen()
        results = predict(img, conf=CONFIDENCE_THRESHOLD)
        boxes = results[0].boxes

        if boxes is None:
            continue

        detections = boxes.xyxy.cpu().numpy()
        classes = boxes.cls.cpu().numpy()
        confidences = boxes.conf.cpu().numpy()

        best_by_class = {}
        for i, (xyxy, cls_idx, conf) in enumerate(zip(detections, classes, confidences)):
            name = model.names[int(cls_idx)]
            if name in COLECTING_CLASSES:
                if name not in best_by_class or conf > best_by_class[name][1]:
                    best_by_class[name] = (xyxy, conf)

        for name, (xyxy, conf) in best_by_class.items():
            x1, y1, x2, y2 = xyxy
            center_x, center_y = int((x1 + x2) / 2), int((y1 + y2) / 2)
            sx, sy = click_on(center_x, center_y, img_width, img_height)
            print(f"[{name}] confiança {conf:.2f} → clique em ({sx}, {sy})")

        # Opcional: salvar imagem com anotações
        annotated = results[0].plot()
        path = os.path.join(DETECTIONS_DIR, f"result_{timestamp}.jpg")
        cv2.imwrite(path, annotated)

        time.sleep(3)