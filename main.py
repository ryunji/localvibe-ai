# main.py

import runpy

def main():
    
    # 파이썬은 줄바꿈 자체가 문장의 끝이므로, 써도 무방하지만 세미콜론(;)을 쓰지 않는다.
    runpy.run_path("src/collectors/seoul_api.py", run_name="__main__")

if __name__ == "__main__":
    main()