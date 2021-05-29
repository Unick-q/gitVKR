from decimal import Decimal

def check_length(value, length):
    """
    Checks length of value
    @param value: value to check
    @type value: C{str}
    @param length: length checking for
    @type length: C{int}
    @return: None when check successful
    @raise ValueError: check failed
    """
    _length = len(value)
    if _length != length:
        raise ValueError("length must be %d, not %d" % \
                         (length, _length))


def check_positive(value, strict=False):
    """
    Checks if variable is positive
    @param value: value to check
    @type value: C{integer types}, C{float} or C{Decimal}
    @return: None when check successful
    @raise ValueError: check failed
    """
    if not strict and value < 0:
        raise ValueError("Value must be positive or zero, not %s" % str(value))
    if strict and value <= 0:
        raise ValueError("Value must be positive, not %s" % str(value))


def split_values(ustring, sep=u','):
    """
    Splits unicode string with separator C{sep},
    but skips escaped separator.
    
    @param ustring: string to split
    @type ustring: C{unicode}
    
    @param sep: separator (default to u',')
    @type sep: C{unicode}
    
    @return: tuple of splitted elements
    """
    assert isinstance(ustring, str), "Должно быть unicode, not %s" % type(ustring)
    ustring_marked = ustring.replace(u'\,', u'\uffff')
    items = tuple([i.strip().replace(u'\uffff', u',') for i in ustring_marked.split(sep)])
    return items

FRACTIONS = (
    (u"десятая", u"десятых", u"десятых"),
    (u"сотая", u"сотых", u"сотых"),
    (u"тысячная", u"тысячных", u"тысячных"),
    (u"десятитысячная", u"десятитысячных", u"десятитысячных"),
    (u"стотысячная", u"стотысячных", u"стотысячных"),
    (u"миллионная", u"милллионных", u"милллионных"),
    (u"десятимиллионная", u"десятимилллионных", u"десятимиллионных"),
    (u"стомиллионная", u"стомилллионных", u"стомиллионных"),
    (u"миллиардная", u"миллиардных", u"миллиардных"),
    ) 

FRACTIONS_UA = (
    (u"десята", u"десятих", u"десятих"),
    (u"сотих", u"сотих", u"сотих"),
    (u"тисячна", u"тисячних", u"тисячних"),
    (u"десятитисячна", u"десятитисячних", u"десятитисячних"),
    (u"стотисячна", u"стотисячних", u"стотисячних"),
    (u"мільйонна", u"міллліонних", u"міллліонних"),
    (u"десятимільйонна", u"десятіміллліонних", u"десятіміллліонних"),
    (u"стомільйонна", u"стоміллліонних", u"стоміллліонних"),
    (u"мільярдна", u"мільярдних", u"мільярдних"),
    ) 

ONES = {
    0: (u"",       u"",       u""),
    1: (u"один",   u"одна",   u"одно"),
    2: (u"два",    u"две",    u"два"),
    3: (u"три",    u"три",    u"три"),
    4: (u"четыре", u"четыре", u"четыре"),
    5: (u"пять",   u"пять",   u"пять"),
    6: (u"шесть",  u"шесть",  u"шесть"),
    7: (u"семь",   u"семь",   u"семь"),
    8: (u"восемь", u"восемь", u"восемь"),
    9: (u"девять", u"девять", u"девять"),
    } 

ONES_UA = {
    0: (u"",       u"",       u""),
    1: (u"один",   u"одна",   u"одне"),
    2: (u"два",    u"дві",    u"два"),
    3: (u"три",    u"три",    u"три"),
    4: (u"чотири", u"чотири", u"чотири"),
    5: (u"п'ять",   u"п'ять",   u"п'ять"),
    6: (u"шість",  u"шість",  u"шість"),
    7: (u"сім",   u"сім",   u"сім"),
    8: (u"вісім", u"вісім", u"вісім"),
    9: (u"дев'ять", u"дев'ять", u"дев'ять"),
    } 

TENS = {
    0: u"",
    10: u"десять",11: u"одиннадцать",12: u"двенадцать",13: u"тринадцать",
    14: u"четырнадцать",15: u"пятнадцать",16: u"шестнадцать",17: u"семнадцать",
    18: u"восемнадцать",19: u"девятнадцать",2: u"двадцать",3: u"тридцать",4: u"сорок",
    5: u"пятьдесят",6: u"шестьдесят",7: u"семьдесят",8: u"восемьдесят",9: u"девяносто",
    }  

TENS_UA = {
    0: u"",
    10: u"десять",11: u"одинадцять",12: u"дванадцять",13: u"тринадцять",
    14: u"чотирнадцять",15: u"п'ятнадцять",16: u"шістнадцять",17: u"сімнадцять",
    18: u"вісімнадцять",19: u"дев'ятнадцять",2: u"двадцять",3: u"тридцять",4: u"сорок",
    5: u"п'ятдесят",6: u"шістдесят",7: u"сімдесят",8: u"вісімдесят",9: u"дев'яносто",
    }  

HUNDREDS = {
    0: u"",1: u"сто",2: u"двести",3: u"триста",
    4: u"четыреста",5: u"пятьсот",6: u"шестьсот",
    7: u"семьсот",8: u"восемьсот",9: u"девятьсот",
    }  

HUNDREDS_UA = {
    0: u"",1: u"сто",2: u"двісті",3: u"триста",
    4: u"чотириста",5: u"п'ятсот",6: u"шістсот",
    7: u"сімсот",8: u"вісімсот",9: u"дев'ятсот",
    }  

MALE = 1   
FEMALE = 2  
NEUTER = 3  


def _get_float_remainder(fvalue, typeindf, signs=9):
    check_positive(fvalue)
    if isinstance(fvalue, int):
        return "0"
    if isinstance(fvalue, Decimal) and fvalue.as_tuple()[2] == 0:
        # Decimal.as_tuple() -> (sign, digit_tuple, exponent)
        # если экспонента "0" -- значит дробной части нет
        return "0"
    if typeindf == False: #Ua
        signs = min(signs, len(FRACTIONS_UA))
    elif typeindf == True: #Ru
        signs = min(signs, len(FRACTIONS))
    # нужно remainder в строке, потому что дробные X.0Y
    # будут "ломаться" до X.Y
    remainder = str(fvalue).split('.')[1]
    iremainder = int(remainder)
    orig_remainder = remainder
    factor = len(str(remainder)) - signs
    if factor > 0:
        # после запятой цифр больше чем signs, округляем
        iremainder = int(round(iremainder / (10.0**factor)))
    format = "%%0%dd" % min(len(remainder), signs)
    remainder = format % iremainder
    if len(remainder) > signs:
        # при округлении цифр вида 0.998 ругаться
        raise ValueError("Signs overflow: I can't round only fractional part \
                          of %s to fit %s in %d signs" % \
                         (str(fvalue), orig_remainder, signs))
    return remainder


def choose_plural(amount, variants): 
    if isinstance(variants, str):
        variants = split_values(variants)
    check_length(variants, 3)
    amount = abs(amount)
    if amount % 10 == 1 and amount % 100 != 11:
        variant = 0
    elif amount % 10 >= 2 and amount % 10 <= 4 and \
         (amount % 100 < 10 or amount % 100 >= 20):
        variant = 1
    else:
        variant = 2
    return variants[variant]


def money(amount, typeindf,  zero_for_kopeck=False):
    check_positive(amount)
    pts = []
    amount = round(amount, 2)
    if typeindf == False: #Ua
        pts.append(sum_string_ua(int(amount), 1, (u"гривня", u"гривні", u"гривень")))
        remainder = _get_float_remainder(amount,typeindf, 2)
        iremainder = int(remainder)
        if iremainder != 0 or zero_for_kopeck:
            # если 3.1, то это 10 копеек, а не одна
            if iremainder < 10 and len(remainder) == 1:
                iremainder *= 10
            pts.append(sum_string_ua(iremainder, 2,
                                (u"копійка", u"копійки", u"копійок")))
    elif typeindf == True: #Ru
        pts.append(sum_string(int(amount), 1, (u"рубль", u"рубля", u"рублей")))
        remainder = _get_float_remainder(amount,typeindf, 2)
        iremainder = int(remainder)
        if iremainder != 0 or zero_for_kopeck:
            # если 3.1, то это 10 копеек, а не одна
            if iremainder < 10 and len(remainder) == 1:
                iremainder *= 10
            pts.append(sum_string(iremainder, 2,
                                (u"копейка", u"копейки", u"копеек")))
    return u" ".join(pts)

def in_words_float(amount, typeindf, _gender=FEMALE):
    check_positive(amount)
    pts = []
    if typeindf == False: #Ua
        # преобразуем целую часть
        pts.append(sum_string_ua(int(amount), 2,
                            (u"ціла", u"цілих", u"цілих")))
        # теперь то, что после запятой
        remainder = _get_float_remainder(amount,typeindf)
        signs = len(str(remainder)) - 1
        pts.append(sum_string_ua(int(remainder), 2, FRACTIONS_UA[signs]))
    elif typeindf == True: #Ru
        # преобразуем целую часть
        pts.append(sum_string(int(amount), 2,
                            (u"целая", u"целых", u"целых")))
        # теперь то, что после запятой
        remainder = _get_float_remainder(amount,typeindf)
        signs = len(str(remainder)) - 1
        pts.append(sum_string(int(remainder), 2, FRACTIONS[signs]))
    else:
        raise TypeError("Что-то пошло не так")
    return u" ".join(pts)

def in_words(amount, typeindf=True, gender=None):
    check_positive(amount)
    if gender is None:
        args = (amount,)
    else:
        args = (amount, gender)
    # если дробное
    if isinstance(amount, (float, Decimal)):
        return in_words_float(*args, typeindf)
    else:
        # до сюда не должно дойти
        raise TypeError("Число должно быть не целое, получили %s" % type(amount))


def sum_string(amount, gender, items=None):
    if isinstance(items, str):
        items = split_values(items)
    if items is None:
        items = (u"", u"", u"")
    try:
        one_item, two_items, five_items = items
    except ValueError:
        raise ValueError("Цепь должна быть 3х элементная")
    check_positive(amount)
    if amount == 0:
        if five_items:
            return u"ноль %s" % five_items
        else:
            return u"ноль"
    into = u''
    tmp_val = amount
    # единицы
    into, tmp_val = _sum_string_fn(into, tmp_val, gender, items)
    # тысячи
    into, tmp_val = _sum_string_fn(into, tmp_val, FEMALE,
                                    (u"тысяча", u"тысячи", u"тысяч"))
    # миллионы
    into, tmp_val = _sum_string_fn(into, tmp_val, MALE,
                                    (u"миллион", u"миллиона", u"миллионов"))
    # миллиарды
    into, tmp_val = _sum_string_fn(into, tmp_val, MALE,
                                    (u"миллиард", u"миллиарда", u"миллиардов"))
    if tmp_val == 0:
        return into
    else:
        raise ValueError("Слишком большое число")

def sum_string_ua(amount, gender, items=None):
    if isinstance(items, str):
        items = split_values(items)
    if items is None:
        items = (u"", u"", u"")
    try:
        one_item, two_items, five_items = items
    except ValueError:
        raise ValueError("Цепь должна быть 3х элементная")
    check_positive(amount)
    if amount == 0:
        if five_items:
            return u"ноль %s" % five_items
        else:
            return u"ноль"
    into = u''
    tmp_val = amount
    # единицы
    into, tmp_val = _sum_string_fn_ua(into, tmp_val, gender, items)
    # тысячи
    into, tmp_val = _sum_string_fn_ua(into, tmp_val, FEMALE,
                                    (u"тысяча", u"тисячі", u"тысяч"))
    # миллионы
    into, tmp_val = _sum_string_fn_ua(into, tmp_val, MALE,
                                    (u"мільйон", u"мільйона", u"мільйонів"))
    # миллиарды
    into, tmp_val = _sum_string_fn_ua(into, tmp_val, MALE,
                                    (u"мільярд", u"мільярда", u"мільярдів"))
    if tmp_val == 0:
        return into
    else:
        raise ValueError("Слишком большое число")

def _sum_string_fn(into, tmp_val, gender, items=None):
    if items is None:
        items = (u"", u"", u"")
    one_item, two_items, five_items = items
    check_positive(tmp_val)
    if tmp_val == 0:
        return into, tmp_val
    words = []
    rest = tmp_val % 1000
    tmp_val = tmp_val // 1000
    if rest == 0:
        # последние три знака нулевые
        if into == u"":
            into = u"%s " % five_items
        return into, tmp_val
    # начинаем подсчет с rest
    end_word = five_items
    # сотни
    words.append(HUNDREDS[rest // 100])
    # десятки
    rest = rest % 100
    rest1 = rest // 10
    # особый случай -- tens=1
    tens = rest1 == 1 and TENS[rest] or TENS[rest1]
    words.append(tens)
    # единицы
    if rest1 < 1 or rest1 > 1:
        amount = rest % 10
        end_word = choose_plural(amount, items)
        words.append(ONES[amount][gender-1])
    words.append(end_word)
    # добавляем то, что уже было
    words.append(into)
    # убираем пустые подстроки
    words = filter(lambda x: len(x) > 0, words)
    # склеиваем и отдаем
    return u" ".join(words).strip(), tmp_val


def _sum_string_fn_ua(into, tmp_val, gender, items=None):
    if items is None:
        items = (u"", u"", u"")
    one_item, two_items, five_items = items
    check_positive(tmp_val)
    if tmp_val == 0:
        return into, tmp_val
    words = []
    rest = tmp_val % 1000
    tmp_val = tmp_val // 1000
    if rest == 0:
        # последние три знака нулевые
        if into == u"":
            into = u"%s " % five_items
        return into, tmp_val
    # начинаем подсчет с rest
    end_word = five_items
    # сотни
    words.append(HUNDREDS_UA[rest // 100])
    # десятки
    rest = rest % 100
    rest1 = rest // 10
    # особый случай -- tens=1
    tens = rest1 == 1 and TENS_UA[rest] or TENS_UA[rest1]
    words.append(tens)
    # единицы
    if rest1 < 1 or rest1 > 1:
        amount = rest % 10
        end_word = choose_plural(amount, items)
        words.append(ONES_UA[amount][gender-1])
    words.append(end_word)
    # добавляем то, что уже было
    words.append(into)
    # убираем пустые подстроки
    words = filter(lambda x: len(x) > 0, words)
    # склеиваем и отдаем
    return u" ".join(words).strip(), tmp_val


print(in_words(1.5,typeindf = False))
print(in_words(5.30000,typeindf = True))
print(money(15,typeindf = True))
print(money(15,typeindf = False))
