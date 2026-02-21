from paddleocr import PaddleOCR
from pdf2image import convert_from_path
import numpy as np

class OCRService:

    def __init__(self, use_gpu=False):
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang="korean",
            use_gpu=use_gpu
        )


    def extract_text_from_pdf(self, pdf_path: str) -> str:

        images = convert_from_path(
            pdf_path,
            poppler_path=r"C:\poppler-25.12.0\Library\bin"
        )

        full_text = ""

        for img in images:
            img_np = np.array(img)

            result = self.ocr.ocr(img_np, cls=True)

            if not result:
                continue

            for line in result:
                full_text += line[1][0] + "\n"

        return full_text