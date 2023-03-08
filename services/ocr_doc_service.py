import numpy as np
from PIL import Image
from models.ocr_reading import OCRResult
from models.ocr_output import OCROutput
from helpers.image_processing import detect_blur


def perform_document_ocr(file_location: str, file_type: str, ocr_output: OCROutput) -> OCRResult:
    """
    performs ocr reading for picture or documents using easyocr
    Args:
        file_location: the path for the file that need to perform ocr on
        file_type :
        ocr_output: OCR output data


    Returns:
    :param :

    """

    ocr_result = OCRResult()
    try:
        try:
            # Blur Detection
            img = np.array(Image.open(file_location).convert('L'))
            if detect_blur(img):
                ocr_result.blurred = False
            else:
                ocr_result.blurred = True
        except Exception as e:
            print(e)

        if len([t for t in ocr_output.text if len(t.strip()) > 0]) != 0:
            # Add image is readable
            ocr_result.readable = True

            # Add extracted text
            ocr_result.readings = " ".join(ocr_output.text)

            # Add confidence score
            ocr_result.confidence_score = float(np.mean([n for n in ocr_output.confidence if n != -1]))

        else:
            # Add image is not readable
            ocr_result.readable = False

            # Add a message if the image has no text
        if not ocr_result.readable:
            ocr_result.message = "Most likely there is no text in the image"

        return ocr_result
    except Exception as e:
        print(e)
        return ocr_result
