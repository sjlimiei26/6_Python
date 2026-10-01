"""
    Transform : 데이터 정제,계산,검증

    - 하지 않은 것: 저장(적재)

    Extract 단계에서 전달된 원본 데이터를
        DB에 저장할 수 있는 상태로 만듬
    - 타입 변환 (문자열 -> 숫자/날짜)
    - 중복 제거
    - 이상치 탐지 / 결측치 처리 (제거/대치/보간)
    - 파생 컬럼(등락,등락률,..) 계산(재계산)
    - 검증
"""
import pandas as pd

# 수치형(숫자)으로 변환할 열 목록
NUM_COLS = ["open","high","low","close","volume","change","changeRate"]

# 보간 대상 목록 (OHLC - 시가,고가,저가,종가)
OHLC = ["open","high","low","close"]


def clean_prices(records, logger):
    """
        정제 함수. 단계마다 건수를 로그로 기록.

        [처리 순서]
        1. list[dict] -> DataFrame 변환
        2. 숫자 타입 정제
        3. 날짜 타입 정제
        4. 종목 코드 정규화 (대문자, 공백 제거, ...)
        5. 중복 제거 (code,date 기준)
        6. 이상치 탐지 -> NaN 처리
        7. 결측 보간 (interpolate -> ffill -> bfill)
        8. OHLC 정합성
        9. 소수점 -> 정수 (반올림)
        10. 등락, 등락률 재계산
    """

    # 1. DataFrame 변환

    # 2. 숫자 타입 정제
    #    -콤마 제거: "1,000" -> "1000" -> 1000
    #    -변환 실패 시 NaN 처리

    # 3. 날짜 타입 정제
    #    -날짜 형식이 다르더라도 변환될 수 있어야 함
    #    -변환 실패 시 NaN 처리
    

def validate(df, logger):
    """
        정제 작업 완료 후 검증 결과를 확인하는 함수
        검증 실패 시 파이프라인 멈춤!

        [검증 항목]
        - 날짜 타입 열이 datetime 타입인지
        - 중복 데이터가 없는지 (code,date 기준)
        - 종가 데이터에 결측이 없는지
        - OHLC 논리 정합성 : 저가 <= 시가,종가 <= 고가
        - 거래량이 음수가 아닌지
    """
    pass