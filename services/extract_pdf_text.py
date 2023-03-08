from PyPDF2 import PdfReader
from models.ocr_output import OCROutput


def get_text(file_location: str) -> OCROutput:
    output = OCROutput()
    try:
        lines_text = []
        reader = PdfReader(file_location)
        pages = reader.pages
        for page in pages:
            lines_text.extend(page.extract_text().splitlines())

        for line_idx, line in enumerate(lines_text):
            for word_idx, word in enumerate(line.split()):
                output.line_num.append(line_idx)
                output.word_num.append(word_idx)
                output.text.append(word.strip())
                output.confidence.append(100.0)
                output.x.append(0)
                output.y.append(0)
                output.width.append(0)
                output.height.append(0)

        return output
    except Exception as e:
        print(e)
        return output
