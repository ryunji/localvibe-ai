import easyocr
import numpy as np
from pdf2image import convert_from_path
import time
import re


class EasyOCREngine:
    """
    EasyOCR 기반 OCR 서비스 클래스

    기능:
    1. PDF → 이미지 변환
    2. 이미지 → OCR 수행
    3. 페이지 진행률 출력
    4. confidence 기반 필터링
    5. 전체 소요 시간 측정
    """

    def __init__(self, use_gpu: bool = False, conf_th: float = 0.6):
        """
        :param use_gpu: GPU 사용 여부
        :param conf_th: confidence 임계값 (이 값 이하 결과는 버림)
        """
        print("🔧 EasyOCR 초기화 중...")
        self.reader = easyocr.Reader(['ko', 'en'], gpu=use_gpu, verbose=True)
        self.conf_th = conf_th
        print("✅ EasyOCR 초기화 완료")

    def _normalize_text(self, text: str) -> str:
        """
        노이즈 제거:
        - URL 제거
        - 과도한 공백 정리
        """
        text = re.sub(r"https?://\S+", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def extract_text_from_pdf(self, pdf_path: str, max_pages: int | None = None) -> str:
        """
        PDF에서 텍스트 추출

        :param pdf_path: OCR 대상 PDF 경로
        :param max_pages: 테스트용 페이지 제한
        :return: 추출된 전체 텍스트
        """

        total_start = time.time()

        print("📄 PDF 로딩 중...")

        images = convert_from_path(
            pdf_path,
            first_page=1,
            last_page=max_pages
        )

        total_pages = len(images)

        print(f"✅ 총 {total_pages} 페이지 이미지 변환 완료")

        full_text = ""

        for idx, img in enumerate(images):

            page_number = idx + 1

            print(f"\n🚀 OCR 시작 - Page {page_number}/{total_pages}")
            page_start = time.time()

            img_np = np.array(img)

            # detail=1 → (bbox, text, confidence)
            result = self.reader.readtext(img_np, detail=1)

            page_text_count = 0

            for bbox, text, conf in result:

                # confidence 필터
                if conf < self.conf_th:
                    continue

                text = self._normalize_text(text)

                if not text:
                    continue

                full_text += text + "\n"
                page_text_count += 1

            page_elapsed = time.time() - page_start
            print(f"📌 추출 라인 수: {page_text_count}")
            print(f"⏱ Page {page_number} 완료 ({page_elapsed:.2f}초)")

        total_elapsed = time.time() - total_start

        print("\n🎉 OCR 전체 완료")
        print(f"🕒 전체 소요 시간: {total_elapsed:.2f}초")

        return full_text