import os
import time
import mss
import cv2
import numpy as np
import pyautogui
from ultralytics import YOLO
import tkinter as tk
from core.screen import capture_bluestacks_screen, get_bluestacks_rect
from config.settings import *

# YOLO model
model = YOLO("weights/best.pt")
screen_width, screen_height = pyautogui.size()

# Criar janela overlay transparente com tkinter
def create_overlay():
    left, top, right, bottom = get_bluestacks_rect()
    width, height = right - left, bottom - top

    root = tk.Tk()
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.geometry(f"{width}x{height}+{left}+{top}")
    root.wm_attributes("-transparentcolor", "black")
    root.configure(bg="black")

    canvas = tk.Canvas(root, width=width, height=height, bg="black", highlightthickness=0)
    canvas.pack()
    return root, canvas

# Atualizar texto e círculos no overlay
def update_overlay(canvas, text, detections_info):
    canvas.delete("text")
    canvas.delete("circle")
    canvas.delete("label")

    # Texto com contagens no canto superior esquerdo
    canvas.create_text(OVERLAY_FONT_PADDING_X, OVERLAY_FONT_PADDING_Y, text=text, anchor=OVERLAY_FONT_ANCHOR, fill=OVERLAY_FONT_COLOR, font=(FONT_TYPE, OVERLAY_FONT_SIZE), tags="text")

    for det in detections_info:
        x1, y1, x2, y2, class_name = det
        canvas.create_oval(x1, y1, x2, y2, outline=OUTLINE_COLOR, width=OUTLINE_WIDTH, tags="circle")
        canvas.create_text(x1, y1 - 12, text=class_name, fill=DETECTION_FONT_COLOR, font=(FONT_TYPE, DETECTION_FONT_SIZE), anchor=DETECTION_FONT_ANCHOR, tags="label")

def main():

    # Iniciar overlay
    root, canvas = create_overlay()

    while True:
        img, timestamp, img_width, img_height = capture_bluestacks_screen()
        results = model.predict(source=img, save=False, conf=CONFIDENCE_THRESHOLD)[0]

        if not results.boxes:
            update_overlay(canvas, "Nada detectado.", [])
            root.update()
            time.sleep(2)
            continue

        boxes = results.boxes.xyxy.cpu().numpy()
        classes = results.boxes.cls.cpu().numpy()
        confidences = results.boxes.conf.cpu().numpy()

        class_counts = {name: 0 for name in DEFENSE_CLASSES}
        detections_info = []

        for xyxy, cls_idx, conf in zip(boxes, classes, confidences):
            class_name = model.names[int(cls_idx)]
            if class_name in DEFENSE_CLASSES:
                class_counts[class_name] += 1
                x1, y1, x2, y2 = xyxy
                # Redimensionar coordenadas para o overlay
                detections_info.append((x1, y1, x2, y2, class_name))

        overlay_text = " | ".join([f"{name}: {count}" for name, count in class_counts.items()])
        update_overlay(canvas, overlay_text, detections_info)

        root.update()
        time.sleep(2)