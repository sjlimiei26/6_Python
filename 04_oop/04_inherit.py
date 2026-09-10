"""
    상속과 다형성
"""

class Account:
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            print("잔액이 부족합니다.")
            return

        self.balance -= amount
        return amount

    def info(self):
        return f"[{self.owner}] 잔액 : {self.balance:,}원"

# 상속 -> class 클래스명(부모클래스명):
#   super() 부모 클래스(객체)

class SavingsAccount(Account):
    def __init__(self, owner, balance = 0, rate = 0.03):
        super().__init__(owner, balance)        # 부모 생성자 호출
        self.rate = rate

    def add_interest(self):
        interest = int(self.balance * self.rate)
        self.balance += interest
        return interest

    def info(self):         # 메소드 오버라이딩 (재정의)
        return f"{super().info()} / 이율 {self.rate}"

sa = SavingsAccount("짱구", 10000)
print(f"info: {sa.info()}")

print(f"이자 지급: {sa.add_interest()}원")
print(f"info: {sa.info()}")
print()


class CheckingAccount(Account):
    FEE = 500

    # 생성자를 정의하지 않을 것임! 
    #   Account(부모타입) 생성자를 기준으로 생성할 수 있게 됨

    def withdraw(self, amount):
        total = amount + self.FEE

        if total > self.balance:
            print("잔액이 부족합니다.")
            return

        self.balance -= total
        return amount

    def info(self):
        return f"{super().info()} / 수수료 : {self.FEE}원"


acc_list = [
    Account("하리보", 2000),
    SavingsAccount("마이구미", 15000),
    CheckingAccount("박카스", 8000)
]

for acc in acc_list:
    print(f"{acc.info()}")

# 덕 타이핑.. (Duck Typing) -- 오리처럼 행동하면 오리다...
#   상속 관계가 없어도 같은 메소드를 가지면 동일하게 취급