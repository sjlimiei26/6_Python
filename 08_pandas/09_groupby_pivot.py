"""
    groupby
    => split -> apply -> combine
        * split : 특정 열(키)을 기준으로 쪼갬
        * apply : 각 그룹에 함수를 적용
        * combine : 결과를 하나로 합침
    pivot
"""
import pandas as pd

from utils.loader import load_merged

df = load_merged()
print(f"통합 데이터 : {len(df)}행 / {df['code'].nunique()} 종목 / {df['sector'].nunique()} 섹터")
# agg      : 요약표를 만들 때 그룹 별로 결과를 도출
# transform: 원본에 열을 추가해서 값을 비교하고자 할 때 
#            그룹별로 계산 결과를 원본과 동일하게 도출
# filter   : 그룹 별로 검사해서 조건에 맞지 않으면 제외

# 종목 코드가 "G0001", "G0002"인 데이터만 추출하여 two 변수에 저장
two = df[ df["code"].isin(["G0001", "G0002"]) ].reset_index(drop=True)
print( two[["code", "date", "close"]].head(6) )

# diff() : 바로 위 행과의 차이를 반환
#    s.diff()  -> s[i] - s[i-1], 맨 첫행은 NaN

wrong = two["close"].diff()
right = two.groupby("code")["close"].diff()

# shift() : 열을 통째로 한 칸 아래로 밀어줌
#    s.shift()  -> 원본과 길이가 같은 Series 를 반환
#                  i번째 값 = s[i-1], 맨 첫 행은 NaN
boundary = two.index[ two['code'] != two['code'].shift() ][1]
# print(boundary[1])
#  [0] -> 첫 행. 이전 데이터가 없으므로 True
#  경계 지점은 [1] 위치가 될 것임!
print(f"종목이 바뀌는 지점: {boundary}")

for i in range(boundary - 2, boundary + 2):
    w = f"{wrong[i] if pd.notna(wrong[i]) else 'NaN'}"
    r = f"{right[i]}" if pd.notna(right[i]) else "NaN"

    print(f"{i:<8} {two.loc[i, 'code']:<9} {two.loc[i, 'close']:<12} {w:>20} {r:>20}")

print("=" * 60)

count_num = df.groupby("sector")["code"].count()
nunique_num = df.groupby("sector")["code"].nunique()

print(f"count : {count_num}")
print(f"nunique : {nunique_num}")

"""
    한 종목이 750행이면, count : 750, nunique : 1
"""

# agg : 요약표
summary = df.groupby("sector").agg(
                종목수=("code", "nunique"),
                거래일수=("date", "count"),
                평균종가=("close", "mean"),
                최대거래량=("volume", "max")
            )

print(summary.round(0))
print('-' * 60)

# filter : 그룹 단위로 걸러내줌. 조건을 만족하는 그룹 전체를 남겨줌!

# 거래일이 700일 미만인 종목 제외
filtered = df.groupby("code").filter(lambda g: len(g) >= 700)
print(f" {len(df)}행 {df['code'].nunique()}종목 ")
print(f" -> {len(filtered)}행 {filtered['code'].nunique()}종목 ")
# 전 종목이 750일 데이터가 존재해서, 걸러지는 게 없음!

# g["close"].mean() -> 750일의 종목 평균
#  종목 평균이 100,000 이하인 종목을 제외
big = df.groupby('code').filter(lambda g: g['close'].mean() > 100_000)
print(f"{len(big)}행  {big['code'].nunique()}종목")
"""
    filter를 사용하면 특정 행이 아니라, 그룹 전체를 남기거나 버림!

    df[df['close'] > 100_000] => 조건에 맞는 행만 남김!
"""
print("=" * 60)

# 다중 그룹, MultiIndex
multi = df.groupby(["sector", "market"])["close"].mean()
print(f" 인덱스 타입 : {type(multi.index).__name__}")
print(multi.head(6).round(0))
# 여러 개(n)의 열을 기준으로 그룹화를 하면, 인덱스가 n개인 시리즈로 반환됨!

print("인덱스의 첫번째 레벨로 조회 (sector)")
print(multi.loc['금융'].round(0))

print("인덱스의 모든 레벨을 지정 -> 튜플로 전달")
print(multi.loc[('금융', 'GX-GROWTH')])
print()

# unstack()  : 인덱스를 열로 펼침
print(multi.unstack().head(4).round(0))
# => 인덱스의 안쪽 레벨 값을 열로 올림
print()

# reset_index()  : 인덱스를 열로 되돌림. 
print(multi.reset_index().head(3).round(0))
# => 인덱스 값이 열이 되고, 인덱스는 0,1,2,... 으로 새로 만들어짐.

# groupby(..., as_index=False) : 처음부터 그룹화기준이 열로 나옴.
flat = df.groupby(['sector', 'market'], as_index=False)['close'].mean()
print(flat.columns.tolist())

print("=" * 60)

# 피벗 - 형식 바꾸기
"""
    pivot_table  : 한 열은 행으로, 다른 열을 열로 펼쳐서 집계

    df.pivot_table(index=행_기준_열, columns=열_기준_열, values=집계대상_열, aggfunc=집계함수)
"""
d = df.copy()

# 분기 정보 추가
d['quarter'] = d['date'].dt.to_period("Q").astype(str)
# - to_period()  : 날짜를 기간으로 변경 (Q: 분기, M: 월, Y: 연)

pv = d.pivot_table(
    index="sector",         # 행
    columns="quarter",      # 열
    values="close",         # 셀 데이터 (연산대상)
    aggfunc="mean"          # 셀 데이터 집계 함수
)
print(pv.iloc[:5, :4].round(0))
print("=" * 60)

# 넓은 형식 , 긴 형식
wide = pv.iloc[:3, :3]
print("== 넓은 형식 ==")
print(wide.round())   # 사람이 보기 편함

# melt : 넓은 형식을 긴 형식으로 녹여서 표현
#    df.melt(id_vars=유지할_열, var_name=열이름을_담을_열, value_name=값을_담을_열)
#    => 열마다 흩어져 있는 값을 하나의 열에 모으기 위함
long = wide.reset_index().melt(id_vars="sector", var_name="quarter", value_name="close")
print("== 긴 형식 ==")
print(long.head(6).round())
# DB 저장, 시각화할 때 활용

# 피봇 -> 사람이 보는 보고서, 엑셀, 데이터 확인 시 활용

back = long.pivot(index="sector", columns="quarter", values="close")
print(back.round())