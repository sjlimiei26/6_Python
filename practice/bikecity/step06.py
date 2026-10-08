"""
    STEP 6. 결측 처리
"""
import pandas as pd
from step05 import detect_outliers
from step04 import df as df4

df5, _, _, _ = detect_outliers(df4)

def handle_missing(df: pd.DataFrame):
    df = df.copy()
    
    # fee 결측 복원 (대여 시간(분) × 분당요금)
    fee_missing = df["fee"].isna()
    recovered_fee_count = fee_missing.sum()
    
    if recovered_fee_count > 0:
        minute_fee = (df["fee"] / df["duration_min"]).median()
        df.loc[fee_missing, "fee"] = df.loc[fee_missing, "duration_min"] * minute_fee
    
    # distance_km 결측 제거
    dist_missing = df["distance_km"].isna()
    removed_dist_count = dist_missing.sum()
    
    df = df[~dist_missing].reset_index(drop=True)
    
    return df, recovered_fee_count, removed_dist_count

if __name__ == "__main__":
    df6, rec_fee, rem_dist = handle_missing(df5)
    print("=" * 60)
    print("\t 결측 처리 결과")
    print(f"요금 복원 : {rec_fee}건")
    print(f"거리 결측 제거 : {rem_dist}건")
    print(f"최종 행 수 : {len(df6):,}건")
    print("=" * 60)
