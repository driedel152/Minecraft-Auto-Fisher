import win32gui
import win32ui
import win32api
import win32con
from ctypes import windll
from PIL import Image
from time import sleep

def findHwnd(h, lParam):
    title = win32gui.GetWindowText(h)
    if 'Minecraft' in title and 'Minecraft-Auto-Fisher' not in title:
        global hwnd
        hwnd = h

def click(x, y):
    lParam = win32api.MAKELONG(x, y)
    win32gui.PostMessage(hwnd, win32con.WM_RBUTTONDOWN,
                             0, lParam)
    win32gui.PostMessage(hwnd, win32con.WM_RBUTTONUP,
                            0, lParam)
    
def testForBlack(image):
    for x in range(0, image.width):
        for y in range(0, image.width):
            if image.getpixel((x,y)) == (13, 13, 13) or image.getpixel((x,y)) == (0, 0, 0): # Color of fishing line
                return True
    return False

win32gui.EnumWindows(findHwnd, None)
print(win32gui.GetWindowText(hwnd))

left, top, right, bot = win32gui.GetClientRect(hwnd)
w = right - left
h = bot - top

hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()

saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

saveDC.SelectObject(saveBitMap)

while (True):
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    if result != 1:
        print("Error code " + result)
        break

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    image = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    cropWidth = 30
    cropped = image.crop((image.width/2-cropWidth/2, image.height/2, image.width/2+cropWidth/2, image.height/2+cropWidth))
    
    cropped.save("test.png")

    if not testForBlack(cropped):
        print("Fish!")
        click(0,0)
        sleep(1)
        click(0,0)
        sleep(1)

    sleep(0.25)

win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hwnd, hwndDC)