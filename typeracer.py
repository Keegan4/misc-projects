import pyautogui as pt
from time import sleep
import pyscreenshot
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image

pos1 = pt.locateOnScreen("start.PNG", confidence=.8)
x1 = pos1[0] + 30
y1 = pos1[1] + 70
pt.moveTo(x1, y1)
pos2 = pt.locateOnScreen("ENd.PNG", confidence=0.8)
x2 = pos2[0] + 100
y2 = pos2[1]

pt.moveTo(x2, y2)
pt.moveTo(x2 - 80, y2 + 73)
pt.click()
img = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
img.save("img.png")
img = Image.open("img.png")
text = pytesseract.image_to_string(img)
text = text.replace("\n", " ").replace("|", "I").replace("{", "")
print(text)
pt.typewrite(text, interval=0.001)
