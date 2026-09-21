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