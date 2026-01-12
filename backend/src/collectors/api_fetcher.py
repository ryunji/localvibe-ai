import requests

# 1. 설정 (주신 정보를 그대로 넣었습니다)
# 공공데이터포털은 보통 파이썬에서 Decoding 키를 쓸 때 가장 잘 작동합니다.
SERVICE_KEY = 'Bwxg8WwP8Xj8wi2Rm0DaxT8glYkhT64wTb7tW4L0Vhtq3xsQkrIzkQ0sfKvqT/75g5FK9bVG+asAdHiDY2CAJw=='

# 주신 End Point 주소 (반드시 http로 시작하고 오타가 없어야 함)
URL = 'http://api.data.go.kr/openapi/tn_pubr_public_pblprfr_event_info_api'

params = {
    'serviceKey': SERVICE_KEY,
    'type': 'json',    # JSON 포맷으로 받기
    'pageNo': '1',
    'numOfRows': '10'
}

try:
    print("🚀 공공데이터 서버에서 전시/행사 정보를 가져오는 중...")
    
    # params를 통해 키를 전달하면 requests가 알아서 인코딩해줍니다.
    response = requests.get(URL, params=params)
    
    print(f"📡 응답 상태 코드: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        
        # 데이터 구조 파고들기
        items = data.get('response', {}).get('body', {}).get('items', [])
        
        if not items:
            print("✅ 연결은 됐지만, 현재 제공되는 데이터가 비어있습니다.")
            print("응답 내용:", data) # 데이터가 왜 비었는지 확인용
        else:
            print(f"🎉 성공! 총 {len(items)}개의 정보를 찾았습니다.\n")
            for i, item in enumerate(items, 1):
                name = item.get('eventNm', '이름 없음')
                place = item.get('opar', '장소 정보 없음')
                start = item.get('eventStartDate', '-')
                end = item.get('eventEndDate', '-')
                
                print(f"{i}. [{name}]")
                print(f"   📍 장소: {place}")
                print(f"   📅 기간: {start} ~ {end}")
                print("-" * 40)
    else:
        print(f"❌ 요청 실패 (상태코드 {response.status_code})")
        print(f"메시지: {response.text}")

except Exception as e:
    print(f"⚠️ 파이썬 코드 실행 에러: {e}")