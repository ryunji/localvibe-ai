from src.services.rag.parser.junggu_parser import JungguPDFParser
import json

if __name__ == "__main__":

    with open("data/processed/jangchungdong.txt", encoding="utf-8") as f:
        text = f.read()

    parser = JungguPDFParser()
    pois = parser.parse(text)

    print(json.dumps(
    [p.to_dict() for p in pois],
    ensure_ascii=False,
    indent=4
))