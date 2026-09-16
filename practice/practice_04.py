"""
    Numpy 연습문제
"""

# =========== 이곳에 필요한 모듈 import 한 후 실행 ===========
import numpy as np
from load_utils import load_one_stock, load_dates, load_matrix

"""
    1. 다음 리스트 [1, 2, 3, 4, 5]를 ndarray로 변환하고, 배열의 차원(ndim)과 형태(shape)을 출력하시오.
"""
print("========= Q1 =========")
arr = np.array([1,2,3,4,5])
print(f"배열의 차원: {arr.ndim}")
print(f"배열의 형태: {arr.shape}")


"""
    2. np.arange()를 이용해 0부터 20까지의 짝수로 이루어진 배열을 생성하시오.
"""
print("========= Q2 =========")
arr = np.arange(0, 21, 2)
print("짝수 배열 (0~20)")
print(arr)


"""
    3. 다음 제시된 리스트를 배열로 변환한 후, 3 이상인 값만 추출하는 불리언 인덱싱 코드를 작성하시오.
"""
print("========= Q3 =========")
list3 = [1,3,5,2,8,3]
arr = np.array(list3)

print("3 이상인 값")
print(arr[arr >= 3])


"""
    4. 다음 제시된 리스트를 배열로 변환한 후, 두 번째 행만 슬라이싱하여 출력하시오.
"""
print("========= Q4 ========")
list4 = [[10, 20, 30], [40, 50, 60], [70, 80, 90]]

arr = np.array(list4)
print("두 번째 행")
# === 인덱싱 ===
print(arr[1])          # 결과가 1차원 배열

# == 슬라이싱 ==
print(arr[1:2:1])      # 결과가 2차원 배열
print(arr[1:2][0:3:1])
print(arr[1:2, 0:3:1])
print(arr[1:2])

"""
    5. 다음 제시된 리스트를 배열로 변환한 후, 모든 홀수에만 10을 더하는 벡터화 연산을 수행하시오.
"""
print("========= Q5 ========")
list5 = [1, 2, 3, 4, 5]

arr = np.array(list5)
print("홀수에 10 더한 배열")
# === 불리언 인덱싱 방식 ===
arr[arr % 2 == 1] += 10
print(arr)

# === np.where 사용 ======
arr = np.where(arr % 2 == 1, arr + 10, arr)
print(arr)

"""
    6. 다음 제시된 실수 리스트를 배열로 변환한 후, 반올림한 정수형 배열로 변환하시오.
        주의 : astype 만 쓰면 소수점 아래가 버려져서 값이 새어나간다.

        [출력 예시]
            np.array([52000.9, -3.7]) -> [52001, -4]

        [힌트] 반올림을 먼저 하고 타입을 바꾼다. 순서가 중요하다.
"""
print("========= Q6 ========")
list6 = [52000.9, 51999.2, -3.7, 52000.5]

arr = np.array(list6)
round_arr = np.round(arr).astype(int)
print(round_arr)

# =========== 아래 문제들은 실습용 데이터(prices.csv, load_utils.py)를 활용하여 풀이해보세요. =========== 
prices = load_one_stock(0)
dates = load_dates()
stocks = load_matrix()
"""
    7. 첫 종목의 종가 데이터를 기준으로 최저가, 최고가와 그에 해당하는 날짜를 각각 출력하시오. 
       (실습용 데이터의 prices 와 dates 는 길이와 순서가 같다.)

        [출력 예시]
            (25899, numpy.datetime64('2023-10-16'), 8885, numpy.datetime64('2026-05-21'))

        [힌트] max 는 '값', argmax 는 '그 값이 있는 위치' 다.
              위치를 얻으면 길이가 같은 다른 배열에서 같은 자리를 꺼낼 수 있다.
"""
print("========= Q7 =========")

max_idx = prices.argmax()
min_idx = prices.argmin()

print(f"({prices[max_idx]}, {dates[max_idx]}, {prices[min_idx]}, {dates[min_idx]})")


"""
    8. 종가 데이터를 기준으로 각 종목별 평균가와, 날짜별 평균가를 구하시오. 
       또한, 각 종목에서 자기 평균을 뺀 배열을 구하시오.
       
       [힌트]
       - 종목별 평균가 : (종목 수,) 배열 
       
       - 날짜별 평균가 : (날짜 수,) 배열
       
       - 각 종목에서 자기 평균을 뺀 배열 : (종목 수, 날짜 수) 배열 
         결과의 종목별 평균은 0 이 되어야 한다.
"""
print("========= Q8 =========")

mean_by_stock = stocks.mean(axis=1)
print(f"종목별 평균가 : {mean_by_stock.shape} \n{mean_by_stock}")
mean_by_date = stocks.mean(axis=0)
print(f"날짜별 평균가 : {mean_by_date.shape} \n{mean_by_date}")
diff_by_stock = stocks - mean_by_stock[:, np.newaxis]
print(f"자기 평균을 뺀 배열 : {diff_by_stock.shape} \n{diff_by_stock}")