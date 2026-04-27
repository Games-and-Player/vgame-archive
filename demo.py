import sys, json
from paddleocr import PaddleOCR

img = sys.argv[1]
ocr = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=True, lang='ch')
result = ocr.predict(img)

for r in result:
    texts = r['rec_texts']
    scores = r['rec_scores']
    for t, s in zip(texts, scores):
        print(f"[{s:.2f}] {t}")
