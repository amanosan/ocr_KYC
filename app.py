from PIL import Image
from fastapi import FastAPI
import urllib.request
import requests
import cv2
import numpy as np
from io import BytesIO
import pytesseract
import matplotlib.pyplot as plt
from Text_Extraction.text_extractor_dl import TextExtractor
from Text_Extraction.validate_dl import Dl_Validator
from Text_Extraction.extractor import Extractor

app = FastAPI(title="Major Project")
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'


@app.get('/index')
async def hello_world():
    return "hello world"


@app.post('/drivers_license/')
def driver_license_info(image_url: str = ""):
    if image_url == "":
        return {
            'message': 'No URL provided.'
        }

    image_extension = image_url.split('.')[-1]
    if image_extension not in ['png', 'jpg', 'jpeg']:
        return {
            'message': 'File Formats supported include - png, jpg, jpeg'
        }

    image_response = requests.get(image_url)
    img = Image.open(BytesIO(image_response.content))
    img = np.array(img)
    # await urllib.request.urlretrieve(image_url, 'image.' + image_extension)
    # image_file = 'image.' + image_extension
    text_extract = TextExtractor(img)
    image_text = text_extract.extract_text()
    dlv = Dl_Validator(image_text)
    parameters_dict = dlv.is_valid()
    print(dlv.text)
    return {
        'params_extracted': parameters_dict
    }


@ app.post('/pan_aadhar')
async def pan_aadhar_info(image_url: str = ""):
    if image_url == "":
        return {
            'message': 'No URL provided.'
        }
    image_extension = image_url.split('.')[-1]
    if image_extension not in ['png', 'jpg', 'jpeg']:
        return {
            'message': 'File Formats supported include - png, jpg, jpeg'
        }
    # await urllib.request.urlretrieve(image_url, 'image.' + image_extension)
    # image_file = 'image.' + image_extension
    image_response = requests.get(image_url)
    img = Image.open(BytesIO(image_response.content))
    img = np.array(img)
    text_extract = Extractor(img)
    pytesseract.pytesseract.tesseract_cmd = 'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    parameters_dict = text_extract.extract_text()
    return {
        'params_extracted': parameters_dict
    }
