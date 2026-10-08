"""
    STEP 2. 자전거 마스터 정제

    대상 : raw-bikes.csv

    요구사항
    - station_id : 대문자로 통일, 빈 값은 결측 처리
    - bike_type : 일반 / 전동 두가지로 통일
    - gear_count : 단위 문자 제거 후 정수로 변환
    - daily_fee : 콤마 제거 후 정수로 변환
    - manufacture_year : 정수로 변환 (실패 시 결측 처리)
    - bike_id 기준 중복 제거
"""
import unicodedata
import pandas as pd

from step01 import raw_bikes

def clean_nums(df:pd.DataFrame, cols:list):
    df = df.copy()
    df[cols] = df[cols].transform(lambda s : s.str.replace(r"[,단]", "", regex=True))
    df[cols] = df[cols].transform(lambda s : pd.to_numeric(s, errors="coerce"))

    return df

def clean_bikes(df:pd.DataFrame):
    df = df.copy()

    # 전각 문자 변환
    for col in df.columns:
        df[col] = df[col].transform(lambda d: unicodedata.normalize("NFKC", d))

    # station_id 정제
    df["station_id"] = df["station_id"].str.upper().replace("", pd.NA)

    # bike_type 정제
    df["bike_type"] = (df["bike_type"]
                            .str.replace("일 반", "일반")
                            .str.replace("electric", "전동", case=False)
                            .str.replace("일반형", "일반")
                            .str.replace(r"\s+", "", regex=True))
    
    # gear_count, daily_fee, manufacture_year 정제
    cols = ["gear_count", "daily_fee", "manufacture_year"]
    df = clean_nums(df, cols)

    # 중복 제거
    df = df.drop_duplicates(subset=["bike_id"], keep="first")

    return df.reset_index(drop=True)


if __name__ == "__main__":
    df = clean_bikes(raw_bikes)
    print("=" * 60)
    print("\t 정제 결과")
    print(f"""
        행수 : {len(df)}
        bike_type 고유값 : {df["bike_type"].unique().tolist()}
        station_id 고유값 : {df["station_id"].nunique()}종 + 결측 {df["station_id"].isna().sum()}건 {df["station_id"].unique().tolist()}
        gear_count 범위 : {df["gear_count"].min():,} ~ {df["gear_count"].max():,}
        daily_fee 범위 : {df["daily_fee"].min():,} ~ {df["daily_fee"].max():,}
    """)
    print("=" * 60)