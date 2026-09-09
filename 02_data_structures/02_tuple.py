"""
    튜플 (tuple)
"""

# 튜플을 생성하는 방법 -> ()
point = (10, 20)
point2 = 50, 60

single = (10,)  # 데이터가 1개일 때 콤마 필수!
single2 = (10)  # 콤마가 없으면 튜플이 아님!

print(f"point : {point} {type(point)}")
print(f"point2 : {point2} {type(point2)}")
print(f"single : {single} {type(single)}")
print(f"single2 : {single2} {type(single2)}")
print()

print(f"point[0] : {point[0]}") # 인덱스 접근은 가능!
# point[0] = 99     # 수정이 불가 (불변성)

point = (99, 20)
print(f"point 자체를 변경 : {point}")
# 새로운 튜플 할당은 가능
print()

# 언패킹
x, y = (2, 6)
print(f"x, y : {x}, {y}")

def get_numbers():
    return 77, 44

x, y = get_numbers()
print(f"x, y : {x}, {y}")
print()

# 튜플 내에서 불필요한 값을 무시 => _ 사용
x, _, z= (10, 20, 30)
print(f"{x} {z}")

# 첫번째 값만 변수에 저장하고 나머지는 따로 처리 => * 사용
x, *rest = (1,2,3,4,5)
print(f"x: {x}, rest: {rest}")      # 나머지 데이터는 리스트 형태로 패킹

"""
    튜플        |  리스트
    불변        |  가변
    ()          |  []
    딕셔너리 키 o| 딕셔너리 키 x
"""
locations = {
    (35.5451, 126.9750): "서울역",
    (30.5401, 124.9050): "부산역"
}