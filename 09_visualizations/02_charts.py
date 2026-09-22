"""
    차트, Seaborn
"""
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from chart_config import setup, out
from merged_loader import load_merged

setup()
df = load_merged()

# 종목별 일간 수익률(%)
df["ret"] = df.groupby("code")["close"].transform(lambda s: s.pct_change() * 100)

"""
    차트 선택 기준 (어떤 용도로 사용할 것인가?)

    - 시간에 따른 변화 -> 선 그래프(plot)
    - 범주 간 크기 비교 -> 막대 그래프(bar)
    - 하나의 분포 -> 히스토그램(hist)
    - 분포 + 이상치 -> 박스 (boxplot)
    - 두 변수의 관계 -> 산점도 (scatter)
    - 여러 변수의 상관 -> 히트맵(heatmap)
"""

# 히스토그램 => 분포 확인
fig, axes = plt.subplots(1, 2, figsize=(13,4))

#   ax.hist(값들, bins=구간수)
#     값을 bins개의 구간으로 나누어서 각 구간에 몇개의 데이터가 있는 표시
#     hist는 NaN(결측)을 만나면 범위 계산이 깨짐! -> dropna() 선행
axes[0].hist(df["ret"].dropna(), bins=60, color="steelblue")

axes[0].set_title("일간 수익률 분포")
axes[0].set_xlabel("수익률(%)")
axes[0].set_ylabel("빈도")

axes[1].hist(df["close"], bins=60, color="indianred")
axes[1].set_title("종가 분포")
axes[1].set_xlabel("종가(원)")

fig.tight_layout()
fig.savefig(out("04_hist.png"), dpi=120)
plt.close(fig)

print(f"수익률: 평균 {df['ret'].mean():.3f}%, 표준편차 {df['ret'].std():.3f}%")
print(f"종가 : 중앙값 {df['close'].median():,.0f}원, 최대값 {df['close'].max():,.0f}원")


# seaborn 으로 boxplot 그리기