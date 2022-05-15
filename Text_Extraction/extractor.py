import json
import pytesseract
import cv2
import numpy as np
from PIL import Image
import ftfy
from Text_Extraction.pan_read import extract_pan_info
from Text_Extraction.aadhar_read import extract_aadhar_info


class Extractor:
    def __init__(self, image):
        self.image_file = image
        if self is None:
            return 0

    def extract_text(self):
        '''
        Function to extract text from the Image of PAN/Aadhar.
        '''
        try:
            # pytesseract.pytesseract.tesseract_cmd = 'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'
            pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
            # img = cv2.imread(self.image_file)
            img = cv2.resize(self.image_file, None, fx=2, fy=2)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # checking if image is too blury or not
            blurry_val = cv2.Laplacian(img, cv2.CV_64F).var()
            # if blurry_val < 50 --> image is too blurry
            if(blurry_val < 50):
                return "Image too Blurry."

            # now extracting the text from the image
            text = pytesseract.image_to_string(img)
            # fixing the text using ftfy
            text = ftfy.fix_text(text)
            text = ftfy.fix_encoding(text)

            if "income" in text.lower() or "tax" in text.lower() or "department" in text.lower():
                data = extract_pan_info(text)
            else:
                data = extract_aadhar_info(text)
            return data
        except Exception as e:
            return str(e)
