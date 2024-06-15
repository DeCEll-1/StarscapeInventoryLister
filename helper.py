from PIL import ImageGrab
from pywinauto import Desktop, Application
from WindowMgr import WindowMgr
import win32gui
import re
import cv2 as cv
import numpy as np
import pytesseract


class HELP:

    def PIL2CV(pil_image):
        pil_image = pil_image.convert("RGB")
        open_cv_image = np.array(pil_image)
        # Convert RGB to BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        return open_cv_image

    def getScreenCV():
        return HELP.PIL2CV(
            ImageGrab.grab()
        )  # turn it to OpenCV format cuz i cant do crab with pil

    def cropImage(image, topLeft, bottomRight):
        (tlx, tly) = topLeft
        (brx, bry) = bottomRight

        return image[tly:bry, tlx:brx]

    def getItemParts(item):

        itemName = HELP.cropImage(
            item, topLeft=(34, 4), bottomRight=(378, 16)
        )  # first row text

        itemAmount = HELP.cropImage(
            item, topLeft=(365, 19), bottomRight=(378, 31)
        )  # first row amount

        return (itemName, itemAmount)

    def readText(img, readMode):
        """readMode = Text || Number"""
        # Mention the installed location of Tesseract-OCR in your system
        pytesseract.pytesseract.tesseract_cmd = (
            "c:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        )

        shapeSizeMult = 4 if readMode == "Text" else 2

        # Preprocessing the image starts

        # Convert the image to gray scale
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Performing OTSU threshold
        _, thresh = cv.threshold(gray, 10, 60, cv.THRESH_OTSU | cv.THRESH_BINARY_INV)

        (imgY, imgX) = thresh.shape[:2]

        imgNewShape = (imgX * shapeSizeMult, imgY * shapeSizeMult)

        thresh = cv.resize(thresh, imgNewShape, interpolation=cv.INTER_AREA)

        # Finding contours
        contours, hierarchy = cv.findContours(
            thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE
        )

        # Creating a copy of image
        (imgY, imgX) = img.shape[:2]
        imgNewShape = (imgX * shapeSizeMult, imgY * shapeSizeMult)

        im2 = cv.resize(img, imgNewShape, interpolation=cv.INTER_AREA).copy()

        # Looping through the identified contours
        # Then rectangular part is cropped and passed on
        # to pytesseract for extracting text from it
        # Extracted text is then written into the text file
        for cnt in contours:
            x, y, w, h = cv.boundingRect(cnt)

            # Drawing a rectangle on copied image
            rect = cv.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Cropping the text block for giving input to OCR
            cropped = im2[y : y + h, x : x + w]

            # Apply OCR on the cropped image
            text = ""
            if readMode == "Text":
                text = pytesseract.image_to_string(
                    cropped,
                    config="--psm 3 -c tessedit_char_whitelist=qwertyuopasdfghjklizxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM",  # use this for texts
                )  # https://stackoverflow.com/a/44632770/21149029
            else:
                text = pytesseract.image_to_string(
                    cropped,
                    config="--psm 7 -c tessedit_char_whitelist=0123456789",  # use this for texts
                )  # https://stackoverflow.com/a/44632770/21149029

            cv.imshow("cropped", cropped)

            text = text.replace("\\n", "").replace("\n", "")

            return text
