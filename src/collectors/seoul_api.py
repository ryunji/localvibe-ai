# ============================================================
# 5. src/collectors/seoul_api.py (API 수집기)
# ============================================================
import requests
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class SeoulAPICollector:
    
    def __init__(self):
        self.api_key  = os.getenv("SEOUL_API_KEY")
        self.base_url = "http://openapi.seoul.go.kr:8088"
    
    def fetch_exhibitions(self, start=1, end=100) -> List[Dict]:
        """서울시 전시회 정보 수집"""
        url = f"{self.base_url}/{self.api_key}/json/culturalEventInfo/{start}/{end}/"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'culturalEventInfo' not in data:
                    print(f"⚠️ API 응답 오류: {data}")
                    return []
                
                result = data['culturalEventInfo']
                events = result.get('row', [])
                
                # 전시회만 필터링
                exhibitions = [
                    e for e in events 
                    if any(keyword in (e.get('CODENAME', '') + e.get('TITLE', '')) 
                        for keyword in ['전시', '미술', '박물관', '갤러리'])
                ]
                
                print(f"✅ {len(exhibitions)}개 전시회 수집 완료!")
                return exhibitions
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"🚫 수집 오류: {e}")
            return []
    
    def parse_to_model_data(self, raw_data: Dict) -> Dict:
        
        """API 데이터를 DB 모델 형식으로 변환"""
        return {
            'title': raw_data.get('TITLE', ''),
            'place': raw_data.get('PLACE', ''),
            'address': raw_data.get('GUNAME', ''),
            'start_date': raw_data.get('STRTDATE', ''),
            'end_date': raw_data.get('END_DATE', ''),
            'use_fee': raw_data.get('USE_FEE', ''),
            'target': raw_data.get('USE_TRGT', ''),
            'contact': raw_data.get('ORG_LINK', ''),
            'homepage': raw_data.get('HMPG_ADDR', ''),
            'category': raw_data.get('CODENAME', ''),
            'source': 'seoul_api',
            'latitude': float(raw_data.get('LAT', 0)) if raw_data.get('LAT') else None,
            'longitude': float(raw_data.get('LOT', 0)) if raw_data.get('LOT') else None,
        }
        
# 파일이 직접 실행될 때만 작동하는 코드.
if __name__ == "__main__":
    
    # 1. 수집기 객체 생성
    collector = SeoulAPICollector()
    
    # 2. 데이터 가져오기 실행
    print("🚀 데이터 수집을 시작합니다...")
    data = collector.fetch_exhibitions(start=1, end=150)
    
    # 3. 결과물 확인
    if data:
        for i, item in enumerate(data[:5], 1): # 상위 5개 출력
            parsed = collector.parse_to_model_data(item)
            print(f"{i}. [{parsed['category']}] {parsed['title']}")
            print(f"   📅 기간: {parsed['start_date']} ~ {parsed['end_date']}")
            print(f"   📍 장소: {parsed['place']} ({parsed['address']})")
            print(f"   💰 비용: {parsed['use_fee']}")
            print("-" * 50)
    else:
        print("검색된 데이터가 없습니다.")        