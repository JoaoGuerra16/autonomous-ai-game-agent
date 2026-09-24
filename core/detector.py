from ultralytics import YOLO
from config.settings import MODEL_PATH
from config.settings import CONFIDENCE_THRESHOLD

model = YOLO(MODEL_PATH)

def predict(img, conf=CONFIDENCE_THRESHOLD):
    return model.predict(source=img, conf=conf)
