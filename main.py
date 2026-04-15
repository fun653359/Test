from datetime import date
class 학생:
    def __init__(self,name,age,school_number,birth):
        self.name = name
        self.age=age
        self.school_number=school_number
        self.birth = birth
    def introduce(self):
        print(f"안녕하세요 {self.name}입니다 나이는 {self.age}이고 학번은 {self.school_number} 이고 생일은 {self.birth}입니다")
    def school(self):
        return date.today().weekday() < 5


class birth(학생):
    def __init__(self,name,age,school_number,birth):
        self.name = name
        self.age=age
        self.school_number=school_number
        self.birth = birth
    def find_birth(self,day):
        if day == self.birth:
            print("생신축하드려요")
        else:
            print("생신이 아니네요...아쉬워요")
a = 학생("홍정현",17,10621,"5050")
'''if __name__ == "__main__":'''

b = birth("홍정현",17,10621,"5050")
a.introduce()
b.find_birth("5050")