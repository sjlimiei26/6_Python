"""
    시계열 데이터
    : 시간의 흐름에 따라 분포된 데이터 (시간, 수치/데이터)
"""
import pandas as pd
from utils.loader import load_merged

pd.set_option("display.width", 140)

df = load_merged()

# one 변수에 G0001 종목 데이터만 저장
one = df[df['code'] == 'G0001']
print(f"one index : {one.index}")

# 날짜 데이터를 인덱스로 사용
#   set_index(인덱스열) : 지정한 열이 인덱스가 되어 새로운 DF 반환
# one.info()
one = one.set_index('date').sort_index()
print(f"인덱스 변경 후 one index : {one.index}")

print(f" 기간 : {one.index.min().date()} ~ {one.index.max().date()}")

# 문자열로 날짜 조회 가능!
#   2026년 3월 전체 데이터 조회
print(f"26년 3월 전체 : {len( one.loc['2026-03'] )}행")
print(f"26년 1월 ~ 6월 전체 : {len( one.loc['2026-01':'2026-06'] )}행")
# 날짜 인덱스로 슬라이싱 할 때는, 이전에 정렬이 되어있어야 함! (sort_index())
print('-' * 60)

# dt 접근자
#   날짜 함수, 연/월/일 같은 조각을 꺼낼 때 사용

d = df.head(3)
print(f"연도 : {d['date'].dt.year.tolist()}")
print(f"분기 : {d['date'].dt.quarter.tolist()}")
print(f"요일 : {d['date'].dt.dayofweek.tolist()} (0: 월, ..., 6: 일)")

print(f"연월로 변경 : {d['date'].dt.to_period('M').astype(str).tolist()}")

dow = df['date'].dt.dayofweek.value_counts().sort_index()
for k, v in dow.items():
    print(f" {'월화수목금토일'[k]}요일 {v:,}건 ")


# resample  : 시간 단위로 바꿔서 다시 묶어줌
#   df.resample(시간단위).집계함수
#   => 시간 단위만큼의 행을 가진 결과. 뒤에 추가한 집계함수가 값을 정해줌.
#      --> 시간 기준으로 groupby
#   * 시간 단위 : D(일), W(주), ME(월말), QE(분기말), YE(연말)

monthly_last = one['close'].resample('ME').last()
monthly_mean = one['close'].resample('ME').mean()
monthly_vol = one['volume'].resample('ME').sum()

print(f"{'월':<12} {'월말종가':<16} {'월평균가':<16}")
for idx in monthly_last.index[:4]:
    print(f"{idx.strftime('%Y-%m'):<12} {monthly_last[idx]:>16.0f} {monthly_mean[idx]:>16.0f}")

print(f"월별 거래량 : {monthly_vol.iloc[0]:,.0f}")

# * resample("ME").ohlc()
#   ohlc : Open(시가) High(고가) Low(저가) Close(종가)
# => 기간별 시가,고가,저가,종가 네개열을 한번에 만들수있음
print(one['close'].resample('ME').ohlc().head(3).round(0))
print("=" * 60)

# rolling : 연속된 N개 행을 윈도우 단위로 훑으면서 계산
#    이동 평균처럼 최근 N일의 데이터가 필요할 때 사용
df = df.sort_values(['code', 'date']).reset_index(drop=True)

wrong = df['close'].rolling(20).mean()
right = df.groupby('code')['close'].transform(lambda s: s.rolling(20).mean())

edge = df.index[ df['code'] != df['code'].shift() ][1]
for i in [edge-1, edge, edge+1]:
    w = f"{wrong[i]:,.0f}" if pd.notna(wrong[i]) else "NaN"
    r = f"{right[i]:,.0f}" if pd.notna(right[i]) else "NaN"

    print(f" {i:<8} {df.loc[i, 'code']:<9} {df.loc[i, 'close']:>10,} {w:>20} {r:>20}")

"""
    groupby 없이 계산하면 (wrong) 종목별 코드가 달라도 이평선 재계산없이 이어지는 형태도 계산됨
    그룹화를 해줘야 종목별 20일 이평선이 정상적으로 계산됨

    diff, shift, rolling... 모두 groupby가 필요함!
"""
print("=" * 60)

# 변화율 계산
#   pct_change : 바로 위행대비 비율 변화
#   cumprod : 누적곱
#      s.cumprod() => s[0], s[0]*s[1], s[0]*s[1]*s[2], ...

df['ret'] = df.groupby('code')['close'].transform(lambda s: s.pct_change())

sample = df[df['code'] == 'G0001'].head(4)
for _, r in sample.iterrows():
    ret = f"{r['ret']:.4f}" if pd.notna(r['ret']) else 'NaN'
    print(f"{r['date'].date()} {r['close']:,} {ret}")

# 누적 수익률 
#  => 첫 날의 NaN을 0으로 채우고, (1+수익률)을 차례로 곱하기
cum = (1+df[df['code'] == 'G0001']['ret'].fillna(0)).cumprod().iloc[-1]
print(f"G0001 종목의 누적 수익률: {(cum - 1) * 100:.1f}%")