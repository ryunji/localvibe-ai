"""
전시회/이벤트 정보 수집 및 AI 처리 시스템
필요한 패키지: pip install requests beautifulsoup4 pandas anthropic
"""

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict
import time

class EventCollector:
    def __init__(self):
        self.events = []
        
    # 1. 공공데이터 API 활용
    def fetch_public_api_data(self, api_key: str = None):
        """
        문화체육관광부 공공데이터 API 예시
        실제 사용시 https://www.data.go.kr/ 에서 API 키 발급 필요
        """
        if not api_key:
            print("⚠️ API 키가 필요합니다. data.go.kr에서 발급받으세요.")
            return []
        
        # 공연전시 정보 API 엔드포인트 예시
        url = "http://www.culture.go.kr/openapi/rest/publicperformancedisplays/area"
        
        params = {
            'serviceKey': api_key,
            'keyword': '전시',
            'sortStdr': '1',  # 등록일순
            'numOfRows': '100',
            'pageNo': '1'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                # XML 또는 JSON 파싱 (API에 따라 다름)
                print("✅ 공공데이터 API 호출 성공")
                # 실제 파싱 로직 추가 필요
                return self._parse_public_api(response.text)
            else:
                print(f"❌ API 호출 실패: {response.status_code}")
        except Exception as e:
            print(f"❌ API 오류: {e}")
        
        return []
    
    def _parse_public_api(self, data):
        """API 응답 파싱 (형식에 맞게 수정 필요)"""
        # 예시 데이터 구조
        return []
    
    # 2. 웹 스크래핑
    def scrape_museum_websites(self):
        """주요 미술관/갤러리 웹사이트 스크래핑"""
        events = []
        
        # 예시: 서울시립미술관
        try:
            url = "https://sema.seoul.go.kr/kr/exhibition/exhibitionNow"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 실제 사이트 구조에 맞게 selector 수정 필요
                exhibition_items = soup.select('.exhibition-item')  # 예시 selector
                
                for item in exhibition_items:
                    event = {
                        'title': item.select_one('.title').text.strip() if item.select_one('.title') else '',
                        'location': '서울시립미술관',
                        'date': item.select_one('.date').text.strip() if item.select_one('.date') else '',
                        'source': 'sema',
                        'url': url
                    }
                    events.append(event)
                
                print(f"✅ 서울시립미술관: {len(exhibition_items)}개 전시 수집")
        except Exception as e:
            print(f"❌ 스크래핑 오류: {e}")
        
        # 다른 사이트들 추가
        events.extend(self._scrape_mmca())  # 국립현대미술관
        events.extend(self._scrape_galleries())  # 기타 갤러리
        
        return events
    
    def _scrape_mmca(self):
        """국립현대미술관 스크래핑"""
        # 구현 예시
        return []
    
    def _scrape_galleries(self):
        """기타 갤러리 스크래핑"""
        # 구현 예시
        return []
    
    # 3. 티켓 플랫폼 스크래핑
    def scrape_ticket_platforms(self):
        """인터파크, 예스24 등 티켓 플랫폼"""
        events = []
        
        try:
            # 인터파크 전시 페이지 예시
            url = "http://ticket.interpark.com/TPGoodsList.asp?Ca=Ar"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 실제 구조에 맞게 수정 필요
                items = soup.select('.goodsBox')  # 예시 selector
                
                for item in items[:50]:  # 최대 50개
                    event = {
                        'title': item.select_one('.goodsName').text.strip() if item.select_one('.goodsName') else '',
                        'location': item.select_one('.placeName').text.strip() if item.select_one('.placeName') else '',
                        'date': item.select_one('.playDate').text.strip() if item.select_one('.playDate') else '',
                        'source': 'interpark',
                        'url': url
                    }
                    events.append(event)
                
                print(f"✅ 인터파크: {len(items)}개 전시 수집")
        except Exception as e:
            print(f"❌ 티켓 플랫폼 스크래핑 오류: {e}")
        
        return events
    
    def collect_all_data(self, api_key: str = None):
        """모든 소스에서 데이터 수집"""
        print("🔍 데이터 수집 시작...\n")
        
        all_events = []
        
        # 1. 공공 API
        print("1️⃣ 공공데이터 API 수집 중...")
        all_events.extend(self.fetch_public_api_data(api_key))
        time.sleep(1)
        
        # 2. 웹 스크래핑
        print("\n2️⃣ 미술관/갤러리 웹사이트 스크래핑 중...")
        all_events.extend(self.scrape_museum_websites())
        time.sleep(1)
        
        # 3. 티켓 플랫폼
        print("\n3️⃣ 티켓 플랫폼 스크래핑 중...")
        all_events.extend(self.scrape_ticket_platforms())
        
        self.events = all_events
        print(f"\n✅ 총 {len(all_events)}개 이벤트 수집 완료")
        
        return all_events


class AIEventProcessor:
    """AI를 활용한 이벤트 데이터 처리"""
    
    def __init__(self, api_key: str = None):
        """
        Anthropic API 키 필요 (https://console.anthropic.com/)
        또는 OpenAI 등 다른 AI API 사용 가능
        """
        self.api_key = api_key
    
    def deduplicate_events(self, events: List[Dict]) -> List[Dict]:
        """AI로 중복 이벤트 제거"""
        if not events:
            return []
        
        print("\n🤖 AI로 중복 제거 중...")
        
        # 간단한 중복 제거 (제목 기반)
        unique_events = {}
        for event in events:
            title = event.get('title', '').strip()
            if title and title not in unique_events:
                unique_events[title] = event
        
        print(f"✅ {len(events)} -> {len(unique_events)}개로 중복 제거")
        return list(unique_events.values())
    
    def structure_event_data(self, raw_event: Dict) -> Dict:
        """비정형 데이터를 구조화"""
        # AI API 호출 대신 기본 구조화
        structured = {
            'id': hash(raw_event.get('title', '') + raw_event.get('location', '')),
            'title': raw_event.get('title', ''),
            'location': raw_event.get('location', ''),
            'date_range': raw_event.get('date', ''),
            'category': self._categorize_event(raw_event.get('title', '')),
            'source': raw_event.get('source', ''),
            'url': raw_event.get('url', ''),
            'created_at': datetime.now().isoformat()
        }
        return structured
    
    def _categorize_event(self, title: str) -> str:
        """이벤트 카테고리 분류"""
        title_lower = title.lower()
        if any(word in title_lower for word in ['미술', '전시', '작품', '갤러리']):
            return '미술전시'
        elif any(word in title_lower for word in ['공연', '콘서트', '뮤지컬']):
            return '공연'
        elif any(word in title_lower for word in ['축제', '페스티벌']):
            return '축제'
        else:
            return '기타'
    
    def process_all_events(self, events: List[Dict]) -> List[Dict]:
        """모든 이벤트 처리"""
        print("\n🔧 AI 처리 시작...\n")
        
        # 중복 제거
        unique_events = self.deduplicate_events(events)
        
        # 구조화
        print("\n📊 데이터 구조화 중...")
        structured_events = [
            self.structure_event_data(event) 
            for event in unique_events
        ]
        
        print(f"✅ {len(structured_events)}개 이벤트 구조화 완료")
        return structured_events


class EventRecommender:
    """사용자 맞춤 추천 시스템"""
    
    def recommend_by_preference(self, events: List[Dict], user_prefs: Dict) -> List[Dict]:
        """사용자 선호도 기반 추천"""
        preferred_category = user_prefs.get('category', '미술전시')
        preferred_location = user_prefs.get('location', '')
        
        scored_events = []
        for event in events:
            score = 0
            
            # 카테고리 매칭
            if event.get('category') == preferred_category:
                score += 10
            
            # 위치 매칭
            if preferred_location and preferred_location in event.get('location', ''):
                score += 5
            
            scored_events.append({**event, 'score': score})
        
        # 점수순 정렬
        scored_events.sort(key=lambda x: x['score'], reverse=True)
        return scored_events[:10]
    
    def natural_language_search(self, events: List[Dict], query: str) -> List[Dict]:
        """자연어 검색"""
        query_lower = query.lower()
        results = []
        
        for event in events:
            # 간단한 키워드 매칭
            if (query_lower in event.get('title', '').lower() or
                query_lower in event.get('location', '').lower()):
                results.append(event)
        
        return results


# 실행 예시
def main():
    print("=" * 60)
    print("🎨 전시회/이벤트 정보 수집 시스템")
    print("=" * 60)
    
    # 1-3. 데이터 수집
    collector = EventCollector()
    raw_events = collector.collect_all_data(api_key=None)  # API 키 입력
    
    # 4. AI 처리
    processor = AIEventProcessor()
    structured_events = processor.process_all_events(raw_events)
    
    # 데이터 저장
    df = pd.DataFrame(structured_events)
    df.to_csv('events_data.csv', index=False, encoding='utf-8-sig')
    print(f"\n💾 데이터 저장 완료: events_data.csv")
    
    # 추천 시스템 예시
    recommender = EventRecommender()
    user_prefs = {
        'category': '미술전시',
        'location': '서울'
    }
    
    recommendations = recommender.recommend_by_preference(structured_events, user_prefs)
    print(f"\n🎯 추천 이벤트 (상위 {len(recommendations)}개):")
    for i, event in enumerate(recommendations[:5], 1):
        print(f"{i}. {event['title']} - {event['location']}")
    
    # 자연어 검색 예시
    search_results = recommender.natural_language_search(structured_events, "홍대")
    print(f"\n🔍 '홍대' 검색 결과: {len(search_results)}개")

if __name__ == "__main__":
    main()