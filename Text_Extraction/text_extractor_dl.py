from PIL import Image
import pytesseract
import cv2


pytesseract.pytesseract.tesseract_cmd = 'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class TextExtractor:
    def __init__(self, image):
        self.image_file = image
        if self is None:
            return 0

    def extract_text(self):
        '''
        Function to extract text from the image.
        '''
        try:
            # pytesseract.pytesseract.tesseract_cmd = 'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'
            pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
            # image = cv2.imread(self.image_file)
            image = cv2.cvtColor(self.image_file, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image, None, fx=2, fy=2)
            # getting the text
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            return str(e)
