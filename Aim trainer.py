import pyautogui as pt
from time import sleep
counter = 0
sleep(3)
pos = pt.locateOnScreen("cookie.png", confidence = 0.6)
x = pos[0]
y = pos[1]
pt.PAUSE = 0.0001
pt.moveTo(x + 60, y + 80)
while True:
    counter += 1
    pt.click()
    if counter % 1000:
        break


