"""
    STEP 3. 대여 기록 정제
    
    대상: raw-rentals.csv

    요구사항
    - distance_km, fee : 콤마 제거 후 숫자로 변환. (실패 시 결측 처리)
    - rent_time, return_time : datetime 으로 통일 (형식 3종 혼재)
    - payment_method : 공백 제거 후 대문자로 통일
    - rent_id 기준 중복 제거
"""
import pandas as pd

from step01 import raw_rentals

def clean_nums(df:pd.DataFrame, cols:list):

    for col in cols:
        df[col] = df[col].str.replace(",","")
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def clean_dates(df:pd.DataFrame, cols:list):
    for col in cols:
        df[col] = pd.to_datetime(df[col], format="mixed", errors="coerce")
    return df


def clean_rentals(df:pd.DataFrame):
    df = df.copy()

    # distance_km, fee 정제
    df = clean_nums(df, ["distance_km", "fee"])

    # rent_time, return_time 정제
    df = clean_dates(df, ["rent_time", "return_time"])
    
    # payment_method 정제
    df["payment_method"] = df["payment_method"].str.strip().str.upper()

    # 중복 제거 : rental_id
    df = df.drop_duplicates(subset=["rental_id"], keep="first")

    return df


if __name__ == "__main__":
    df = clean_rentals(raw_rentals)

    print("=" * 60)
    print("\t 정제 결과")
    print(f"""
        행수 : {len(df):,}
        distance_km 결측 : {df["distance_km"].isna().sum()}
        fee 결측 : {df["fee"].isna().sum()}
        payment_method 고유값 : {df["payment_method"].unique().tolist()}
    """)
    print("=" * 60)