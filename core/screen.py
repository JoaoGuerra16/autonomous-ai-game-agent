import mss, cv2, time, os
import numpy as np
from config.settings import CAPTURED_DIR
import win32gui

def capture_screen():
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        path = os.path.join(CAPTURED_DIR, f"capture_{timestamp}.jpg")
        cv2.imwrite(path, img)
        return img, timestamp, img.shape[1], img.shape[0]

# Posição da janela BlueStacks
def get_bluestacks_rect(title="BlueStacks App Player"):
    hwnd = win32gui.FindWindow(None, title)
    if not hwnd:
        raise Exception("Janela do BlueStacks não encontrada")
    return win32gui.GetWindowRect(hwnd)  # (left, top, right, bottom)

# Captura de Ecrã
def capture_bluestacks_screen():
    with mss.mss() as sct:
        left, top, right, bottom = get_bluestacks_rect()
        monitor = {"top": top, "left": left, "width": right - left, "height": bottom - top}
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        img_height, img_width, _ = img.shape
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        return img, timestamp, img_width, img_height