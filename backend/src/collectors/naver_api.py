import os
import requests

# 1. 네이버에서 받은 키 넣기
client_id = "t7BrDv7vgK_k4mrziZkQ"
client_secret = "4aI6gxa7fw"

def get_exhibition_blog(keyword):
    url = f"https://openapi.naver.com/v1/search/blog.json?query={keyword}&display=10"
    
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        items = response.json().get('items', [])
        for item in items:
            print(f"📌 제목: {item['title'].replace('<b>', '').replace('</b>', '')}")
            print(f"🔗 링크: {item['link']}")
            print(f"📝 요약: {item['description'][:100]}...")
            print("-" * 50)
    else:
        print(f"Error: {response.status_code}")

# 실행
get_exhibition_blog("서울 전시회 추천")