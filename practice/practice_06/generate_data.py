import numpy as np
import pandas as pd

# 리포트 결과의 재현성을 위한 시드 고정
np.random.seed(42)

n_samples = 250

# 1. 컬럼 데이터 생성
dates = pd.date_range(start="2024-01-01", periods=n_samples, freq="D")
categories = np.random.choice(
    ["아우터", "상의", "바지", "잡화/신발"], size=n_samples, p=[0.25, 0.35, 0.25, 0.15]
)
brands = np.random.choice(
    ["디스이즈네버댓", "커버낫", "쿠어", "라퍼지스토어", "코드그라피"], size=n_samples
)

# 카테고리별 단가 기준 설정 및 정규분포 매출액 생성
base_sales = {"아우터": 180000, "상의": 45000, "바지": 65000, "잡화/신발": 85000}
sales = [
    int(np.random.normal(loc=base_sales[cat], scale=base_sales[cat] * 0.2))
    for cat in categories
]

# 주문 수량 및 리뷰 수 생성
quantities = np.random.randint(1, 10, size=n_samples)
review_counts = np.random.poisson(lam=45, size=n_samples)
review_scores = np.round(
    np.random.choice([3.0, 3.5, 4.0, 4.5, 5.0], size=n_samples, p=[0.05, 0.1, 0.25, 0.4, 0.2]),
    1,
)

# DataFrame 구성
df = pd.DataFrame(
    {
        "order_date": dates,
        "category": categories,
        "brand": brands,
        "sales_amount": sales,
        "quantity": quantities,
        "review_count": review_counts,
        "review_score": review_scores,
    }
)

# 2. 결측치(NaN) 주입 (약 4~5%)
nan_indices_sales = np.random.choice(n_samples, size=10, replace=False)
df.loc[nan_indices_sales, "sales_amount"] = np.nan

nan_indices_score = np.random.choice(n_samples, size=12, replace=False)
df.loc[nan_indices_score, "review_score"] = np.nan

# 3. 비즈니스 이상치(Outlier) 주입
# 이상치 1: 상의 카테고리인데 단가가 말도 안 되게 높게 들어간 데이터 (시스템 입력 오류 의심)
df.loc[15, "sales_amount"] = 2500000

# 이상치 2: 매출 대비 리뷰 수가 비정상적으로 쏠린 건 (바이럴/어뷰징 이벤트 의심)
df.loc[88, "review_count"] = 850

# CSV 파일 저장 및 로드 확인
df.to_csv("business_data.csv", index=False, encoding="utf-8-sig")
print("✅ 'business_data.csv' 데이터셋 생성이 완료되었습니다.")
print(df.info())