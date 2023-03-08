import platform
import numpy as np
from PIL import Image
import pytesseract
import pandas as pd
from helpers import text_processing as tp
from models.ocr_output import OCROutput

if platform.system() == 'Windows':
    # Detect tesseract executable file
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

elif platform.system() == 'Linux' and platform.linux_distribution()[0] == 'Red Hat':
    print('Red Hat detected')
else:
    print('Operating system not recognized')



class TesseractOCR:

    def __int__(self):
        self.languages: [] = ['eng', 'ara']
        self.output_type: str = "dict"

    def __init__(self, languages: [], output_type: str):
        self.languages: [] = languages
        self.output_type: str = output_type

    def get_supported_languages():
        """

        :return: Supported languages by Tesseract
        """
        return pytesseract.get_languages()

    def apply_ocr(self, file_location: str)-> OCROutput:

        # Create OCROutput object
        prepare_ouput = OCROutput()
        try:

            # Apply OCR using Tesseract
            data = pytesseract.image_to_data(Image.open(file_location),
                                             lang="+".join(self.languages),
                                             output_type=self.output_type)

            # Prepare OCR ouput
            prepare_ouput = self._process_output(data)

            return prepare_ouput

        except Exception as e:
            print(e)
            return prepare_ouput

    @staticmethod
    def _process_output(ocr_results) -> OCROutput:
        output_result = OCROutput()
        try:
            output_result.line_num = ocr_results["line_num"]
            output_result.word_num = ocr_results["word_num"]
            output_result.text = ocr_results["text"]
            output_result.confidence = ocr_results["conf"]
            output_result.x = ocr_results["left"]
            output_result.y = ocr_results["top"]
            output_result.width = ocr_results["width"]
            output_result.height = ocr_results["height"]

            return output_result
        except Exception as e:
            print(e)
            return output_result

