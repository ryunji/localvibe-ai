import easyocr
import numpy as np
from pdf2image import convert_from_path
import time


class EasyOCREngine:
    """
    EasyOCR 기반 OCR 서비스 클래스
    """

    def __init__(self, use_gpu: bool = False):
        print("🔧 EasyOCR 초기화 중...")
        self.reader = easyocr.Reader(
            ['ko', 'en'],
            gpu=use_gpu,
            verbose=True
        )
        print("✅ EasyOCR 초기화 완료")

    def extract_text_from_pdf(self, pdf_path: str, max_pages: int | None = None) -> str:
        """
        PDF에서 텍스트 추출
        max_pages로 테스트 범위 제한 가능
        """

        print("📄 PDF 로딩 중...")

        images = convert_from_path(
            pdf_path,
            first_page=1,
            last_page=max_pages
        )

        print(f"✅ 총 {len(images)} 이미지 변환 완료")

        full_text = ""

        for idx, img in enumerate(images):
            print(f"\n🚀 OCR 시작 - Page {idx+1}")
            start_time = time.time()

            img_np = np.array(img)
            result = self.reader.readtext(img_np)

            for line in result:
                full_text += line[1] + "\n"

            elapsed = time.time() - start_time
            print(f"⏱ Page {idx+1} 완료 ({elapsed:.2f}초)")

        print("\n🎉 OCR 전체 완료")

        return full_text