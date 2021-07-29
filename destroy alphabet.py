import pyautogui as pt
from time import sleep
import pyscreenshot
import pytesseract
from pynput import mouse, keyboard
from PIL import Image
sleep(2)
word = ""
alpha = [chr(i) for i in range(ord("a"), ord("z") + 1)]
pt.typewrite(word.join(alpha))


