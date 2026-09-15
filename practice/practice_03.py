"""
    실습용 사이트에서
        종목 메뉴 페이지(SSR)의 섹터를 "IT 서비스"로 검색한 결과 데이터를 추출

    - 요청 주소: ??
    TODO: 오늘(09/15) 18시까지 이메일로 제출
"""
import requests

from config import BASE, TIMEOUT, HEADERS
from parsers import parse_stocks

resp = requests.get(f"{BASE}/stocks", 
                    params={"sector": "S08"}, 
                    timeout=TIMEOUT,
                    headers=HEADERS)
resp.raise_for_status()

html = resp.text
results = parse_stocks(html)
print("="*70)
print(f"\t\t********* 데이터 추출 결과 ({len(results)}개) *********")
print("-" * 70)
print(f"{'코드':<8}{'종목명':<14}{'섹터':<10}{'현재가':>10}{'등락률':>9}")
print("-" * 70)
for s in results:
    print(f"{s['code']:<8}{s['name']:<14}{s['sector']:<10}{s['price']:>12}{s['rate']:>9}")
print("="*70)