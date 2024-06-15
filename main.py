from PIL import ImageGrab
from helper import HELP as helper
from pywinauto import Desktop, Application
from WindowMgr import WindowMgr
from time import sleep
from ahk import AHK
import win32gui
import re
import cv2 as cv
import win32api
import win32con
import json
import numpy as np


# 730, 374 /// 1111, 379
# 730, 522 /// 1111, 522
# item height: 32
# margin: 5
# 660, 695 searchBox
w = WindowMgr()

w.find_window(class_name=None, window_name="Roblox")
w.set_foreground()

sleep(0.3)

ahk = AHK(executable_path="AutoHotkey64.exe")
ahk.set_send_mode("Event")
ahk.mouse_move(x=660, y=695, speed=3)

sleep(0.3)

open("recognized.txt", "w").close()

file = open("items.json", "r")
jsonOutput = file.read()
items = json.loads(jsonOutput)
items = items["items"]
itemsInInventory = [[], []]
for item in items[:5]:

    ahk.mouse_move(x=660, y=695, speed=3)
    sleep(0.3)
    ahk.click(3, "Left")
    sleep(0.3)
    ahk.send(item)
    sleep(0.4)

    screenshot = helper.getScreenCV()  # get the screen

    # region getting rows

    rows = []

    rows.append(
        helper.cropImage(screenshot, topLeft=(732, 379), bottomRight=(1111, 411))
    )  # crop the firstRow
    rows.append(
        helper.cropImage(screenshot, topLeft=(732, 416), bottomRight=(1111, 448))
    )  # crop the secondRow
    rows.append(
        helper.cropImage(screenshot, topLeft=(732, 453), bottomRight=(1111, 485))
    )  # crop the thirdRow
    rows.append(
        helper.cropImage(screenshot, topLeft=(732, 490), bottomRight=(1111, 522))
    )  # crop the fourthRow

    # endregion

    for i in range(4):
        (imgName, imgAmount) = helper.getItemParts(rows[i])
        itemsInInventory.append(
            [
                helper.readText(img=imgName, readMode="Text"),
                helper.readText(img=imgAmount, readMode="Number"),
            ]
        )

itemsInInventory = list(filter(None, itemsInInventory))  # remove empty entries

# tupledArray = [tuple(row) for row in itemsInInventory]  # remove duplicates
# inventory = np.unique(tupledArray)  # https://stackoverflow.com/a/31097302/21149029

file = open("recognized.txt", "a")
file.write(str(itemsInInventory))
file.close()


cv.waitKey(0)
