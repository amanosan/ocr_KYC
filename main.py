import pytesseract
from Text_Extraction.text_extractor_dl import TextExtractor
from Text_Extraction.validate_dl import Dl_Validator
pytesseract.pytesseract.tesseract_cmd = 'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'


if __name__ == '__main__':
    te = TextExtractor('./image_samples/dl_sample.jpg')
    image_text = te.extract_text()
    dlv = Dl_Validator(image_text)
    dlv.is_valid()
    # print(image_text)
