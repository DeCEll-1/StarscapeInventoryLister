# 730, 374 /// 1111, 379
# 730, 522 /// 1111, 522
# item height: 32
# margin: 5
w = WindowMgr()

w.find_window(class_name=None, window_name="Roblox")

w.set_foreground()

sleep(0.05)

screenshot = helper.getScreenCV()  # get the screen

# region rowChecks

firstRow = helper.cropImage(
    screenshot, topLeft=(732, 379), bottomRight=(1111, 411)
)  # crop the firstRow
secondRow = helper.cropImage(
    screenshot, topLeft=(732, 416), bottomRight=(1111, 448)
)  # crop the secondRow
thirdRow = helper.cropImage(
    screenshot, topLeft=(732, 453), bottomRight=(1111, 485)
)  # crop the thirdRow
fourthRow = helper.cropImage(
    screenshot, topLeft=(732, 490), bottomRight=(1111, 522)
)  # crop the fourthRow

# endregion

open("recognized.txt", "w").close()

# region firstRow

firstRowTextCrop = helper.cropImage(
    firstRow, topLeft=(34, 4), bottomRight=(378, 16)
)  # first row text

firstRowAmountCrop = helper.cropImage(
    firstRow, topLeft=(363, 19), bottomRight=(378, 31)
)  # first row amount

helper.readText(firstRowTextCrop)
helper.readText(firstRowAmountCrop)

# endregion

# region secondRow

secondRowTextCrop = helper.cropImage(
    secondRow, topLeft=(34, 4), bottomRight=(378, 16)
)  # second row text

secondRowAmount = helper.cropImage(
    secondRow, topLeft=(363, 19), bottomRight=(378, 31)
)  # second row amount

helper.readText(secondRowTextCrop)
helper.readText(secondRowAmount)

# endregion

cv.imshow("firstRow", firstRow)
cv.imshow("firstRowTextCrop", firstRowTextCrop)

cv.waitKey(0)
