"""
    STEP 4. 결합

    대여 기록 (raw-rentals.csv) 
        + 자전거 정보 (raw-bikes.csv)  --- bike_id
        + 대여소 정보 (stations.csv)   --- station_id

    요구 사항
    - how, validate 명시
    - indicator=True 매칭 실패 확인
    - 매칭 실패 시 제외하고 진행
"""
import pandas as pd

from step01 import raw_rentals, raw_bikes, stations
from step02 import clean_bikes
from step03 import clean_rentals

rentals = clean_rentals(raw_rentals)
bikes = clean_bikes(raw_bikes)

def load_merged():
    # 1. rentals -> bikes 결합
    df = rentals.merge(bikes, on="bike_id", how="left", validate="many_to_one", indicator=True)
    
    # 매칭 실패 항목 확인 (rentals에는 있는데 bikes에는 없는 bike_id)
    fail_bikes = df[df["_merge"] != "both"]
    
    # 매칭 실패 항목 제외
    df = df[df["_merge"] == "both"].drop(columns=["_merge"])
    
    # 2. -> stations 결합
    df = df.merge(stations, on="station_id", how="left", validate="many_to_one", indicator=True)
    
    # 매칭 실패 항목 확인
    fail_stations = df[df["_merge"] != "both"]
    
    # 매칭 실패 항목 제외
    df = df[df["_merge"] == "both"].drop(columns=["_merge"])
    
    return df.sort_values(["rental_id"]).reset_index(drop=True), fail_bikes, fail_stations

df, fail_bikes, fail_stations = load_merged()

if __name__ == "__main__":
    print("=" * 60)
    print("\t 확인 문항")
    print(f"""
        1. 매칭 실패 bike_id : {fail_bikes['bike_id'].unique().tolist()} ({len(fail_bikes)}건)
        2. 이런 데이터는 '고아 레코드(Orphan record)' 또는 '참조 무결성 오류'라고 부릅니다. 
           원인을 파악하여 마스터 데이터(bikes)에 해당 자전거를 추가하거나, 분석에서 제외해야 합니다.
        3. 자치구명이 결측인 행 원인 : 자전거 마스터 데이터에서 station_id가 결측인 자전거(B043)의 대여 기록이 {len(fail_stations)}건 존재하며, 
           stations 테이블과 결합 시 station_id가 없어 매칭되지 않기 때문입니다.
    """)
    print("-" * 60)
    print("\t 결합 결과")
    print(f"""
        결합 전 대여 기록 행수 : {len(rentals):,}
        rental + bike 매칭 실패 건수 : {len(fail_bikes):,}
        bike + station 매칭 실패 건수 : {len(fail_stations):,}
        모든 매칭 실패 제외 후 최종 행수 : {len(df):,}
        자치구 결측 : {df["district"].isna().sum():,}
    """)
    print("=" * 60)