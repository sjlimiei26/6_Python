"""
    STEP 7. 집계
"""
import pandas as pd
from step06 import handle_missing
from step05 import detect_outliers
from step04 import df as df4

df5, _, _, _ = detect_outliers(df4)
df6, _, _ = handle_missing(df5)

def analyze(df: pd.DataFrame):
    print("1. 전체 요약")
    print(f"- 행 수: {len(df):,}")
    print(f"- 자전거 수: {df['bike_id'].nunique():,}")
    print(f"- 이용자 수: {df['user_id'].nunique():,}")
    print(f"- 총 이동 거리: {df['distance_km'].sum():,.2f} km")
    print(f"- 총 매출: {df['fee'].sum():,.0f} 원")
    print(f"- 평균 대여 시간: {df['duration_min'].mean():,.1f} 분")
    print("\n2. 자치구별 집계 (매출 내림차순)")
    district_agg = df.groupby('district').agg(
        건수=('rental_id', 'count'),
        이동거리=('distance_km', 'sum'),
        매출=('fee', 'sum')
    ).sort_values('매출', ascending=False)
    print(district_agg)
    
    print("\n3. 자전거 타입별 집계")
    bike_agg = df.groupby('bike_type').agg(
        건수=('rental_id', 'count'),
        평균이동거리=('distance_km', 'mean'),
        평균대여시간=('duration_min', 'mean')
    )
    print(bike_agg)
    
    print("\n4. 결제수단별 건수")
    print(df['payment_method'].value_counts())

if __name__ == "__main__":
    print("=" * 60)
    print("\t 집계 결과")
    analyze(df6)
    print("=" * 60)
