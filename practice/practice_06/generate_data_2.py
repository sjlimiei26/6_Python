import numpy as np
import pandas as pd

# 재현성을 위한 시드 고정
np.random.seed(42)

# 1. 기본 데이터 생성 (200행)
n_rows = 200

# 날짜 (최근 8주간의 주간/일간 데이터)
dates = pd.date_range(start="2026-01-01", periods=n_rows, freq="D")

# 범주형 변수
departments = ["개발팀", "영업팀", "디자인팀", "경영지원팀", "마케팅팀"]
traffic_types = ["Inbound", "Outbound"]
protocol_types = ["HTTPS", "SFTP", "API Call", "DB Query"]

dep_sample = np.random.choice(departments, size=n_rows, p=[0.3, 0.25, 0.15, 0.15, 0.15])
traffic_sample = np.random.choice(traffic_types, size=n_rows, p=[0.6, 0.4])
protocol_sample = np.random.choice(protocol_types, size=n_rows, p=[0.5, 0.2, 0.2, 0.1])

# 수치형 변수 (정상 범위)
# 트래픽량 (GB): 평균 50, 표준편차 15
traffic_gb = np.random.normal(loc=50, scale=15, size=n_rows).round(2)
traffic_gb = np.clip(traffic_gb, 5, None)  # 음수 방지

# 접속 세션 수 (Session Count): 평균 1200, 표준편차 300
session_count = np.random.normal(loc=1200, scale=300, size=n_rows).astype(int)

# 평균 응답 시간 (Response Time ms): 평균 45ms, 표준편차 10ms
response_time_ms = np.random.normal(loc=45, scale=10, size=n_rows).round(1)

# DataFrame 생성
df = pd.DataFrame(
    {
        "Date": dates,
        "Department": dep_sample,
        "Traffic_Type": traffic_sample,
        "Protocol": protocol_sample,
        "Traffic_GB": traffic_gb,
        "Session_Count": session_count,
        "Response_Time_MS": response_time_ms,
    }
)

# 2. 현실적인 이상치(Outlier) 주입 (의심스러운 보안/성능 징후)
# 이상치 1: 특정 날짜 마케팅팀의 대용량 Outbound 트래픽 폭증 (데이터 유출 의심)
df.loc[15, "Traffic_GB"] = 480.5
df.loc[15, "Department"] = "마케팅팀"
df.loc[15, "Traffic_Type"] = "Outbound"

# 이상치 2: 특정 날짜 DB Query 응답시간 병목 현상
df.loc[88, "Response_Time_MS"] = 850.0
df.loc[88, "Protocol"] = "DB Query"

# 이상치 3: 세션 수 대비 트래픽 비정상 대폭증
df.loc[142, "Traffic_GB"] = 390.0
df.loc[142, "Session_Count"] = 150

# 3. 결측치(NaN) 주입 (약 3~5%)
nan_idx_1 = np.random.choice(n_rows, size=8, replace=False)
nan_idx_2 = np.random.choice(n_rows, size=10, replace=False)

df.loc[nan_idx_1, "Traffic_GB"] = np.nan
df.loc[nan_idx_2, "Department"] = np.nan

# CSV 저장 및 확인
df.to_csv("business_data.csv", index=False, encoding="utf-8-sig")
print("비즈니스 데이터셋('business_data.csv') 생성이 완료되었습니다.")
print(df.info())