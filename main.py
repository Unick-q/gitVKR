import constant


def getNumber():
    while True:
        getNum = input('Введите целое положительное число: ')  # перевели строку в int
        if getNum.isdigit() : return getNum
#print(int(getNumber()))

unitNumber = {
    '1': UNUS,
    '2','3','4': SMALL,
    '0','5','6','7','8','9': BIG2,
}

if getNumber()):
    if (int(getNumber()) % 100) / 10 == 1:
        scl = BIG2
    elif (getNumber() % 10) in unitNumber:
        num = unitNumber[etNumber()]
else 
    i = 0
    


#print(constant.MAXUNUS)
#print(constant.MAXSMALL)
#print(constant.MAXBIG1)
