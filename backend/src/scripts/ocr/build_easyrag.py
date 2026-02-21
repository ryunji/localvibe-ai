from src.services.rag.ocr.ocr_easyocr import EasyOCREngine
import os


if __name__ == "__main__":

    ocr = EasyOCREngine(use_gpu=False)

    pdf_path = "data/raw/gwanghuido_playground_junggu_vol07.pdf"

    text = ocr.extract_text_from_pdf(pdf_path)

    output_path = "data/processed/gwanghuido.txt"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print("📁 텍스트 저장 완료")