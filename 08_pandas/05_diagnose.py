"""
    점검하기

    데이터 정제 전에 데이터가 정상인지 여부를 확인하는 단계(방법)
"""
import pandas as pd

from utils.config import RAW_PATH, ENCODING

# 옵션 없이 그대로 데이터 읽어오기
df = pd.read_csv(RAW_PATH, encoding=ENCODING)

print(f"- 형태(행/열) : {df.shape} / {df.shape[0]}행 {df.shape[1]}열")

print(f"- 상위 3개 데이터 조회 :\n{df.head(3)}")
print(f"- 열별 데이터 타입 확인 :\n{df.dtypes}")

"""
    close, volume 은 숫자(int)여야하는데 문자열(str)로 확인됨!

    read_csv 는 열마다 타입을 추론하는데,
    한 열에 숫자가 아닌 값이 '하나라도' 존재하면 그 열은 전체가 문자열로 판단됨!
"""
print(" === 현재 상태에서 통계 조회 === ")
print(df[['close', 'volume', 'high', 'low']].describe())
# int64 타입인 'high', 'low' 정상적으로 값이 출력
# str 타입인 'close', 'volume' 값이 출력되지 않음!

# df.info()  : 행 수, 열 이름, non-null 개수, dtype 을 출력
df.info()
# non-null 개수를 통해, 전체 행수와 다르면 결측이 있다고 판단!


# 결측률
#    df.isnull() / df.isna()

na = df.isnull().sum()
print(f"{'열':<14}{'결측 수':<14}{'비율':<14}")
for col in df.columns:
    if na[col] > 0:
        print(f"{col:<14} {na[col]:<14}{na[col]/len(df)*100:>9.2f}")

# read_csv 는 일부 문자열에 대해서 알아서 결측으로 변경해줌
#  데이터에 N/A 라고 되어있는 값을 읽을 때 NaN이 됨. 다른 문자들은 전부 결측처리가 되지 않음!

# * keep_default_na=False => 파일에 저장된 데이터를 그대로 읽어옴
# * dtype=str => 모든 열을 문자열로 읽어옴
# ---> "N/A" 값을 자동으로 Nan으로 처리했던 작업을 하지 않고, 문자열 그대로 읽어옴
df2 = pd.read_csv(RAW_PATH, encoding=ENCODING,
                        keep_default_na=False, dtype=str)
print(f"{'열':<14}{'N/A':>10}{'-':>10}{'빈칸':>10}")
for col in ['close', 'volume']:
    na_cnt = (df2[col] == 'N/A').sum()
    dash_cnt = (df2[col] == '-').sum()
    blank_cnt = (df2[col] == '').sum()

    print(f"{col:<14}{na_cnt:>10}{dash_cnt:>10}{blank_cnt:>10}")

# 동일한 데이터가 오염되어 있어도 N/A은 결측으로 확인이 되는데, 
#    오염된 데이터가 확실하게 확인하기가 어려움!
# 데이터를 읽어올 때 결측으로 판단할 값들을 지정할 수 있음!
#  => na_values=['N/A', '-', ''] 옵션을 통해 결측 처리를 할 수 있음!!
print('-' * 60)

# * value_counts()  : 어떤 값이 몇 번 나오는 지 확인
#   - dropna=False  : 결측치(NaN)도 하나의 값으로 처리

print(df['close'].value_counts(dropna=False).head())
# 종가(close) 데이터는 value_counts() 결과를 본다기 보단
#   오염된 데이터를 찾고자 할 때 이 방식으로 확인이 가능! (dropna=False)
print('-' * 60)


# * to_numeric(errors="coerce")  : 숫자로 변경이 불가능한 값에 대해 오류 대신 NaN으로 처리
for col in ['close', 'volume']:
    na_result = pd.to_numeric(df2[col], errors="coerce").isna().sum()
    print(f"{col:<10} : {na_result:>6}건")
# 콤마(,)가 포함된 데이터도 숫자로 변경 불가능한 데이터에 포함됨!
print('-' * 60)

# 데이터 중복 확인
#    duplicated(subset=[기준열, 기준열, ...])
#    => 원본 길이와 같은 결과를 반환 (True/False)
#    => 첫번째 값은 False, 두번째부터 True

dup = df.duplicated(subset=['code', 'date']).sum()
print(f" (code, date) 중복건수 : {dup}")
print(f" 중복 제거 후 개수 : {len(df) - dup}")

print('-' * 60)

# 날짜 형식
#   --> 현재 실습 데이터에는 3가지 형식 존재

# 글자 수 : .str.len()
lens = df['date'].astype(str).str.len().value_counts()
# print(lens)
# 2026-09-18, 2026.09.18 --> 10글자
# 20260918  --> 8글자
print(f"20260918 형식 : {lens.get(8, 0)}")

# 패턴 검색 : .str.contains()
dot_cnt = df['date'].astype(str).str.contains(r"\.", regex=True).sum()
print(f"2026.09.18 형식 : {dot_cnt}건")

print(f"2026-09-18 형식 : {lens.get(10, 0) - dot_cnt}건")


temp = df.copy()
temp['date'] = pd.to_datetime(temp['date'], format='mixed')
# temp.info()
dup2 = temp.duplicated(subset=['code', 'date']).sum()
print(f"날짜 데이터 변환 후 중복 건수 : {dup2}")

print(f" 날짜 형식 차이로 숨겨진 중복 : {dup2 - dup}")
# G0001, 2026-09-18
# G0001, 20260918

print('-' * 60)

temps = pd.DataFrame({
    'code': ['G0001', 'G0001', 'G0002'],
    'date': ['2026-09-18', '20260918', '2026-09-18'],
    'close': [24000, 24000, 28800]
})
print(temps)
print(f"문자열인 상태에서 중복 : {temps.duplicated(subset=['code', 'date']).sum()}건")

temps['date'] = pd.to_datetime(temps['date'], format='mixed')
print(f"날짜타입으로 변환 후 중복 : {temps.duplicated(subset=['code', 'date']).sum()}건")


# 어떤 데이터가 문제가 있는 지 진단
#     => 타입 -> 중복 -> 결측 -> 이상치 -> 검증

# 데이터 정제 목표 정하기.
print(f"{'항목':<24} {'현재':<14} {'목표':<14}")
print("=" * 60)
print(f"{'행수':<24} {len(df):<14} {'90,000':<14}")
print(f"{'종목수':<24} {df['code'].nunique():<14} {'120':<14}")
print(f"{'종목별 행수(최소~최대)':<18}"
      f"{str( df.groupby('code').size().min() ) + '~' + str( df.groupby('code').size().max()):<14} {'750':<14}")