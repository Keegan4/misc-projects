import pyautogui as pt
from time import sleep
import pyperclip
import random

sleep(1)

pos1 = pt.locateOnScreen("img_1.png", confidence = .6)
x = pos1[0]
y = pos1[1]

#message
def get_msg():
    global x, y
    position = pt.locateOnScreen("img_1.png", confidence = .6)
    x = position[0]
    y = position[1]
    pt.moveTo(x, y, duration=.05)
    pt.moveTo(x + 31, y - 77, duration=.5)
    pt.tripleClick()
    pt.rightClick()
    pt.moveRel(12, -160)
    pt.click()
    new_message = pyperclip.paste()
    pt.click()
    print(new_message)
    return new_message


def post(message):
    global x, y
    position = pt.locateOnScreen("img_1.png", confidence=.6)
    x = position[0]
    y = position[1]
    pt.moveTo(x + 200, y + 20, duration = 0.05)
    pt.tripleClick()
    pt.typewrite(message, interval=0.1)

post(get_msg())