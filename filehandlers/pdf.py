from os.path import splitext
import fitz


def pdf_filehandler(file_location: str) -> str:
    new_path = splitext(file_location)[0] + '.jpg'
    pdf_document = fitz.open(file_location)
    for page in pdf_document:
        pix = page.get_pixmap()
        pix.save(new_path)
        break
    return new_path



