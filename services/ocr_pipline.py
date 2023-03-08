from services.ocr_services.tesseract_ocr import TesseractOCR
from services import extract_pdf_text
from filehandlers.pdf import pdf_filehandler
from models.ocr_output import OCROutput
from helpers.file import remove_uploaded_file

FILE_HANDLERS = {
    "image/png": None,
    "image/jpeg": None,
    "image/tiff": None,
    "application/pdf": pdf_filehandler,
}


def run_pipline(file_location: str, file_type: str):
    ocr_output = OCROutput()

    try:

        ocr = TesseractOCR(languages=['eng', 'ara'], output_type="dict")
        if file_type == "application/pdf":
            ocr_output = extract_pdf_text.get_text(file_location=file_location)

            # Check extracted text
            # If no text extracted, then convert PDF to be as image
            if len(ocr_output.line_num) == 0:

                handler = FILE_HANDLERS[file_type]
                if handler is not None:
                    new_file_location = handler(file_location)
                    ocr_output = ocr.apply_ocr(file_location=new_file_location)

                    # remove converted PDF file
                    remove_uploaded_file(new_file_location)

                    return ocr_output
            return ocr_output

        else:
            ocr_output = ocr.apply_ocr(file_location=file_location)
            return ocr_output
    except Exception as e:
        print(e)
        return ocr_output
