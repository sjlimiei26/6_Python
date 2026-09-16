"""
    결측과 이상치
"""
import numpy as np
from load_utils import load_dirty

arr, nan_idx, outlier_idx = load_dirty()

print(f"===== np.nan =====")
print(f"np.nan == np.nan ? {np.nan == np.nan}")  # 자신과 비교했을 때 False
print(f"np.nan != np.nan ? {np.nan != np.nan}")
print(f"np.nan > 1 ? {np.nan > 1}")
print(f"np.nan < 1 ? {np.nan < 1}")
print(f"np.nan + 1 ? {np.nan + 1}")

# nan 뜻 자체가 Not a Number 이므로
#  "모르는 값"이랑 "모르는 값" 을 비교하거나 연산을 수행했을 때 결과를 알 수 없음!

result = (arr == np.nan)
print(f" arr == np.nan : {result.sum()}")
# 동등 비교로 결측치를 찾을 수 없음!!

result = np.isnan(arr)
# print(result)
print(f" 총 개수: {len(arr)} / 결측 : {result.sum()}")
print(f" 결측치의 위치 : {np.where(result)[0]}")

print(f" 평균 : {np.mean(arr)}  -> {np.nanmean(arr):.2f}")
print()

for name, f1, f2 in [
    ("mean", np.mean, np.nanmean),
    ("sum", np.sum, np.nansum),
    ("std", np.std, np.nanstd),
    ("max", np.max, np.nanmax),
    ("min", np.min, np.nanmin)
]:
    r1 = f1(arr)
    r2 = f2(arr)

    print(f"{name} f1: {r1} f2: {r2}")

"""
    [결측치 해결방법]

    1. 전용 함수 사용 (np.nanXXXX)
    2. 결측치 제거   arr[~np.isnan(arr)] # nan 이 아닌 값만 추출
    3. 결측치를 다른 값으로 대체   arr[np.isnan(arr)] = np.nanmean(arr) # 평균으로 채우기
"""