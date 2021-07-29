import pyautogui as pt
from time import sleep
import pyscreenshot
import pytesseract
from pynput import mouse, keyboard
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def on_click(x, y, button, pressed):
    if pressed:
        listbox.append((x, y))
    if not pressed:
        return False

satisfied = False
def on_press(key):
    global satisfied
    if key == keyboard.Key.esc:
        return False
    if key == keyboard.Key.insert:
        satisfied = True
        return False

listbox = []

while not satisfied:
    print("Capturing the screen, click on the top and bottom \ncorner of the image you wanna capture")
    with mouse.Listener(on_click = on_click) as listener:
        listener.join()
    with mouse.Listener(on_click = on_click) as listener:
        listener.join()
    print("Ready")
    print("Click esc to retake, Click end to write the capture down")
    with keyboard.Listener(on_press = on_press) as listener:
        listener.join()

img = pyscreenshot.grab(bbox=(listbox[0][0], listbox[0][1], listbox[1][0], listbox[1][1]))
img.save("img.png")
img = Image.open("img.png")
text = pytesseract.image_to_string(img)
text = text.replace("[", "").replace("|", "I").replace("{", "").replace("\n", " ")
print(text)
pt.typewrite(text, interval = 0.0001)





