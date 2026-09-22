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
# ==========================================
# 과제 1 TODO 코드 템플릿
# ==========================================

# TODO 1-1: 'Department' 컬럼의 결측치를 '미지정' 문자열로 대체하세요.
df_clean_dep = df.copy()
df_clean_dep["Department"] = df_clean_dep["Department"].fillna("미지정")

# 그래프 크기 설정
fig, axes= plt.subplots(2,2, figsize=(17,9))
# plt.figure(figsize=(10, 5))

# TODO 1-2: 부서별 트래픽 건수를 Countplot으로 그리세요. (순서 정렬 고려)
# order 파라미터에 value_counts().index를 전달하면 빈도순 정렬이 가능합니다.
ax1 = axes[0, 0]
sns.countplot(
    data=df_clean_dep,
    x="Department",
    order=df_clean_dep["Department"].value_counts().index.tolist(),
    palette=sns.color_palette("pastel"),
    ax=ax1
)

# 그래프 타이틀 및 라벨링
ax1.set_title(
    "[주간 리뷰] 부서별 네트워크 트래픽 발생 건수 (미지정 항목 포함)",
    fontsize=14,
    pad=15,
)
ax1.set_xlabel("부서명", fontsize=12)
ax1.set_ylabel("트래픽 발생 건수 (회)", fontsize=12)

# 막대 상단에 수치 표시 (Hint: ax.containers)
for container in ax1.containers:
    ax1.bar_label(container, fmt="%d", padding=3)

# ==========================================
# 과제 2 TODO 코드 템플릿
# ==========================================

# TODO 2: x축은 'Session_Count', y축은 'Traffic_GB', 구분(hue)은 'Traffic_Type'으로 산점도를 그리세요.
ax2 = axes[0,1]
sns.scatterplot(
    data=df,
    x="Session_Count",
    y="Traffic_GB",
    hue="Traffic_Type",
    style="Traffic_Type",
    s=100,  # 점 크기
    alpha=0.8,
    palette={"Inbound": "#2ecc71", "Outbound": "#e74c3c"},
    ax=ax2
)

# 이상치 강조를 위한 임계선(Threshold) 표시 (예: Traffic_GB > 350)
ax2.axhline(
    y=350, color="red", linestyle="--", linewidth=1.5, label="위험 트래픽 임계치"
)

ax2.set_title(
    "[보안 모니터링] 세션 수 대비 트래픽 전송량 이상 징후 (Outbound 폭증 식별)",
    fontsize=14,
    pad=15,
)
ax2.set_xlabel("접속 세션 수 (Session Count)", fontsize=12)
ax2.set_ylabel("트래픽 용량 (Traffic GB)", fontsize=12)
ax2.legend(title="트래픽 유형", loc="upper left")

# ==========================================
# 과제 3 TODO 코드 템플릿
# ==========================================

# TODO 3: x축은 'Protocol', y축은 'Response_Time_MS'로 박스플롯을 생성하세요.
ax3 = axes[1,0]
sns.boxplot(
    data=df,
    x="Protocol",
    y="Response_Time_MS",
    palette="Set2",
    fliersize=8,  # 이상치 점 크기
    flierprops={"markerfacecolor": "red", "marker": "D"},  # 이상치 빨간 다이아몬드 표시
    ax=ax3
)

ax3.set_title(
    "[성능 모니터링] 프로토콜별 응답 시간(Response Time) 분포 및 지연 병목 현황",
    fontsize=14,
    pad=15,
)
ax3.set_xlabel("프로토콜 유형", fontsize=12)
ax3.set_ylabel("응답 시간 (ms)", fontsize=12)

# ==========================================
# 과제 4 TODO 코드 템플릿
# ==========================================

# TODO 4-1: 부서(Department)와 프로토콜(Protocol) 기준 Traffic_GB의 평균(mean) 피벗 테이블을 작성하세요.
# (Tip: 결측 부서는 dropna=True로 자동 제외하거나 사전에 처리하세요)
pivot_df = df.pivot_table(
    index="Department", columns="Protocol", values="Traffic_GB", aggfunc="mean"
)

# TODO 4-2: 생성한 pivot_df를 활용해 히트맵을 생성하세요.
ax4 = axes[1,1]
sns.heatmap(
    data=pivot_df,
    annot=True,  # 셀 내부 수치 표시
    fmt=".1f",  # 소수점 첫째 자리까지 표시
    cmap="YlGnBu",  # 색상 팔레트
    linewidths=0.5,  # 셀 간 격자선
    cbar_kws={"label": "평균 트래픽 (GB)"},
    ax=ax4
)

ax4.set_title(
    "[경영진 보고] 부서 x 프로토콜별 평균 네트워크 트래픽 소비 매트릭스",
    fontsize=14,
    pad=15,
)
ax4.set_xlabel("프로토콜", fontsize=12)
ax4.set_ylabel("부서명", fontsize=12)

fig.suptitle("네트워크 트래픽 분석 보드")
fig.tight_layout()
fig.savefig("p06_traffic_summary.png", dpi=120)