"""
    STEP 5. 이상치와 논리 검사
"""
import pandas as pd
from step04 import df as df4

def detect_outliers(df: pd.DataFrame):
    df = df.copy()
    
    # 파생 컬럼: 대여 시간(분)
    df["duration_min"] = (df["return_time"] - df["rent_time"]).dt.total_seconds() / 60
    
    # ① 반납 시각이 대여 시각보다 앞서면 안 됨
    cond1 = df["return_time"] <= df["rent_time"]
    
    # ② 요금이 음수면 안 됨
    cond2 = df["fee"] < 0
    
    # ③ 이동 거리가 물리 상한을 넘으면 안 됨
    # speed(km/h) = distance_km / (duration_min / 60)
    # duration_min 이 0이하인 경우를 피하기 위해 (cond1에서 걸러지지만 여기서도 안전하게 처리)
    speed = df["distance_km"] / (df["duration_min"] / 60)
    cond3 = (speed > 50) & (~cond1) # cond1인 경우는 시간 역전이라 속도 계산이 무의미함
    
    # 이상치 탐지
    outliers = cond1 | cond2 | cond3
    
    return df[~outliers].reset_index(drop=True), cond1, cond2, cond3

if __name__ == "__main__":
    df5, c1, c2, c3 = detect_outliers(df4)
    print("=" * 60)
    print("\t 이상치 검사 결과")
    print(f"① 반납 <= 대여 : {c1.sum()}건")
    print(f"② 요금 음수 : {c2.sum()}건")
    print(f"③ 속도 > 50km/h : {c3.sum()}건")
    print(f"합계 (중복 제외) : {(c1 | c2 | c3).sum()}건")
    print(f"제거 후 행 수 : {len(df5):,}건")
    print("=" * 60)
