import numpy as np
import pandas as pd
from PIL import Image
from models.ocr_reading import OCRResult
from models.ocr_output import OCROutput
from helpers.image_processing import detect_blur
from helpers.text_processing import get_possible_floats

ARABIC_KEYWORDS = ['اجمالي', 'مجموع', 'صافي', 'المجموع', 'الرصيد']
ENGLISH_KEYWORDS = ['total', 'tot', 'paid', 'Balance']
KEYWORDS = ENGLISH_KEYWORDS + ARABIC_KEYWORDS


def prepare_lines(df: pd.DataFrame) -> dict:
    try:
        dict_lines = {}
        for i in range(df.shape[0]):
            line_num = df.loc[i, "line_num"]
            if line_num not in dict_lines.keys():
                dict_lines[line_num] = []
            if len(df.loc[i, "text"].strip()) > 0:
                dict_lines[line_num].append(df.loc[i, "text"])

        return dict_lines

    except Exception as e:
        print(e)
        return {}


def get_invoice_info(keywords: list, ocr_output: OCROutput):
    dict_output = {
        "text": "",
        "confidence_score": 0.0,
        "key": {
            "word": "",
            "coord": [],
            "conf": 0.0
        },

        "value": {
            "str_val": "",
            "float_val": 0.0,
            "coord": [],
            "conf": 0.0
        }
    }
    try:

        # Add OCR results in dictionary
        dict_data = {
            "line_num": ocr_output.line_num,
            "word_num": ocr_output.word_num,
            "text": ocr_output.text,
            "confidence": ocr_output.confidence,
            "x": ocr_output.x,
            "y": ocr_output.y,
            "width": ocr_output.width,
            "height": ocr_output.height

        }

        # Save output in DataFrame
        df = pd.DataFrame(dict_data)

        # Prepare group output based on lines
        dict_lines = prepare_lines(df=df)

        dict_output["text"] = " ".join(df["text"].values)

        if len(dict_output["text"]) == 0:
            dict_output["confidence_score"] = 0.0
            return dict_output

        dict_output["confidence_score"] = df[df["confidence"] != -1]["confidence"].mean()

        # coord values left, top, width, height = x,y,w,h
        # to draw a box using these coordinates (x, y), (x + w, y + h)

        dict_res = {
            "key": None,
            "str_val": None,
            "float_val": None
        }

        for keyword in keywords:
            dict_res = get_possible_floats(keyword=keyword, lines=dict_lines)
            if len(dict_res) != 0:
                break

        if len(list(dict_res.keys())) > 0:
            line_num = list(dict_res.keys())[0]

            if dict_res[line_num]["key"] is not None:
                dict_output["key"]["word"] = str(dict_res[line_num]["key"])
                dict_output["key"]["coord"] = [int(c) for c in df.loc[int(line_num), ['x', 'y', 'width', 'height']]]
                dict_output["key"]["conf"] = float(df.loc[line_num, "confidence"])

                idx_val = int(dict_res[line_num]["value_index"])
                dict_output["value"]["str_val"] = str(dict_res[line_num]["str_value"])
                dict_output["value"]["float_val"] = float(dict_res[line_num]["float_value"])
                dict_output["value"]["coord"] = [int(c) for c in df.loc[idx_val, ['x', 'y', 'width', 'height']]]
                dict_output["value"]["conf"] = float(df.loc[idx_val, "confidence"])

        return dict_output
    except Exception as e:
        print(e)
        return dict_output


def read_invoice(file_location: str, ocr_output: OCROutput) -> OCRResult:
    """
    performs ocr reading on picture or documents and try to extract Bill total amount from the readings

    Args:
      file_location: the path for the file that need to perform ocr on
      ocr_output: OCR output data

    Returns:
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

            # Select key and value from ocr output
            dict_invoice_info = get_invoice_info(keywords=KEYWORDS, ocr_output=ocr_output)

            # Add extracted text
            ocr_result.readings = {key: dict_invoice_info[key] for key in ["key", "value"]}

            # Add a message if total not found in the text
            is_total_found = not (
                    ocr_result.readings["key"]["word"] is None or len(ocr_result.readings["key"]["word"]) == 0)

            ocr_result.message = "OCR Error: Couldn't extract total value" if not is_total_found else ''

            # Add confidence score
            ocr_result.confidence_score = float(np.mean([n for n in ocr_output.confidence if n != -1]))

            return ocr_result

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
