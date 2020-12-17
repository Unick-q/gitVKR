age = input('Введите возраст человека в годах: ')

if   age[1] in '1':    print(age, 'год')
elif age in ['11','12','13','14','15','16','17','18','19']: print(age, 'лет')
elif age[1] in '234':  print(age, 'года')
else : print(age, 'лет')
