"""
    STEP 1. 진단
"""
import pandas as pd

from _config import raw_bikes_path,raw_rentals_path, stations_path, ENCODING

raw_bikes = pd.read_csv(raw_bikes_path(), encoding=ENCODING, dtype=str, keep_default_na=False)
raw_rentals = pd.read_csv(raw_rentals_path(), encoding=ENCODING, dtype=str, keep_default_na=False)
stations = pd.read_csv(stations_path(), encoding=ENCODING)


def step01_check(df:pd.DataFrame):
    print(f"- 행수: ({len(df):,}행) \n dtypes: \n{df.dtypes}\n")
    print(" - 컬럼별 결측 수와 비율 \n")
    print(f"{df.isna().sum()}")

def step02_duplicates(df:pd.DataFrame):
    columns = ["bike_id", "rental_id"]  # 중복 체크 컬럼 목록

    for col in columns:
        if col in df.columns:
            print(f"'{col}' 중복 건수: {df[col].value_counts()}")

def step03_unique(df:pd.DataFrame):
    columns = ["bike_type", "district", "payment_method"]

    for col in columns:
        if col in df.columns:
            print(f"'{col}' 의 고유값 목록: {df[col].unique().tolist()}")


if __name__ == "__main__":
    # {데이터명: (데이터프레임, 중복체크컬럼목록)}
    datas = {"raw_bikes":raw_bikes, 
            "raw_rentals":raw_rentals, 
            "stations":stations}

    for name, df in datas.items():
        print("=" * 60)
        print(f"{name} ---------------------------")
        print("=" * 60)

        step01_check(df)
        step02_duplicates(df)
        step03_unique(df)

    print("=" * 60)
    print("\t 확인 문항")
    print("""
        1. 자전거 개수 (bike_id) : 50, 중복 데이터 존재로 예상됨.
        2. `bike_type` 고유 값 종류 : 6가지. 실제로는 2가지 (일반, 전동)
        3. `distance_km` 숫자로 못 바꾸는 값 : N/A
    """)
    print("=" * 60)
    # print(raw_bikes["bike_id"].nunique())
    # print(raw_bikes["bike_type"].unique().tolist())
    # print(raw_rentals["distance_km"].unique().tolist())