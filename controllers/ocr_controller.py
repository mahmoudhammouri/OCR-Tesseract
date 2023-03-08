from fastapi import APIRouter
from fastapi import File, UploadFile
import mimetypes
from models.ocr_reading import OCRResult
from services.ocr_invoice_service import read_invoice
from helpers.file import remove_uploaded_file, save_uploaded_file
from services.ocr_doc_service import perform_document_ocr
from services import ocr_pipline

ocr_router = APIRouter(prefix="/ocr", tags=['OCR'])


@ocr_router.post('/document', response_model=OCRResult)
async def ocr_read_document(file: UploadFile = File(...)) -> OCRResult:
    # Save uploaded file
    file_location = save_uploaded_file(file)
    file_type = mimetypes.guess_type(file_location)[0]

    # Run ocr pipline
    ocr_output = ocr_pipline.run_pipline(file_location=file_location, file_type=file_type)

    # Prepare OCR for document
    result = perform_document_ocr(file_location=file_location,file_type = file_type, ocr_output=ocr_output)

    # Remove uploaded file
    remove_uploaded_file(file_location)
    return result


@ocr_router.post('/invoice')
async def ocr_read_invoice(file: UploadFile = File(...)) -> OCRResult:
    # Save uploaded file
    file_location = save_uploaded_file(file)
    file_type = mimetypes.guess_type(file_location)[0]

    # Run ocr pipline
    ocr_output = ocr_pipline.run_pipline(file_location=file_location, file_type=file_type)

    # Prepare OCR for invoices
    result = read_invoice(file_location=file_location, ocr_output=ocr_output)

    # Remove uploaded file
    remove_uploaded_file(file_location)
    return result
