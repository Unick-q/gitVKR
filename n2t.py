import decimal
import sys
import pymorphy2

units = (
    u'ноль',
    (u'один', u'одна'),
    (u'два', u'две'),
    u'три', u'четыре', u'пять',
    u'шесть', u'семь', u'восемь', u'девять'
)

teens = (
    u'десять', u'одиннадцать',
    u'двенадцать', u'тринадцать',
    u'четырнадцать', u'пятнадцать',
    u'шестнадцать', u'семнадцать',
    u'восемнадцать', u'девятнадцать'
)

tens = (
    teens,
    u'двадцать', u'тридцать',
    u'сорок', u'пятьдесят',
    u'шестьдесят', u'семьдесят',
    u'восемьдесят', u'девяносто'
)

hundreds = (
    u'сто', u'двести',
    u'триста', u'четыреста',
    u'пятьсот', u'шестьсот',
    u'семьсот', u'восемьсот',
    u'девятьсот'
)

orders = (# plural forms and gender
    #((u'', u'', u''), 'm'), 
    ((u'тысяча', u'тысячи', u'тысяч'), 'f'),
    ((u'миллион', u'миллиона', u'миллионов'), 'm'),
    ((u'миллиард', u'миллиарда', u'миллиардов'), 'm'),
)

minus = u'минус'

def convert(rest, sex):
    "Converts numbers from 19 to 999"
    prev = 0
    plural = 2
    name = []
    use_teens = rest % 100 >= 10 and rest % 100 <= 19
    if not use_teens:
        data = ((units, 10), (tens, 100), (hundreds, 1000))
    else:
        data = ((teens, 10), (hundreds, 1000))
    for names, x in data:
        cur = int(((rest - prev) % x) * 10 / x)
        prev = rest % x
        if x == 10 and use_teens:
            plural = 2
            name.append(teens[cur])
        elif cur == 0:
            continue
        elif x == 10:
            name_ = names[cur]
            if isinstance(name_, tuple):
                name_ = name_[0 if sex == 'm' else 1]
            name.append(name_)
            if cur >= 2 and cur <= 4:
                plural = 1
            elif cur == 1:
                plural = 0
            else:
                plural = 2
        else:
            name.append(names[cur-1])
    return plural, name


def int_num2text(num, main_units=((u'', u'', u''), 'm')):
    "Converts int numbers to text"
    _orders = (main_units,) + orders
    if num == 0:
        return ' '.join((units[0], _orders[0][0][2])).strip() # ноль

    rest = abs(num)
    ord = 0
    name = []
    while rest > 0:
        plural, nme = convert(rest % 1000, _orders[ord][1])
        if nme or ord == 0:
            name.append(_orders[ord][0][plural])
        name += nme
        rest = int(rest / 1000)
        ord += 1
    if num < 0:
        name.append(minus)
    name.reverse()
    return ' '.join(name).strip()


def float_num2text(value, places=2, int_units=(('', '', ''), 'f'), exp_units=(('', '', ''), 'm')):
    "Converts float numbers to text"
    value = decimal.Decimal(value)
    q = decimal.Decimal(10) ** -places

    integral, exp = str(value.quantize(q)).split('.')
    return u'{} {}'.format(
        int_num2text(int(integral), int_units),
        int_num2text(int(exp), exp_units))
  
def get_number_and_noun(numeral, noun):
    morph = pymorphy2.MorphAnalyzer()
    elem = morph.parse(noun)[0]
    value_num = decimal.Decimal(numeral)
    l = decimal.Decimal(10) ** -2
    f_part, s_part = str(value_num.quantize(l)).split('.')
    #print(f_part) #5
    #print(elem.make_agree_with_number(f_part)) #????? Не выдаёт числительное в правильном падеже
    #print(s_part) #50
    #nmrl = int(numeral)
    #print('qqq1')
    #print(nmrl)
    #print(elem.make_agree_with_number(nmrl))
    v1, v2, v3 = elem.inflect({'sing', 'nomn'}), elem.inflect({'gent'}), elem.inflect({'plur', 'gent'})
    try:
        if '.' in numeral:
            print('The result is ------ ',float_num2text(decimal.Decimal(numeral),
            int_units=((elem.make_agree_with_number(f_part), elem.make_agree_with_number(f_part), elem.make_agree_with_number(f_part)), 'f'),
            exp_units=((elem.make_agree_with_number(s_part), elem.make_agree_with_number(s_part), elem.make_agree_with_number(s_part)), 'm')))
        else:
           print('The result is ------ ',int_num2text(int(numeral),main_units=((v1.word, v2.word, v3.word), 'm')))
    except ValueError:
        print ('Error: Invalid argument ')
    sys.exit() 

print("Input your number")
inpt_num = input()
print("Input your noun")
inpt_str = input()
get_number_and_noun(inpt_num, inpt_str)  

#elem.make_agree_with_number(numeral)