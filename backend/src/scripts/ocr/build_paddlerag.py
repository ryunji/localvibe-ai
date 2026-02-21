from backend.src.services.rag.ocr.ocr_paddleservice import OCRService

if __name__ == "__main__":
    ocr = OCRService(use_gpu=False)
    text = ocr.extract_text_from_pdf("data/raw/gwanghuido_playground_junggu_vol07.pdf")

    with open("data/ocr/gwanghuido.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("OCR 완료")