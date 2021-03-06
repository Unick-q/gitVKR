# -*- coding: utf-8 -*-
import decimal
import sys
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
# добавить дату для порядковых 
units = (
    u'ноль',
    (u'один', u'одна', u'одно'),
    (u'два', u'две'),
    u'три', u'четыре', u'пять',
    u'шесть', u'семь', u'восемь', u'девять'
)

units_ordinals = (
    u'нулевой',
    u'первый', u'второй',
    u'третий', u'четвертый', u'пятый',
    u'шестой', u'седьмой', u'восьмой', u'девятый'
)

teens = (
    u'десять', u'одиннадцать',
    u'двенадцать', u'тринадцать',
    u'четырнадцать', u'пятнадцать',
    u'шестнадцать', u'семнадцать',
    u'восемнадцать', u'девятнадцать'
)

teens_ordinals = (
    u'десятый', u'одиннадцатый',
    u'двенадцатый', u'тринадцатый',
    u'четырнадцатый', u'пятнадцатый',
    u'шестнадацатый', u'семнадцатый',
    u'восемнадцатый', u'девятнадцатый'
)

tens = (
    teens,
    u'двадцать', u'тридцать',
    u'сорок', u'пятьдесят',
    u'шестьдесят', u'семьдесят',
    u'восемьдесят', u'девяносто'
)

tens_ordinals = (
    teens,
    u'двадцатый', u'тридцатый',
    u'сороковой', u'пятидесятый',
    u'шестидесятый', u'семидесятый',
    u'восьмидесятый', u'девяностый'
)

hundreds = (
    u'сто', u'двести',
    u'триста', u'четыреста',
    u'пятьсот', u'шестьсот',
    u'семьсот', u'восемьсот',
    u'девятьсот'
)

hundreds_ordinals = (
    u'сотый', u'двухсотый',
    u'трёхсотый', u'четырёхсотый',
    u'пятисотый', u'шестисотый',
    u'семисотый', u'восмисотый',
    u'девятисотый'
)

orders = (# plural forms and gender
    #((u'', u'', u''), 'm'), 
    ((u'тысяча', u'тысячи', u'тысяч'), 'f'),
    ((u'миллион', u'миллиона', u'миллионов'), 'm'),
    ((u'миллиард', u'миллиарда', u'миллиардов'), 'm'),
)

orders_ordinals = (# plural forms and gender
    #((u'', u'', u''), 'm'), 
    u'тысячный', u'двухтысячный',
    u'трёхтысячный', u'четырёхсотый',
    u'пятисотый', u'шестисотый',
    u'семисотый', u'восмисотый',
    u'девятисотый'
)


minus = u'минус'

# def convert(rest, lm, sex):
def convert(rest, sex):
    "Converts numbers from 19 to 999"
    prev = 0
    plural = 2
    name = []
    use_teens = rest % 100 >= 10 and rest % 100 <= 19 # проверка метки 
    if not use_teens:
        data = ((units, 10), (tens, 100), (hundreds, 1000))
    else:
        data = ((teens, 10), (hundreds, 1000))
    for names, x in data:
        cur = int(((rest - prev) % x) * 10 / x)
        # print(cur)
        prev = rest % x
        if x == 10 and use_teens:
            plural = 2
            name.append(teens[cur])
        elif cur == 0:
            continue
        elif x == 10:
            name_ = names[cur]
            if isinstance(name_, tuple):
                # print(name_)
                # print(tuple)
                name_ = name_[0 if sex == 'm' else 1]
                print('name_ is',name_)
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

# def int_n2t(num, lam, main_units=((u'', u'', u''), 'm')):
def int_n2t(num, main_units=((u'', u'', u''), 'm')): 
    "Converts int numbers to text"
    _orders = (main_units,) + orders
    if num == 0:
        return ' '.join((units[0], _orders[0][0][2])).strip() # ноль

    rest = abs(num)
    ord = 0
    name = []
    while rest > 0:
        plural, nme  = convert(rest % 1000, _orders[ord][1]) 
        # print(plural)
        # plural, nme, tmp = convert(rest % 1000, lam, _orders[ord][1])
        if nme or ord == 0:
            name.append(_orders[ord][0][plural])
            # print(_orders[ord][0][plural])
            # print('Name is',name)
        name += nme
        rest = int(rest / 1000)
        ord += 1
    if num < 0:
        name.append(minus)
    name.reverse()
    return ' '.join(name).strip()


# def float_n2t(value, places=2, int_units=(('', '', ''), 'f'), exp_units=(('', '', ''), 'm')):
    "Converts float numbers to text"
    value = decimal.Decimal(value)
    q = decimal.Decimal(10) ** -places

    integral, exp = str(value.quantize(q)).split('.')
    return u'{} {}'.format(
        int_n2t(int(integral), int_units),
        int_n2t(int(exp), exp_units))

# def make_unicode(input):
#     if type(input) != unicode:
#         input =  input.decode('utf-8')
#         return input
#     else:
#         return input

# def get_number_and_noun(numeral, lam, noun):
def get_number_and_noun(numeral, noun):
    morph = pymorphy2.MorphAnalyzer()
    elem = morph.parse(noun)[0]
    ##############################
    # value_num = decimal.Decimal(numeral)
    # l = decimal.Decimal(10) ** -2
    # f_part, s_part = str(value_num.quantize(l)).split('.')
    v1, v2, v3 = elem.inflect({'sing', 'nomn'}), elem.inflect({'gent'}), elem.inflect({'plur', 'gent'})
    #uv1, uv2, uv3 = elem.inflect({'sing', 'nomn'}), elem.inflect({'plur', 'nomn'}), elem.inflect({'plur', 'gent'})
    try:
        # if '.' in numeral:
        #     print('The result is ------ ',float_n2t(decimal.Decimal(numeral),
        #     int_units=((elem.make_agree_with_number(f_part), elem.make_agree_with_number(f_part), elem.make_agree_with_number(f_part)), 'f'),
        #     exp_units=((elem.make_agree_with_number(s_part), elem.make_agree_with_number(s_part), elem.make_agree_with_number(s_part)), 'm')))
        # else:
           return int_n2t(int(numeral), main_units=((v1.word, v2.word, v3.word), 'm')) #добавляем метку для порядковых 
        #    return int_n2t(int(numeral), lam, main_units=((v1.word, v2.word, v3.word), 'm'))
        #else:
        #   print('The result is ------ ',int_n2t(int(numeral),main_units=((uv1.word, uv2.word, uv3.word), 'm', 1)))
    except ValueError:
        print ('Error: Invalid argument!')
    sys.exit() 


# butyavka = morph.parse('сто пятдесят первый')[0]
# print(butyavka.lexeme)
# gent = butyavka.inflect({'sing', 'nomn','gent'})
# print(gent.word)

print("Input your number")
inpt_num = input()
# print("Ordianl number or not?")
# print("1 -- Yes, it's ordinal")
# print("2 -- No, it's normal numeral")
# lmbd = int(input())
# if (lmbd != 1) & (lmbd != 2):
#     print(" Error ") 
#     sys.exit() 
print("Input your noun")
inpt_str = str(input())
str_res = get_number_and_noun(inpt_num, morph.parse(inpt_str)[0].normal_form)
# str_res = get_number_and_noun(inpt_num, lmdb, morph.parse(inpt_str)[0].normal_form)  
print('The result is ------ ',str_res)

# print(morph.parse('пользователи')[0].normal_form)
