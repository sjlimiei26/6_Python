# 2026-09-22 
#  ==  AI를 활용한 데이터 분석 연습 ==
#  - 주제: [e커머스 플랫폼] 무신사 의류 카테고리별 매출 및 리뷰 분석


# ===========================
#       차트 기본 설정
# ===========================
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# 한글 깨짐 방지 폰트 설정 (OS별 자동 구분)
import platform

if platform.system() == "Darwin":  # Mac OS
    plt.rc("font", family="AppleGothic")
elif platform.system() == "Windows":  # Windows
    plt.rc("font", family="Malgun Gothic")

# 마이너스 기호 깨짐 방지
plt.rcParams["axes.unicode_minus"] = False

# Seaborn 스타일 설정
sns.set_theme(style="whitegrid", font=plt.rcParams["font.family"])

# 데이터 로드
df = pd.read_csv("business_data.csv")

# =========================================
#            문제 풀이
# =========================================
"""
    [과제 1] 카테고리별 볼륨 및 데이터 결측 점검
    비즈니스 질문: "우리 플랫폼에서 가장 주문 건수가 많은 카테고리는 무엇이며, 
                   데이터 수집 누락(결측치)이 발생한 카테고리가 있는가?"
"""
# TODO: 결측치 개수 확인 (isnull().sum() 활용)
print("=== 컬럼별 결측치 현황 ===")
# print(df.______)
print(df.isnull().sum())
print("데이터 수집 누락(결측치) 카테고리 x")

# TODO: 카테고리별 거래 건수(Countplot) 시각화
"""
plt.figure(figsize=(9, 5))
# ax = sns.countplot(data=df, x='______', palette='Blues_d', order=df['category'].value_counts().index)
ax = sns.countplot(data=df, x='category', palette='Blues_d', order=df['category'].value_counts().index)

plt.title("카테고리별 전체 주문 건수 분포", fontsize=14, fontweight="bold")
plt.xlabel("카테고리")
plt.ylabel("주문 건수(건)")

# 그래프 상단에 숫자 라벨 달아주기 (옵션)
# for p in ax.patches:
#     ax.annotate(f'{int(p.get_height())}건', (p.get_x() + p.get_width() / 2., p.get_height()),
#                 ha='center', va='center', xytext=(0, 5), textcoords='offset points')

plt.tight_layout()
plt.show()
"""

fig, ax = plt.subplots(figsize=(9,5))
sns.countplot(data=df, x='category', palette='Blues_d', order=df['category'].value_counts().index, ax=ax)

ax.set_title("카테고리별 전체 주문 건수 분포")
ax.set_xlabel("카테고리")
ax.set_ylabel("주문 건수(건)")

fig.savefig("p06_countplot.png", dpi=120)
plt.close(fig)