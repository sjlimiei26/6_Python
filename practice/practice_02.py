"""
### 1. 몸무게(kg)와 키(cm)를 입력받아 BMI 지수를 계산하는 함수를 정의
- BMI = 몸무게(kg) / (키(m) * 키(m))
- 키는 cm로 입력받아 m로 변환
- 반올림 함수: `round(숫자, 자릿수)`
"""
# 함수 정의
def calc_bmi():
    w = float(input("몸무게를 입력하세요(kg): "))
    h = float(input("키를 입력하세요(cm): "))
    
    h_m = h / 100
    bmi = w / (h_m * h_m)
    
    print(f"BMI: {round(bmi, 2)}")

# 함수 호출
calc_bmi()


"""
### 2. 여러 개의 숫자를 입력받아 평균을 계산하는 함수를 정의
- 사용자가 'q'를 입력할 때까지 숫자를 계속 입력받음 (입력받는 개수는 정해져 있지 않음)
- 평균 = 총합 / 총개수
"""

# 함수 정의
def calc_average():
    print("========== 평균 계산기 ==========")

    numbers = []
    while True:
        num = input("숫자 입력 (q 입력 시 종료) : ")

        if num == "q":
            break
        numbers.append(int(num))
    
    if len(numbers) == 0:
        print("---> 값이 없습니다.")
    else:
        total = sum(numbers)
        avg = total / len(numbers)
        print(f"---> 평균: {round(avg, 2)}")

# 함수 호출
# calc_average()


"""
### 3. 단어 빈도수 분석 함수 정의
- 문장(문자열)을 입력받아 공백 단위로 단어를 분리하고, 각 단어의 등장 횟수를 딕셔너리로 계산하여 반환
- 대소문자를 구분하지 않도록 모든 문자를 소문자로 변환하여 처리
- 소문자 변환: `.lower()`
- 문자열 분리: `.split()`
"""

def count_word_frequency(text):
    words = text.lower().split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

# data = "Python is fun and Python is powerful"
data = input("문장을 입력하세요: ")
print()

result_freq = count_word_frequency(data)
print("[단어 빈도수 결과]")
for word, count in result_freq.items():
    print(f"- {word}: {count}회")


"""
### 4. 로또 번호 자동 생성 함수 정의
- 1부터 45 사이의 서로 다른 무작위 숫자 6개를 생성한 후 오름차순으로 정렬하여 반환
- 구매할 게임 수를 입력받아 해당 횟수만큼 로또 번호 세트를 출력
- 정렬: `sorted()`
- 난수: `import random` 후 `random.randint(1, 45)` 활용
"""
import random

def generate_lotto():
    lottos = set()

    while len(lottos) < 6:
        lottos.add(random.randint(1, 45))

    return sorted(list(lottos))

game_count = int(input("구매할 로또 게임 수를 입력하세요: "))
print()
print("[로또 번호 발급 결과]")

for i in range(1, game_count + 1):
    print(f"{i}게임: {generate_lotto()}")


"""
### 5. 학생 성적 통계 분석 함수 정의
- 학생들의 이름과 점수가 담긴 딕셔너리를 전달받아 최고 득점자, 최저 득점자, 전체 평균 점수를 계산하여 반환
- 반환값은 `((최고득점자, 점수), (최저득점자, 점수), 평균점수)` 형태로 반환
- 함수 호출 후 반환값을 튜플 언패킹(Unpacking)으로 받아 결과 출력
- 데이터 예시:
```python
{
    "홍길동": 85,
    "이순신": 96,
    "강감찬": 72,
    "유관순": 91
}
```
"""

def analyze_scores(scores):
    if not scores:
        return None, None, 0.0
    
    # 최고 득점자 및 최저 득점자 계산
    max_student = max(scores.items(), key=lambda x: x[1])
    min_student = min(scores.items(), key=lambda x: x[1])
    avg_score = sum(scores.values()) / len(scores)
    
    return max_student, min_student, round(avg_score, 2)

student_scores = {
    "홍길동": 85,
    "이순신": 96,
    "강감찬": 72,
    "유관순": 91
}
top_scorer, low_scorer, average = analyze_scores(student_scores)

print("========== 학생 성적 분석 결과 ==========")
print(f"- 최고 득점자: {top_scorer[0]} ({top_scorer[1]}점)")
print(f"- 최저 득점자: {low_scorer[0]} ({low_scorer[1]}점)")
print(f"- 전체 평균: {average}점")
