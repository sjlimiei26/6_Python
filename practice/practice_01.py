"""
1. 이름, 성별, 나이, 키를 입력받은 후 정보를 출력하는 프로그램
   - 출력 형식: `이름: xxx, 성별: xx, 나이: xx, 키: xx.xxcm`
"""
name = input("이름 입력: ")
gender = input("성별(M/F) 입력: ")
age = input("나이 입력: ")
height = float(input("키 입력: "))

print()
# print(f"이름: {name}, 성별: {gender}, 나이: {age}, 키: {height:.1f}cm")
print(f"이름: {name}, 성별: {'남' if gender == 'M' else '여'}, 나이: {age}, 키: {height:.1f}cm")


"""
### 2. 소문자를 대문자로 변환하여 출력하는 프로그램
- 영문 소문자를 입력받아 대문자로 변환하여 출력하세요.
- Tip: 
  - `ord()` : 문자 -> 아스키 코드값
  - `chr()` : 아스키 코드값 -> 문자
  - `upper()` : 대문자 변환
"""

lower_alpha = input("영문 소문자를 입력하세요: ")
print()

# 직접 계산하는 방법
ascii_alpha = ord(lower_alpha)
upper_alpha = chr(ascii_alpha - 32)

print(f"소문자: {lower_alpha}")
print(f"대문자: {upper_alpha}")

# 함수 사용하는 방법
print(f"대문자: {lower_alpha.upper()}")

"""
### 3. 정수 두 개를 입력받아 산술 연산 결과를 출력하는 프로그램
- 합, 차, 곱, 몫, 나머지를 계산하여 출력하세요.
"""
n1 = int(input("첫 번째 정수를 입력하세요: "))
n2 = int(input("두 번째 정수를 입력하세요: "))
print()

print(f"합: {n1 + n2}")
print(f"차: {n1 - n2}")
print(f"곱: {n1 * n2}")
print(f"몫: {n1 // n2}")
print(f"나머지: {n1 % n2}")

"""
### 4. 두 정수를 입력받아 제곱과 제곱근을 출력하는 프로그램
- 첫 번째 입력받은 정수의 제곱을 출력
- 두 번째 입력받은 정수의 제곱근을 출력
  - 제곱근: 어떤 수를 제곱하여 주어진 수가 되는 수 (예: 4의 제곱근은 2, -2)
"""
n1 = int(input("첫 번째 정수를 입력하세요: "))
n2 = int(input("두 번째 정수를 입력하세요: "))
print()

print(f"{n1}의 제곱: {n1 ** 2}")
print(f"{n2}의 제곱근: {int(n2 ** 0.5)}")

"""
### 5. 학점 산출 프로그램
- 키보드로 정수를 입력받아 정해진 점수 기준에 따라 학점을 출력하세요.

#### 점수 기준
- 90점 이상 : A
- 80점 이상 : B
- 70점 이상 : C
- 60점 이상 : D
- 60점 미만 : F
"""

score = int(input("점수를 입력하세요(0-100): "))

if score < 0 or score > 100:
  print("점수를 올바르게 입력해주세요.")
else:
  if score >= 90:
    print("학점: A")
  elif score >= 80:
    print("학점: B")
  elif score >= 70:
    print("학점: C")
  elif score >= 60:
    print("학점: D")
  else:
    print("학점: F")

"""
### 6. 1부터 100까지의 숫자 중에서 짝수만 출력하는 프로그램
"""

for i in range(1, 101):
  if i % 2 != 0: 
    continue
  print(i)
  # print(i, end=' ')

"""
### 7. 1부터 100까지의 숫자 중에서 "3의 배수"이고 "5의 배수가 아닌 수"의 합을 구하여 출력하는 프로그램
"""

total = 0
for n in range(1, 101):
  if n % 3 != 0 or n % 5 == 0:
    continue
  total += n

print("1부터 100까지의 숫자 중 3의 배수이고 5의 배수가 아닌 수의 합")
print(f"결과: {total}")
