import pyautogui as pt

from PIL import Image
def gimmie_color(filename):
    img = Image.open(filename)
    img = img.convert('RGBA')
    data = img.getdata()
    return data

def detect_color(rgb, filename):
    img = Image.open(filename)
    img = img.convert('RGBA')
    data = img.getdata()

    for item in data:
        if item[0] == rgb[0] and item[1] == rgb[1] and item[2] == rgb[2]:
            return True
    return False


while True:
    im = pt.screenshot(region=(277, 477, 278, 480))
    im.save("green.png")
    if detect_color((75, 219, 106), "green.png"):
        pt.click()


