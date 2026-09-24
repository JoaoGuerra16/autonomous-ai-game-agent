import pyautogui

screen_width, screen_height = pyautogui.size()

def click_on(center_x, center_y, img_width, img_height):
    scaled_x = int((center_x / img_width) * screen_width)
    scaled_y = int((center_y / img_height) * screen_height)
    pyautogui.moveTo(scaled_x, scaled_y, duration=0.3)
    pyautogui.click()
    return scaled_x, scaled_y
