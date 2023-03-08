from pydantic import BaseModel


class OCROutput(BaseModel):
    line_num: list = []
    word_num: list = []
    text: list = []
    confidence: list = []
    x: list = []
    y: list = []
    width: list = []
    height: list = []
