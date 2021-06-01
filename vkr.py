import sys
import math
import re
import pymorphy2
from decimal import Decimal
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

morph = pymorphy2.MorphAnalyzer(lang='ru')
morph_ua = pymorphy2.MorphAnalyzer(lang='uk')

nth = {
    0: "ой",
    1: "ый",
    2: "ой",
    3: "ий",
    4: "ый",
    5: "ый",
    6: "ой",
    7: "ой",
    8: "ой",
    9: "ый"
}

nth_ua = {
    0: "ий",
    1: "ий",
    2: "ий",
    3: "ій",
    4: "ий",
    5: "ий",
    6: "ий",
    7: "ий",
    8: "ий",
    9: "ий"
}

ordinal = dict(
    ty="ый",
    ноль="нулевой",один="первый",два="второй",три="третий",четыре="четвертый",шесть="шестой",семь="седьмой",восемь="восьмой",
    сорок="сороковой", пятьдесят="пятидесятый", шестьдесят="шестидесятый",семьдесят="семидесятый",восемьдесят="восьмидесятый",девяносто="девяностый",
    сто="сотый", двести="двухсотый",триста="трёхсотый", четыреста="четырёхсотый",пятьсот="пятисотый", шестьсот="шестисотый",семьсот="семисотый", восемьсот="восмисотый",девятьсот="девятисотый",
    тысяча="тысячный",миллион="миллиoнный",миллиард="миллиaрдный",триллион="триллиoнный",квадриллион="квaдриллионный",квинтиллион="квинтиллиoнный"
)

ordinal_ua = {
    "ty":"ий",
    "нуль":"нульовий","один":"перший","два":"другий","три":"третій","чотири":"четвертий","шість":"шостий","сім":"сьомий","вісім":"восьмий",
    "сорок":"сороковий","сімдесят":"семидесятий","вісімдесят":"восьмидесятих",
    "сто":"сотий","двісті":"двохсотий","триста":"трьохсот","чотириста":"чотирьохсотий","п'ятсот":"п'ятисотий","шістсот":"шестисотий","сімсот":"семисотий","вісімсот":"восмісотий","дев'ятсот":"дев'ятисотий",
    "тисяча":"тисячний","мільйон":"мілліoнний","мільярд":"мілліaрдний","трильйон":"трілліoнний","квадрильйон":"квaдрілліонний","квінтильйон":"квінтілліoнний"
}

ordinal_tens = dict(
    тысяча="тысячный",миллион="миллиoнный",миллиард="миллиaрдный",триллион="триллиoнный",квадриллион="квaдриллионный",квинтиллион="квинтиллиoнный"
)

ordinal_tens_ua = dict(
    тисяча="тисячний", мільйон="мілліoнний", мільярд="мілліaрдний",трильйон ="трілліoнний",квадрильйон="квaдрілліонний",квінтильйон="квінтілліoнний"
)

ordinal_suff = "|".join(list(ordinal.keys()))
ordinal_suff_ua = "|".join(list(ordinal_ua.keys()))

to_inflect = ["gent","datv","accs","ablt","loct"]
inflect_str = ["Родительный","Дательный","Винительный","Творительный","Предложный (на)"]
inflect_str_ua = ["Родовий","Давальний","Знахідний","Орудний","Місцевий (на)"]

# NUMBERS
(u'один', u'одна', u'одно')
(u'два', u'две')

digits = [2,3,4,5]
unit = ["", "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять"]
unit_ua = ["", "один", "два", "три", "чотири", "п'ять", "шість", "сім", "вісім", "дев'ять"]
unit_cardinal = ["", "одна", "две", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять"]
unit_cardinal_ua = ["", "одна", "дві", "три", "чотири", "п'ять", "шість", "сім", "вісім", "дев'ять"]
unit_coll = ["", "двое", "трое", "четверо", "пятеро", "шестеро", "семеро", "восьмеро", "девятеро", "десятеро"]
unit_coll_ua = ["", "двоє", "троє", "четверо", "п'ятеро", "шестеро", "семеро", "восьмеро", "дев'ятеро", "десятеро"]

uncount_num = ["сколько","сколько-нибудь","сколько-то","несколько","столько","столько-то","мало","много"]
sck = ["сколько""сколька","скольку","сколько","скольком","скольке"]
sck_nbd = ["сколько-нибудя","сколько-нибудю","сколько-нибудя","сколько-нибудём","сколько-нибуде"]
scl_to = ["сколько-то","сколько-то","сколько-то","сколько-то","сколько-то"]
nsck = ["нескольких","нескольким","несколько","несколькими","нескольких"]
stck = ["столька","стольку","столько","стольком","стольке"]
stck_to = ["столько-то","столько-то","столько-то","столько-то","столько-то"]
malo = ["нет варианта","нет варианта","мало","нет варианта","нет варианта"]
mnogo = ["многих","многим","много","многими","многих"]
# добавить!!!
uncount_num_ua = ["скільки","декілька","небагато","кілька","стільки","стільки-то","мало","багато"]
sck_ua = ["скілько́х","скілько́м","скі́льки","скількома́","скілько́х"]
dekil_ua = ["декількох","декільком","декілька","декількома","декількох"]
nemnogo_ua = ["небагатьо́х","небагатьо́м","небага́то","небагатьма́","небагатьо́х"]
nsck_ua = ["кілько́х","кілько́м","кі́лька","кількома́","кілько́х"]
stck_ua = ["стільки","стількох","стільки","стільком","стількома"]
stck_to_ua = ["стілько́х-то","стілько́м-то","сті́льки-то","стількома́-то","стілько́х-то"]
malo_ua = ["немає варіанта","немає варіанта","мало","немає варіанта","немає варіанта"]
mnogo_ua = ["багатьох","багатьом","багато","багатьма","багатьох"]

teen = ["десять",
    "одиннадцать","двенадцать","тринадцать",
    "четырнадцать","пятнадцать","шестнадцать",
    "семнадцать","восемнадцать","девятнадцать",
]

teen_ua = ["десять",
    "одинадцять","дванадцять","тринадцять",
    "чотирнадцять","п'ятнадцять","шістнадцять",
    "сімнадцять","вісімнадцять","дев'ятнадцять",
]

ten = [
    "",
    "","двадцать","тридцать",
    "сорок","пятьдесят","шестьдесят",
    "семьдесят","восемьдесят","девяносто",
]

ten_ua = [
    "",
    "","двадцять","тридцять",
    "сорок","п'ятдесят","шістдесят",
    "сімдесят","вісімдесят","дев'яносто",
]

hundred = [
    "","сто","двести","триста","четыреста","пятьсот","шестьсот","семьсот","восемьсот","девятьсот",
]

hundred_ua = [
    "","сто","двісті","триста","чотириста","п'ятсот","шістсот","сімсот","вісімсот","дев'ятсот",
]

mill = [
    ""," тысяча"," миллион"," миллиард"," триллион"," квадриллион"," квинтиллион"
]

mill_ua = [
    ""," тисяча"," мільйон"," мільярд"," трильйон"," квадрильйон"," квінтильйон"
]

only_plur = [
    "окуляри","двері","гроші","лапки","вила","ковзани","сани","терези","куранти"
    ,"вершки","консерви","діти","копалини","сутінки","заробітки","шахи","шашки"
]

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

class BadChunkingOptionError(Exception):
    pass

class NumOutOfRangeError(Exception):
    pass

class Application(QWidget):
    class ru_engine:
        def ordinal(self, num):
            """
            Возвращает порядковый номер числа.
            порядковый ('один') возвращает 'первый'
            """
            if re.match(r"\d", str(num)):
                try:
                    num % 2
                    n = num
                except TypeError:
                    if "." in str(num):
                        try:
                            n = int(num[-1])

                        except ValueError: 
                            n = int(num[:-1])
                    else:
                        n = int(num)
                try:
                    post = nth[n % 100]
                except KeyError:
                    post = nth[n % 10]
                return "{}{}".format(num, post)
            else:
                mo = re.search(r"(%s)\Z" % ordinal_suff, num)
                try:
                    post = ordinal[mo.group(1)]
                    return re.sub(r"(%s)\Z" % ordinal_suff, post, num)
                except AttributeError:
                    return "%sый" % num

        def millfn(self, ind=0):
            if ind > len(mill) - 1:
                self.exit_text.setText("Заданное число превосходит допустимое значение")
                raise NumOutOfRangeError
            return mill[ind]

        def unitfn(self, units, mindex=0):
            return "{}{}".format(unit[units], self.millfn(mindex))

        def tenfn(self, tens, units, mindex=0):
            if tens != 1:
                return "{}{}{}{}".format(
                    ten[tens],
                    " ",
                    unit[units],
                    self.millfn(mindex),
                )
            return "{}{}".format(teen[units], mill[mindex])

        def hundfn(self, hundreds, tens, units, mindex):
            if hundreds:
                # andword = " %s " % self.number_args["andword"] if tens or units else ""
                return "{}{}{}{} ".format(
                    hundred[hundreds], 
                    " ",
                    self.tenfn(tens, units),
                    self.millfn(mindex)
                )
            if tens or units:
                return "{}{} ".format(self.tenfn(tens, units), self.millfn(mindex))
            return ""

        def group1sub(self, mo):
            units = int(mo.group(1))
            if units == 1:
                return " %s, " % self.number_args["one"]
            elif units:
                return "%s, " % unit[units]
            else:
                return " %s, " % self.number_args["zero"]

        def group1bsub(self, mo):
            units = int(mo.group(1))
            if units:
                return "%s, " % unit[units]
            else:
                return " %s, " % self.number_args["zero"]

        def group2sub(self, mo):
            tens = int(mo.group(1))
            units = int(mo.group(2))
            if tens:
                return "%s, " % self.tenfn(tens, units)
            if units:
                return " {} {} ".format(self.number_args["zero"], unit[units])
            return " {} {} ".format(self.number_args["zero"], self.number_args["zero"])

        def group3sub(self, mo):
            hundreds = int(mo.group(1))
            tens = int(mo.group(2))
            units = int(mo.group(3))
            if hundreds == 1:
                hunword = " %s" % self.number_args["one"]
            elif hundreds:
                hunword = "%s" % unit[hundreds]
            else:
                hunword = " %s" % self.number_args["zero"]
            if tens:
                tenword = self.tenfn(tens, units)
            elif units:
                tenword = " {} {}".format(self.number_args["zero"], unit[units])
            else:
                tenword = " {} {}".format(
                    self.number_args["zero"], self.number_args["zero"]
                )
            return "{} {} ".format(hunword, tenword)

        def hundsub(self, mo):
            ret = self.hundfn(
                int(mo.group(1)), int(mo.group(2)), int(mo.group(3)), self.mill_count
            )
            self.mill_count += 1
            return ret

        def tensub(self, mo):
            return "%s " % self.tenfn(int(mo.group(1)), int(mo.group(2)), self.mill_count)

        def unitsub(self, mo):
            return "%s " % self.unitfn(int(mo.group(1)), self.mill_count)

        def enword(self, num, group):

            if group == 1:
                num = re.sub(r"(\d)", self.group1sub, num)
            elif group == 2:
                num = re.sub(r"(\d)(\d)", self.group2sub, num)
                num = re.sub(r"(\d)", self.group1bsub, num, 1)
            elif group == 3:
                num = re.sub(r"(\d)(\d)(\d)", self.group3sub, num)
                num = re.sub(r"(\d)(\d)", self.group2sub, num, 1)
                num = re.sub(r"(\d)", self.group1sub, num, 1)
            elif int(num) == 0:
                num = self.number_args["zero"]
            elif int(num) == 1:
                num = self.number_args["one"]
            else:
                num = num.lstrip().lstrip("0")
                self.mill_count = 0
                mo = re.search(r"(\d)(\d)(\d)(?=\D*\Z)", num)
                while mo:
                    num = re.sub(r"(\d)(\d)(\d)(?=\D*\Z)", self.hundsub, num, 1)
                    mo = re.search(r"(\d)(\d)(\d)(?=\D*\Z)", num)
                num = re.sub(r"(\d)(\d)(?=\D*\Z)", self.tensub, num, 1)
                num = re.sub(r"(\d)(?=\D*\Z)", self.unitsub, num, 1)
            return num

        def blankfn(self, mo):
            """глобальная пустая замена
            """
            return ""

        def commafn(self, mo):
            """глобальная ',' замена
            """
            return ","

        def spacefn(self, mo):
            """глобальная ' ' замена
            """
            return " "

        def number_to_words(
            self,
            num,
            wantlist=False,
            group=0,
            comma="",
            andword="",
            zero="ноль",
            one="один",
            decimal="целых",
            threshold=None,
        ):
            """
            Вернёт число прописью.
            group = 1, 2 или 3 для группировки чисел перед преобразованием в слова
            запятая: определить запятую
            andword: слово для «и». Может быть установлен на "".
                например "сто и один" vs "сто один"
            ноль: слово для '0'
            один: слово для "1"
            десятичный: слово для десятичной точки
            порог: числа выше порога не превращаются в слова
            параметры не запоминаются из последнего вызова.
            """
            self.number_args = dict(andword=andword, zero=zero, one=one)
            num = "%s" % num

            # Обработка "стилистических" преобразований (до заданного порога)
            if threshold is not None and float(num) > threshold:
                spnum = num.split(".", 1)
                while comma:
                    (spnum[0], n) = re.subn(r"(\d)(\d{3}(?:,|\Z))", r"\1,\2", spnum[0])
                    if n == 0:
                        break
                try:
                    return "{}.{}".format(spnum[0], spnum[1])
                except IndexError:
                    return "%s" % spnum[0]

            if group < 0 or group > 3:
                raise BadChunkingOptionError
            nowhite = num.lstrip()
            if nowhite[0] == "+":
                sign = "плюс"
            elif nowhite[0] == "-":
                sign = "минус"
            else:
                sign = ""

            myord = num[-2:] in ("ый", "ой", "ий")
            if myord:
                num = num[:-2]
            finalpoint = False
            if decimal:
                if group != 0:
                    chunks = num.split(".")
                else:
                    chunks = num.split(".", 1)
                if chunks[-1] == "":  # удаляем пустую строку, если после десятичной дроби ничего нет
                    chunks = chunks[:-1]
                    finalpoint = True  # добавляем точку в конце вывода 
            else:
                chunks = [num]

            first = 1
            loopstart = 0

            if chunks[0] == "":
                first = 0
                if len(chunks) > 1:
                    loopstart = 1

            for i in range(loopstart, len(chunks)):
                chunk = chunks[i]
                # убираем все \D
                chunk = re.sub(r"\D", self.blankfn, chunk)
                if chunk == "":
                    chunk = "0"

                if group == 0 and (first == 0 or first == ""):
                    chunk = self.enword(chunk, 1)
                else:
                    chunk = self.enword(chunk, group)

                if chunk[-2:] == ", ": 
                    chunk = chunk[:-2]
                chunk = re.sub(r"\s+,", self.commafn, chunk)

                if group == 0 and first:
                    chunk = re.sub(r", (\S+)\s+\Z", " %s \\1" % andword, chunk)
                chunk = re.sub(r"\s+", self.spacefn, chunk)
                # chunk = re.sub(r"(\A\s|\s\Z)", self.blankfn, chunk)
                chunk = chunk.strip()
                if first:
                    first = ""
                chunks[i] = chunk

            numchunks = []
            if first != 0:
                numchunks = chunks[0].split("%s " % comma)


            if myord and numchunks:
                mo = re.search(r"(%s)\Z" % ordinal_suff, numchunks[-1])
                result = []
                if mo:
                    numchunks[-1] = re.sub(
                        r"(%s)\Z" % ordinal_suff, ordinal[mo.group(1)], numchunks[-1]
                    )
                else:
                    numchunks[-1] = re.sub(r"ь","",numchunks[-1])
                    numchunks[-1] += "ый"

            for chunk in chunks[1:]:
                numchunks.append(decimal)
                numchunks.extend(chunk.split("%s " % comma))

            if finalpoint:
                numchunks.append(decimal)

            if wantlist:
                if sign:
                    numchunks = [sign] + numchunks
                return numchunks
            elif group:
                signout = "%s " % sign if sign else ""
                return "{}{}".format(signout, " ".join(numchunks))
            else:
                signout = "%s " % sign if sign else ""
                num = "{}{}".format(signout, numchunks.pop(0))
                if decimal is None:
                    first = True
                else:
                    first = not num.endswith(decimal)
                for nc in numchunks:
                    if nc == decimal:
                        num += " %s" % nc
                        first = 0
                    elif first:
                        num += "{} {}".format(comma, nc)
                    else:
                        num += " %s" % nc
                return num
        
        def type_num(self, num):
            array = []
            if num < 0:
                num = abs(num)
            while num:
                num //=1000 
                if num > 0:
                    array.append(int(num))
            return array
        
        def end_way(self, array, endstr, num):
            result = []
            if num > 1000 or num < -1000:
                for i in range(len(array)):
                    result = re.sub(mill[i+1],morph.parse(mill[i+1])[0].make_agree_with_number(array[i]).word, endstr)
                    endstr = result
            else:
                result = endstr
            return result

        def corr_num(self, endstr):
            result = []
            lol = re.split(" ",endstr)
            for x in range(len(lol)):
                for value in ordinal_tens.values():
                    if lol[x] == 'тысяча':
                        for j in range(len(unit) - 1):
                            if lol[lol.index('тысяча') - 1] == unit[j+1]:
                                lol[lol.index('тысяча') - 1] = unit_cardinal[j+1]
                                result = "{}".format(" ".join(lol))
                                endstr = result
                                break
                    elif lol[x] == value:
                        for j in range(len(unit) - 1):
                            if lol[lol.index(value) - 1] == 'один':
                                lol[lol.index(value) - 1] = 'одно' 
                                break
                            else:
                                lol[lol.index(value) - 1] = morph.parse(lol[lol.index(value) - 1])[0].inflect({'gent'}).word
                        result = "{}".format(" ".join(lol))
                        endstr = result
                        break
                    else:
                        result = endstr
            return result

        def inflect_num_noun(self, endstr, noun, typeinf, num): #склонение 
            result = []
            pup = re.split(" ",endstr)
            rang = len(pup)
            for x in range(len(pup)):
                noun_res = morph.parse(noun)[0]
                gen = noun_res.tag.gender
                if ('accs' in typeinf) and ('anim' in noun_res.tag): 
                    if pup[x] == 'минус':
                        pup[x] = 'минус'
                    elif pup[x] == 'один' and x == rang - 1:
                        if 'masc' in noun_res.tag:
                            pup[x] = morph.parse(pup[x])[0].inflect({"gent",'masc'}).word
                        else:
                            pup[x] = morph.parse(pup[x])[0].inflect({"accs",gen}).word
                    elif abs(num) % 10 in [2,3,4]:
                        if 'neut' in noun_res.tag and pup[x] == 'два' and x == rang - 1:
                            pup[x] = morph.parse(pup[x])[0].inflect({"nomn",'masc'}).word
                        else:
                            if 'Pltm' in noun_res.tag:
                                num = abs(num) % 10 
                                if pup[len(pup)-1] == unit[abs(num)]: 
                                    pup[len(pup)-1] = unit_coll[abs(num)-1]
                            else:
                                if pup[len(pup)-1] == "два":
                                    pup[len(pup)-1] = morph.parse(pup[len(pup)-1])[0].inflect({"nomn",gen}).word
                                else:
                                    pup[x] = morph.parse(pup[x])[0].inflect({"nomn"}).word
                    else: 
                        a = pup[x]
                        for i in range(1,6):
                            nrm = morph.parse(pup[x])[0].normal_form
                            if nrm == mill[i].replace(' ', ''):
                                pup[x] = a
                                break
                            else:
                                pup[x] = morph.parse(pup[x])[0].inflect({"accs"}).word
                    if abs(num) % 10 == 1 and abs(num) % 100 not in [11]: 
                        if 'Pltm' in noun_res.tag: 
                            noun_res = noun_res.inflect({"accs"}).word
                        else:
                            noun_res = noun_res.inflect({"sing","accs",gen}).word
                    elif abs(num) % 10 in [2,3,4]:
                        if 'Pltm' in noun_res.tag:
                            noun_res = noun_res.inflect({"gent"}).word
                        else:
                            if abs(num) % 100 in [12,13,14]:
                                noun_res = noun_res.inflect({"plur","gent"}).word
                            else:
                                noun_res = noun_res.inflect({"sing","gent"}).word
                    else:
                        noun_res = noun_res.inflect({"plur","gent"}).word
                elif ('accs' in typeinf) and ('inan' in noun_res.tag):
                    if pup[x] == 'минус':
                        pup[x] = 'минус'
                    elif pup[x] == 'один' and x == rang - 1:
                        if 'masc' in noun_res.tag:
                            pup[x] = morph.parse(pup[x])[0].inflect({"nomn",'masc'}).word
                        else: 
                            pup[x] = morph.parse(pup[x])[0].inflect({"accs",gen}).word
                    elif abs(num) % 10 in [2,3,4]:
                        if 'Pltm' in noun_res.tag:
                            num = abs(num) % 10 
                            if pup[len(pup)-1] == unit[abs(num)]: 
                                pup[len(pup)-1] = unit_coll[abs(num)-1]
                        else:
                            if pup[len(pup)-1] == "два":
                                pup[len(pup)-1] = morph.parse(pup[len(pup)-1])[0].inflect({"nomn",gen}).word
                            else:
                                pup[x] = morph.parse(pup[x])[0].inflect({"nomn"}).word    
                    else:
                        a = pup[x]
                        for i in range(1,6):
                            nrm = morph.parse(pup[x])[0].normal_form
                            if nrm == mill[i].replace(' ', ''):
                                pup[x] = a
                                break
                            else:
                                pup[x] = morph.parse(pup[x])[0].inflect({"accs"}).word
                    if abs(num) % 10 == 1 and abs(num) % 100 not in [11]:
                        if 'Pltm' in noun_res.tag:
                            noun_res = noun_res.inflect({"gent"}).word
                        else:
                            noun_res = noun_res.inflect({"sing","accs"}).word
                    elif abs(num) % 10 in [2,3,4]:
                        if 'Pltm' in noun_res.tag:
                            noun_res = noun_res.inflect({"gent"}).word
                        else:
                            if abs(num) % 100 in [12,13,14]:
                                noun_res = noun_res.inflect({"plur","gent"}).word
                            else:
                                noun_res = noun_res.inflect({"sing","gent"}).word
                    else:
                        noun_res = noun_res.inflect({"plur","gent"}).word
                else:
                    if pup[x] == 'один' and x == rang - 1: 
                        noun_res = noun_res.inflect({typeinf,"sing"}).word
                        pup[x] = morph.parse(pup[x])[0].inflect({typeinf,gen}).word
                    else:
                        if pup[x] == 'сто':
                            pup[x] = 'ста'
                        elif pup[x] == 'тысячи':
                            pup[x] = morph.parse(pup[x])[0].inflect({typeinf,'plur'}).word
                        elif pup[x] == 'минус':
                            pup[x] = 'минус'
                        else:
                            pup[x] = morph.parse(pup[x])[0].inflect({typeinf}).word
                        noun_res = noun_res.inflect({typeinf,"plur"}).word
                result = "{}".format(" ".join(pup))
                total = " ".join((result, noun_res))
            return total

        def inflect_ord_num_noun(self, endstr, noun, typeinf): #склонение порядкового
            result = []
            mim = re.split(" ",endstr)
            last = morph.parse(mim[len(mim) - 1])[0]
            noun_res = morph.parse(noun)[0]
            gen = noun_res.tag.gender
            mim[len(mim) - 1] = last.inflect({gen,typeinf}).word #числит.
            noun_res = noun_res.inflect({typeinf}).word # сущ.
            result = "{}".format(" ".join(mim))
            total = " ".join((result, noun_res))
            return total


        def inflect_float_num_noun(self, noun, endstr, typeinf):
            result = []
            tyt = re.split(" ",endstr)
            if endstr == 'одна целая пять десятых':
                tyt = 'полтора'
                noun_res = morph.parse(noun)[0]
                gen = noun_res.tag.gender 
                tyt = morph.parse(morph.parse(tyt)[0].inflect({gen}).word)[0].inflect({typeinf}).word
                noun_res = noun_res.inflect({typeinf}).word
                float_noun = " ".join((tyt, noun_res))
            else:
                for x in range(len(tyt)):  
                    noun_res = morph.parse(noun)[0]
                    if ('accs' in typeinf) and (tyt[x] == 'десятых'): 
                        tyt[x] = 'десятых'
                    else:
                        tyt[x] = morph.parse(tyt[x])[0].inflect({typeinf}).word
                    noun_res = noun_res.inflect({"gent"}).word
                    result = "{}".format(" ".join(tyt))
                    float_noun = " ".join((result, noun_res))
            return float_noun

        
        def correct_ord_num(self, endstr, noun): #порядковое числительное 
            noun = morph.parse(noun)[0]
            result = [] 
            olo = re.split(" ",endstr)
            last = morph.parse(olo[len(olo) - 1])[0]
            gen = noun.tag.gender 
            if 'Pltm' in noun.tag:
                olo[len(olo) - 1] = last.inflect({'plur','nomn'}).word
                result = "{}".format(" ".join(olo))
                total = " ".join((result, noun.normal_form))
            elif gen in noun.tag:
                olo[len(olo) - 1] = last.inflect({gen,'sing','nomn'}).word
                result = "{}".format(" ".join(olo))
                total = " ".join((result, noun.normal_form))
            else:
                total = endstr
            return total
        
        def correct_card_num(self, num, endstr, noun): #собирательные и количественные 
            noun_res = morph.parse(noun)[0]
            what_gen = noun_res.tag.gender
            result = []
            aka = re.split(" ",endstr) #изменить что последняя цифра, а не одна цифра
            if (('Pltm' in noun_res.tag) and (abs(num) % 10 in digits) or (('anim' in noun_res.tag) and ('gent' in noun_res.tag or 'accs' in noun_res.tag) and ('plur' in noun_res.tag) and (abs(num) % 10 in digits))): #нужно брать 2-10 числа и менять на собирательные
                num = abs(num) % 10 
                aka[len(aka) - 1] = unit_coll[abs(num)-1]
                result = "{}".format(" ".join(aka))
                noun_res = noun_res.inflect({'plur','gent'}).word
            else: #Склоняем 1,2 в конце числительного + существителное 
                if aka[len(aka) - 1] == 'один' or aka[len(aka) - 1] == 'два':
                    aka[len(aka) - 1] = morph.parse(aka[len(aka) - 1])[0].inflect({what_gen}).word
                    result = "{}".format(" ".join(aka))
                else:
                    result = endstr
                if abs(num) % 10 == 1 and abs(num) % 100 != 11:
                    noun_res = noun_res.inflect({'nomn','sing'}).word 
                elif abs(num) % 10 in [2,3,4] and (abs(num) % 100 < 10 or abs(num) % 100 >= 20):
                    if 'Pltm' in noun_res.tag:
                        noun_res = noun_res.inflect({'gent'}).word
                    else:
                        noun_res = noun_res.inflect({'gent','sing'}).word
                else:
                    noun_res = noun_res.inflect({'gent','plur'}).word
            total_2 = " ".join((result, noun_res))
            return total_2


#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------

    class ua_engine:
        def ordinal_ua(self, num):
            if re.match(r"\d", str(num)):
                try:
                    num % 2
                    n = num
                except TypeError:
                    if "." in str(num):
                        try:
                            n = int(num[-1])

                        except ValueError: 
                            n = int(num[:-1])
                    else:
                        n = int(num)
                try:
                    post = nth_ua[n % 100]
                except KeyError:
                    post = nth_ua[n % 10]
                return "{}{}".format(num, post)
            else:
                mo = re.search(r"(%s)\Z" % ordinal_suff_ua, num)
                try:
                    post = ordinal_ua[mo.group(1)]
                    return re.sub(r"(%s)\Z" % ordinal_suff_ua, post, num)
                except AttributeError:
                    return "%sий" % num

        def millfn(self, ind=0):
            if ind > len(mill_ua) - 1:
                self.exit_text.setText("Заданное число превосходит допустимое значение")
                raise NumOutOfRangeError
            return mill_ua[ind]

        def unitfn(self, units, mindex=0):
            return "{}{}".format(unit_ua[units], self.millfn(mindex))

        def tenfn(self, tens, units, mindex=0):
            if tens != 1:
                return "{}{}{}{}".format(
                    ten_ua[tens],
                    " ",
                    unit_ua[units],
                    self.millfn(mindex),
                )
            return "{}{}".format(teen_ua[units], mill_ua[mindex])

        def hundfn(self, hundreds, tens, units, mindex):
            if hundreds:
                # andword = " %s " % self.number_args["andword"] if tens or units else ""
                return "{}{}{}{} ".format(
                    hundred_ua[hundreds], 
                    " ",
                    self.tenfn(tens, units),
                    self.millfn(mindex)
                )
            if tens or units:
                return "{}{} ".format(self.tenfn(tens, units), self.millfn(mindex))
            return ""

        def group1sub(self, mo):
            units = int(mo.group(1))
            if units == 1:
                return " %s, " % self.number_args["one"]
            elif units:
                return "%s, " % unit_ua[units]
            else:
                return " %s, " % self.number_args["zero"]

        def group1bsub(self, mo):
            units = int(mo.group(1))
            if units:
                return "%s, " % unit_ua[units]
            else:
                return " %s, " % self.number_args["zero"]

        def group2sub(self, mo):
            tens = int(mo.group(1))
            units = int(mo.group(2))
            if tens:
                return "%s, " % self.tenfn(tens, units)
            if units:
                return " {} {} ".format(self.number_args["zero"], unit_ua[units])
            return " {} {} ".format(self.number_args["zero"], self.number_args["zero"])

        def group3sub(self, mo):
            hundreds = int(mo.group(1))
            tens = int(mo.group(2))
            units = int(mo.group(3))
            if hundreds == 1:
                hunword = " %s" % self.number_args["one"]
            elif hundreds:
                hunword = "%s" % unit_ua[hundreds]
            else:
                hunword = " %s" % self.number_args["zero"]
            if tens:
                tenword = self.tenfn(tens, units)
            elif units:
                tenword = " {} {}".format(self.number_args["zero"], unit_ua[units])
            else:
                tenword = " {} {}".format(
                    self.number_args["zero"], self.number_args["zero"]
                )
            return "{} {} ".format(hunword, tenword)

        def hundsub(self, mo):
            ret = self.hundfn(
                int(mo.group(1)), int(mo.group(2)), int(mo.group(3)), self.mill_count
            )
            self.mill_count += 1
            return ret

        def tensub(self, mo):
            return "%s " % self.tenfn(int(mo.group(1)), int(mo.group(2)), self.mill_count)

        def unitsub(self, mo):
            return "%s " % self.unitfn(int(mo.group(1)), self.mill_count)

        def enword(self, num, group):

            if group == 1:
                num = re.sub(r"(\d)", self.group1sub, num)
            elif group == 2:
                num = re.sub(r"(\d)(\d)", self.group2sub, num)
                num = re.sub(r"(\d)", self.group1bsub, num, 1)
            elif group == 3:
                num = re.sub(r"(\d)(\d)(\d)", self.group3sub, num)
                num = re.sub(r"(\d)(\d)", self.group2sub, num, 1)
                num = re.sub(r"(\d)", self.group1sub, num, 1)
            elif int(num) == 0:
                num = self.number_args["zero"]
            elif int(num) == 1:
                num = self.number_args["one"]
            else:
                num = num.lstrip().lstrip("0")
                self.mill_count = 0
                mo = re.search(r"(\d)(\d)(\d)(?=\D*\Z)", num)
                while mo:
                    num = re.sub(r"(\d)(\d)(\d)(?=\D*\Z)", self.hundsub, num, 1)
                    mo = re.search(r"(\d)(\d)(\d)(?=\D*\Z)", num)
                num = re.sub(r"(\d)(\d)(?=\D*\Z)", self.tensub, num, 1)
                num = re.sub(r"(\d)(?=\D*\Z)", self.unitsub, num, 1)
            return num

        def blankfn(self, mo):
            """глобальная пустая замена
            """
            return ""

        def commafn(self, mo):
            """глобальная ',' замена
            """
            return ","

        def spacefn(self, mo):
            """глобальная ' ' замена
            """
            return " "

        def number_to_words(
            self,
            num,
            wantlist=False,
            group=0,
            comma="",
            andword="",
            zero="нуль",
            one="один",
            decimal="целих",
            threshold=None,
        ):
            self.number_args = dict(andword=andword, zero=zero, one=one)
            num = "%s" % num
            # Обработка "стилистических" преобразований (до заданного порога)
            if threshold is not None and float(num) > threshold:
                spnum = num.split(".", 1)
                while comma:
                    (spnum[0], n) = re.subn(r"(\d)(\d{3}(?:,|\Z))", r"\1,\2", spnum[0])
                    if n == 0:
                        break
                try:
                    return "{}.{}".format(spnum[0], spnum[1])
                except IndexError:
                    return "%s" % spnum[0]

            if group < 0 or group > 3:
                raise BadChunkingOptionError
            nowhite = num.lstrip()
            if nowhite[0] == "+":
                sign = "плюс"
            elif nowhite[0] == "-":
                sign = "мінус"
            else:
                sign = ""

            myord = num[-2:] in ("ій", "ий")
            if myord:
                num = num[:-2]
            finalpoint = False
            if decimal:
                if group != 0:
                    chunks = num.split(".")
                else:
                    chunks = num.split(".", 1)
                if chunks[-1] == "":  # удаляем пустую строку, если после десятичной дроби ничего нет
                    chunks = chunks[:-1]
                    finalpoint = True  # добавляем точку в конце вывода 
            else:
                chunks = [num]

            first = 1
            loopstart = 0

            if chunks[0] == "":
                first = 0
                if len(chunks) > 1:
                    loopstart = 1

            for i in range(loopstart, len(chunks)):
                chunk = chunks[i]
                # убираем все \D
                chunk = re.sub(r"\D", self.blankfn, chunk)
                if chunk == "":
                    chunk = "0"

                if group == 0 and (first == 0 or first == ""):
                    chunk = self.enword(chunk, 1)
                else:
                    chunk = self.enword(chunk, group)

                if chunk[-2:] == ", ": 
                    chunk = chunk[:-2]
                chunk = re.sub(r"\s+,", self.commafn, chunk)

                if group == 0 and first:
                    chunk = re.sub(r", (\S+)\s+\Z", " %s \\1" % andword, chunk)
                chunk = re.sub(r"\s+", self.spacefn, chunk)
                chunk = chunk.strip()
                if first:
                    first = ""
                chunks[i] = chunk

            numchunks = []
            if first != 0:
                numchunks = chunks[0].split("%s " % comma)

            if myord and numchunks:
                mo = re.search(r"(%s)\Z" % ordinal_suff_ua, numchunks[-1])
                result = []
                if mo:
                    numchunks[-1] = re.sub(
                        r"(%s)\Z" % ordinal_suff_ua, ordinal_ua[mo.group(1)], numchunks[-1]
                    )
                else:
                    numchunks[-1] = re.sub(r"ь","",numchunks[-1])
                    numchunks[-1] += "ий"

            for chunk in chunks[1:]:
                numchunks.append(decimal)
                numchunks.extend(chunk.split("%s " % comma))

            if finalpoint:
                numchunks.append(decimal)

            if wantlist:
                if sign:
                    numchunks = [sign] + numchunks
                return numchunks
            elif group:
                signout = "%s " % sign if sign else ""
                return "{}{}".format(signout, " ".join(numchunks))
            else:
                signout = "%s " % sign if sign else ""
                num = "{}{}".format(signout, numchunks.pop(0))
                if decimal is None:
                    first = True
                else:
                    first = not num.endswith(decimal)
                for nc in numchunks:
                    if nc == decimal:
                        num += " %s" % nc
                        first = 0
                    elif first:
                        num += "{} {}".format(comma, nc)
                    else:
                        num += " %s" % nc
                return num
        
        def type_num(self, num):
            array = []
            if num < 0:
                num = abs(num)
            while num:
                num //=1000
                if num > 0:
                    array.append(int(num))
            return array
        
        def end_way(self, array, endstr, num):
            result = []
            if num > 1000 or num < -1000:
                for i in range(len(array)):
                    if array[i] == 1 and array[i-1] not in [12,13,14]:
                        result = re.sub(mill_ua[i+1],morph_ua.parse(mill_ua[i+1])[0].inflect({'nomn'}).word, endstr)
                    elif array[i] in [2,3,4] and array[i-1] not in [12,13,14]:
                        result = re.sub(mill_ua[i+1],morph_ua.parse(mill_ua[i+1])[0].inflect({'gent'}).word, endstr)
                    else:
                        result = re.sub(mill_ua[i+1],morph_ua.parse(mill_ua[i+1])[0].inflect({'gent','plur'}).word, endstr)
                    endstr = result
            else:
                result = endstr
            return result

        def corr_num(self, endstr):
            result = []
            lol = re.split(" ",endstr)
            for x in range(len(lol)):
                for value in ordinal_tens_ua.values():
                    if lol[x] == 'тисяча':
                        for j in range(len(unit_ua) - 1):
                            if lol[lol.index('тисяча') - 1] == unit_ua[j+1]:
                                lol[lol.index('тисяча') - 1] = unit_cardinal_ua[j+1]
                                result = "{}".format(" ".join(lol))
                                endstr = result
                                break
                    elif lol[x] == value:
                        for j in range(len(unit_ua) - 1):
                            if lol[lol.index(value) - 1] == 'один':
                                lol[lol.index(value) - 1] = 'одно' 
                                break
                            else:
                                lol[lol.index(value) - 1] = morph_ua.parse(lol[lol.index(value) - 1])[0].inflect({'gent'}).word
                        result = "{}".format(" ".join(lol))
                        endstr = result
                        break
                    else:
                        result = endstr
            return result

        def inflect_num_noun(self, endstr, noun, typeinf, num): #склонение 
            result = []
            pup = re.split(" ",endstr)
            rang = len(pup)
            for x in range(len(pup)):
                noun_res = morph_ua.parse(noun)[0]
                gen = noun_res.tag.gender
                if abs(num) % 10 == 1:
                    if abs(num) % 100 == [11]:
                        if typeinf == 'accs':
                            noun_res = noun_res.inflect({'gent','plur'}).word # сущ.
                        else:
                            noun_res = noun_res.inflect({typeinf,'plur'}).word # сущ.
                        if pup[x] == 'мінус':
                            pup[x] = 'мінус'
                        else:
                            pup[x] = morph_ua.parse(pup[x])[0].inflect({typeinf}).word #числит.
                    else:
                        noun_res = noun_res.inflect({typeinf}).word # сущ.
                        if pup[x] == 'мінус':
                            pup[x] = 'мінус'
                        else:
                            pup[x] = morph_ua.parse(pup[x])[0].inflect({typeinf,gen}).word #числит.
                else:
                    if abs(num) % 10 == 2 and abs(num) % 100 != 12:
                        if gen is None:
                            pup[x] = morph_ua.parse(pup[x])[0].inflect({typeinf}).word #числит.
                        elif pup[x] == 'мінус':
                            pup[x] = 'мінус'
                        else:
                            pup[x] = morph_ua.parse(pup[x])[0].inflect({typeinf,gen}).word #числит.
                    elif abs(num) % 10 == 3 and abs(num) % 100 != 13 and x == rang - 1: 
                        if typeinf == 'gent':
                            pup[x] = 'трьох'
                        elif typeinf == 'datv':
                            pup[x] = 'трьом'
                        elif typeinf == 'accs': 
                            pup[x] = 'три'  
                        elif typeinf == 'ablt':
                            pup[x] = 'трьома́'
                        elif typeinf == 'loct':
                            pup[x] = 'трьох'
                        elif pup[x] == 'мінус':
                            pup[x] = 'мінус'
                    else:
                        if pup[x] == 'мінус':
                            pup[x] = 'мінус'
                        else:
                            pup[x] = morph_ua.parse(pup[x])[0].inflect({typeinf}).word #числит.
                    if gen is None and typeinf == 'accs' and noun_res.word != 'діти':
                        noun_res = noun_res.inflect({'gent'}).word # сущ.
                    elif noun_res.word == 'діти':
                        if typeinf == 'gent':
                            noun_res = 'дітей'
                        elif typeinf == 'datv':
                            noun_res = 'дітям'
                        elif typeinf == 'accs': 
                            noun_res = 'дітей'  
                        elif typeinf == 'ablt':
                            noun_res = 'дітьми'
                        elif typeinf == 'loct':
                            noun_res = 'дітях'
                    else:
                        if noun_res.word == 'вікно':
                            noun_res = 'вікон'
                            noun_res = morph_ua.parse(noun_res)[0]
                        noun_res = noun_res.inflect({typeinf}).word # сущ.
                result = "{}".format(" ".join(pup))
                total = " ".join((result, noun_res))
            return total

        def inflect_ord_num_noun(self, endstr, noun, typeinf): #склонение порядкового
            result = []
            mim = re.split(" ",endstr)
            last = morph_ua.parse(mim[len(mim) - 1])[0]
            noun_res = morph_ua.parse(noun)[0]
            gen = noun_res.tag.gender
            if typeinf == 'accs' and 'masc' in noun_res.tag:
                mim[len(mim) - 1] = last.inflect({gen,'nomn'}).word #числит.
            else:
                mim[len(mim) - 1] = last.inflect({gen,typeinf}).word #числит.
            noun_res = noun_res.inflect({typeinf}).word # сущ.
            result = "{}".format(" ".join(mim))
            total = " ".join((result, noun_res))
            return total

        def inflect_float_num_noun(self, noun, endstr, typeinf):
            result = []
            tyt = re.split(" ",endstr)
            if endstr == "одна ціла п'ять десятих":
                tyt = 'півтора'
                noun_res = morph_ua.parse(noun)[0]
                gen = noun_res.tag.gender 
                if typeinf == 'gent' or typeinf == 'accs':
                    noun_res = noun_res.inflect({'gent'}).word
                else:
                    noun_res = noun_res.inflect({typeinf,'plur'}).word
                float_noun = " ".join((tyt, noun_res))
            else:
                for x in range(len(tyt)): 
                    noun_res = morph_ua.parse(noun)[0]
                    if ('accs' in typeinf) and (tyt[x] == 'десятих'): 
                        tyt[x] = 'десятих'
                    else: 
                        tyt[x] = morph_ua.parse(tyt[x])[0].inflect({typeinf}).word
                    noun_res = noun_res.inflect({"gent"}).word
                    result = "{}".format(" ".join(tyt))
                    float_noun = " ".join((result, noun_res))
            return float_noun

        
        def correct_ord_num(self, endstr, noun): #порядковое числительное 
            noun = morph_ua.parse(noun)[0]
            result = [] 
            olo = re.split(" ",endstr)
            last = morph_ua.parse(olo[len(olo) - 1])[0]
            gen = noun.tag.gender 
            if 'Pltm' in noun.tag:
                olo[len(olo) - 1] = last.inflect({'plur','nomn'}).word
                result = "{}".format(" ".join(olo))
                total = " ".join((result, noun.normal_form))
            elif gen in noun.tag:
                olo[len(olo) - 1] = last.inflect({gen,'nomn'}).word
                result = "{}".format(" ".join(olo))
                total = " ".join((result, noun.normal_form))
            else:
                total = endstr
            return total
        
        def correct_card_num(self, num, endstr, noun): #собирательные и количественные 
            noun_res = morph_ua.parse(noun)[0]
            nrm_form = morph_ua.parse(noun_res.normal_form)[0]
            what_gen = nrm_form.tag.gender
            result = []
            aka = re.split(" ",endstr) 
            if (('Pltm' in noun_res.tag) and (abs(num) % 10 in digits) or ((noun_res.word in only_plur) and (abs(num) % 10 in digits))): #нужно брать 2-5 числа и менять на собирательные
                num = abs(num) % 10 
                aka[len(aka) - 1] = unit_coll_ua[abs(num)-1]
                result = "{}".format(" ".join(aka))
                if noun_res.word == 'діти':
                    noun_res = 'дітей'
                else:
                    noun_res = noun_res.inflect({'plur','gent'}).word
            else: #Склоняем 1,2 в конце числительного + существителное 
                if aka[len(aka) - 1] == 'один' or aka[len(aka) - 1] == 'два':
                    aka[len(aka) - 1] = morph_ua.parse(aka[len(aka) - 1])[0].inflect({what_gen}).word
                    result = "{}".format(" ".join(aka))
                else:
                    result = endstr
            noun_res = morph_ua.parse(noun)[0]
            if abs(num) % 10 == 1 and noun_res.word != 'діти':
                if abs(num) % 100 == 11:
                    if noun_res.tag.number != None:  
                        noun_res = noun_res.inflect({'gent','plur'}).word   
                    else:
                        noun_res = noun_res.inflect({'gent'}).word
                else:
                    if noun_res.tag.number != None:  
                        noun_res = noun_res.inflect({'nomn','plur'}).word 
                    else:
                        noun_res = noun_res.inflect({'nomn'}).word   
            elif (abs(num) % 10 in [2,3,4]) and (noun_res.word not in only_plur):
                if abs(num) % 100 in [12,13,14]:
                    if noun_res.tag.number != None:  
                        noun_res = noun_res.inflect({'gent','plur'}).word   
                    else:
                        noun_res = noun_res.inflect({'gent'}).word
                else:
                    if abs(num) > 4:
                        noun_res = noun_res.inflect({'gent'}).word 
                    else:
                        if noun_res.tag.number != None:  
                            noun_res = noun_res.inflect({'nomn','plur'}).word 
                        else:
                            if noun_res.tag.gender == 'neut':
                                noun_res = noun_res.inflect({'gent'}).word
                            else:
                                noun_res = noun_res.inflect({'nomn'}).word
            else:
                if noun_res.word == 'діти':
                    noun_res = 'дітей'
                elif noun_res.word == 'вікно':
                    noun_res = 'вікон'
                else:
                    noun_res = noun_res.inflect({'gent','plur'}).word   
            total_2 = " ".join((result, noun_res))
            return total_2

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
    class float_nums():
        def check_length(self, value, length):
            """
            Проверяет длину значения
            @param value: значение для проверки
            @type value: C {str}
            @param length: проверка длины 
            @type length: C {int}
            @return: ничего при успешной проверке
            @raise ValueError: проверка не удалась
            """
            _length = len(value)
            if _length != length:
                raise ValueError("length must be %d, not %d" % \
                                (length, _length))


        def check_positive(self, value, strict=False):
            """
            Проверяет, положительна ли переменная
            @param value: значение для проверки
            @type value: C{integer types}, C{float} or C{Decimal}
            @return: ничего при успешной проверке
            @raise ValueError: проверка не удалась
            """
            if not strict and value < 0:
                raise ValueError("Value must be positive or zero, not %s" % str(value))
            if strict and value <= 0:
                raise ValueError("Value must be positive, not %s" % str(value))


        def split_values(self, ustring, sep=u','):
            """
            Разделяет строку Unicode разделителем C {sep},
            но пропускает экранированный разделитель.
            
            @param ustring: строка для разделения
            @type ustring: C{unicode}
            
            @param sep: separator (по умолчанию u ',')
            @type sep: C{unicode}
            
            @return: кортеж разделенных элементов
            """
            assert isinstance(ustring, str), "Должно быть unicode, not %s" % type(ustring)
            ustring_marked = ustring.replace(u'\,', u'\uffff')
            items = tuple([i.strip().replace(u'\uffff', u',') for i in ustring_marked.split(sep)])
            return items

        def _get_float_remainder(self, fvalue, typeindf, signs=9):
            self.check_positive(fvalue)
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
                # при округлении цифр вида 0.998 ругается
                raise ValueError("Signs overflow: I can't round only fractional part \
                                of %s to fit %s in %d signs" % \
                                (str(fvalue), orig_remainder, signs))
            return remainder


        def choose_plural(self, amount, variants): 
            if isinstance(variants, str):
                variants = self.split_values(variants)
            self.check_length(variants, 3)
            amount = abs(amount)
            if amount % 10 == 1 and amount % 100 != 11:
                variant = 0
            elif amount % 10 >= 2 and amount % 10 <= 4 and \
                (amount % 100 < 10 or amount % 100 >= 20):
                variant = 1
            else:
                variant = 2
            return variants[variant]


        def money(self, amount, typeindf,  zero_for_kopeck=False):
            self.check_positive(amount)
            pts = []
            amount = round(amount, 2)
            if typeindf == False: #Ua
                pts.append(self.sum_string_ua(int(amount), 1, (u"гривня", u"гривні", u"гривень")))
                remainder = self._get_float_remainder(amount,typeindf, 2)
                iremainder = int(remainder)
                if iremainder != 0 or zero_for_kopeck:
                    # если 3.1, то это 10 копеек, а не одна
                    if iremainder < 10 and len(remainder) == 1:
                        iremainder *= 10
                    pts.append(self.sum_string_ua(iremainder, 2,
                                        (u"копійка", u"копійки", u"копійок")))
            elif typeindf == True: #Ru
                pts.append(self.sum_string(int(amount), 1, (u"рубль", u"рубля", u"рублей")))
                remainder = self._get_float_remainder(amount,typeindf, 2)
                iremainder = int(remainder)
                if iremainder != 0 or zero_for_kopeck:
                    if iremainder < 10 and len(remainder) == 1:
                        iremainder *= 10
                    pts.append(self.sum_string(iremainder, 2,
                                        (u"копейка", u"копейки", u"копеек")))
            return u" ".join(pts)

        def in_words_float(self, amount, typeindf, _gender=FEMALE):
            self.check_positive(amount)
            pts = []
            if typeindf == False: #Ua
                # преобразуем целую часть
                pts.append(self.sum_string_ua(int(amount), 2,
                                    (u"ціла", u"цілих", u"цілих")))
                # теперь то, что после запятой
                remainder = self._get_float_remainder(amount,typeindf)
                signs = len(str(remainder)) - 1
                pts.append(self.sum_string_ua(int(remainder), 2, FRACTIONS_UA[signs]))
            elif typeindf == True: #Ru
                pts.append(self.sum_string(int(amount), 2,
                                    (u"целая", u"целых", u"целых")))
                remainder = self._get_float_remainder(amount,typeindf)
                signs = len(str(remainder)) - 1
                pts.append(self.sum_string(int(remainder), 2, FRACTIONS[signs]))
            else:
                raise TypeError("Что-то пошло не так")
            return u" ".join(pts)

        def in_words(self, amount, typeindf=True, gender=None):
            self.check_positive(amount)
            if gender is None:
                args = (amount,)
            else:
                args = (amount, gender)
            # если дробное
            if isinstance(amount, (float, Decimal)):
                return self.in_words_float(*args, typeindf)
            else:
                # до сюда не должно дойти
                raise TypeError("Число должно быть не целое, получили %s" % type(amount))


        def sum_string(self, amount, gender, items=None):
            if isinstance(items, str):
                items = self.split_values(items)
            if items is None:
                items = (u"", u"", u"")
            try:
                one_item, two_items, five_items = items
            except ValueError:
                raise ValueError("Цепь должна быть 3х элементная")
            self.check_positive(amount)
            if amount == 0:
                if five_items:
                    return u"ноль %s" % five_items
                else:
                    return u"ноль"
            into = u''
            tmp_val = amount
            # единицы
            into, tmp_val = self._sum_string_fn(into, tmp_val, gender, items)
            # тысячи
            into, tmp_val = self._sum_string_fn(into, tmp_val, FEMALE,
                                            (u"тысяча", u"тысячи", u"тысяч"))
            # миллионы
            into, tmp_val = self._sum_string_fn(into, tmp_val, MALE,
                                            (u"миллион", u"миллиона", u"миллионов"))
            # миллиарды
            into, tmp_val = self._sum_string_fn(into, tmp_val, MALE,
                                            (u"миллиард", u"миллиарда", u"миллиардов"))
            if tmp_val == 0:
                return into
            else:
                raise ValueError("Слишком большое число")

        def sum_string_ua(self, amount, gender, items=None):
            if isinstance(items, str):
                items = self.split_values(items)
            if items is None:
                items = (u"", u"", u"")
            try:
                one_item, two_items, five_items = items
            except ValueError:
                raise ValueError("Цепь должна быть 3х элементная")
            self.check_positive(amount)
            if amount == 0:
                if five_items:
                    return u"ноль %s" % five_items
                else:
                    return u"ноль"
            into = u''
            tmp_val = amount
            into, tmp_val = self._sum_string_fn_ua(into, tmp_val, gender, items)
            into, tmp_val = self._sum_string_fn_ua(into, tmp_val, FEMALE,
                                            (u"тысяча", u"тисячі", u"тысяч"))
            into, tmp_val = self._sum_string_fn_ua(into, tmp_val, MALE,
                                            (u"мільйон", u"мільйона", u"мільйонів"))
            into, tmp_val = self._sum_string_fn_ua(into, tmp_val, MALE,
                                            (u"мільярд", u"мільярда", u"мільярдів"))
            if tmp_val == 0:
                return into
            else:
                raise ValueError("Слишком большое число")

        def _sum_string_fn(self, into, tmp_val, gender, items=None):
            if items is None:
                items = (u"", u"", u"")
            one_item, two_items, five_items = items
            self.check_positive(tmp_val)
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
                end_word = self.choose_plural(amount, items)
                words.append(ONES[amount][gender-1])
            words.append(end_word)
            # добавляем то, что уже было
            words.append(into)
            # убираем пустые подстроки
            words = filter(lambda x: len(x) > 0, words)
            # склеиваем и отдаем
            return u" ".join(words).strip(), tmp_val


        def _sum_string_fn_ua(self, into, tmp_val, gender, items=None):
            if items is None:
                items = (u"", u"", u"")
            one_item, two_items, five_items = items
            self.check_positive(tmp_val)
            if tmp_val == 0:
                return into, tmp_val
            words = []
            rest = tmp_val % 1000
            tmp_val = tmp_val // 1000
            if rest == 0:
                if into == u"":
                    into = u"%s " % five_items
                return into, tmp_val
            end_word = five_items
            words.append(HUNDREDS_UA[rest // 100])
            rest = rest % 100
            rest1 = rest // 10
            tens = rest1 == 1 and TENS_UA[rest] or TENS_UA[rest1]
            words.append(tens)
            if rest1 < 1 or rest1 > 1:
                amount = rest % 10
                end_word = self.choose_plural(amount, items)
                words.append(ONES_UA[amount][gender-1])
            words.append(end_word)
            words.append(into)
            words = filter(lambda x: len(x) > 0, words)
            return u" ".join(words).strip(), tmp_val


#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()
        self.rus = self.ru_engine()
        self.ua = self.ua_engine()
        self.fln = self.float_nums()

        # start button
        self.go_button = QPushButton('&Start')

        # validator
        self.insert_number_line = QLineEdit()
        self.validator = QRegExpValidator(QRegExp(r'\d{1,7}\.\d{1,2}'), self)
        self.insert_number_line.setValidator(self.validator)

        self.insert_noun_line = QLineEdit()
        self.validator = QRegExpValidator(QRegExp("[а-яА-Я\\s]+"), self)
        self.insert_noun_line.setValidator(self.validator)

        # language list
        self.language_title = QLabel('Язык:')
        self.number_title = QLabel('Число:')
        self.what_number_1 = QCheckBox('Количественное')
        self.what_number_2 = QCheckBox('Порядковое')
        self.what_number_3 = QCheckBox('Собирательное')
        self.what_number_4 = QCheckBox('Валюта')
        self.noun_title = QLabel('Существительное:')
        self.language = QComboBox()
        self.language.setFixedWidth(70)
        self.language.addItem('Ru')
        self.language.addItem('Ua')

        # exit text
        self.exit_text = QTextEdit()

        self.initui()

    def change_separator(self):
        if self.language.currentText() == "Ru":
            self.insert_number_line.setText("")
            self.exit_text.setText("")
            self.validator = QRegExpValidator(QRegExp('[а-яА-Я0-9.-\\s]+'), self)
            self.insert_number_line.setValidator(self.validator)
            self.insert_noun_line.setText("")
            self.exit_text.setText("")
            self.validator = QRegExpValidator(QRegExp("[а-яА-Я\\s]+"), self)
            self.insert_noun_line.setValidator(self.validator)
        if self.language.currentText() == "Ua":
            self.insert_number_line.setText("")
            self.exit_text.setText("")
            self.validator = QRegExpValidator(QRegExp("[А-Яа-яЁёЇїІіЄєҐґ'0-9.-\\s]+"), self)
            self.insert_number_line.setValidator(self.validator)
            self.insert_noun_line.setText("")
            self.exit_text.setText("")
            self.validator = QRegExpValidator(QRegExp("[А-Яа-яЁёЇїІіЄєҐґ'\\s]+"), self)
            self.insert_noun_line.setValidator(self.validator)

    def initui(self):

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.language_title, 1, 0, 1, 4)
        grid.addWidget(self.language, 1, 1, 1, 4)
        grid.addWidget(self.go_button, 1, 4)
        grid.addWidget(self.number_title, 3, 0, 1, 4)
        grid.addWidget(self.insert_number_line, 3, 1, 1, 4)
        grid.addWidget(self.what_number_1, 2, 1)
        grid.addWidget(self.what_number_2, 2, 2)
        grid.addWidget(self.what_number_3, 2, 3)
        grid.addWidget(self.what_number_4, 2, 4)
        grid.addWidget(self.noun_title, 4, 0, 1, 3)
        grid.addWidget(self.insert_noun_line, 4, 2, 1, 3)
        grid.addWidget(self.exit_text, 5, 0, 1, 5)
        self.setLayout(grid)

        self.setGeometry(70, 70, 550, 300)
        self.setWindowTitle('Convert number to text')
        self.show()

        self.language.currentIndexChanged.connect(self.change_separator)
        # self.insert_number_line.textEdited.connect(self.convert)

        self.go_button.clicked.connect(self.convert)

    def convert(self):  # переделать 
        self.exit_text.setText("")
        # self.insert_number = self.insert_number_line.text().replace(',', '.')

        if self.language.currentText() == "Ua":
            self.convert_ua()
        
        if self.language.currentText() == "Ru":
            self.convert_ru()

    
    def num_is_ok(self,text):
        try:
            float(text)
            return True
        except ValueError:
            return False

    def str_is_ok(self,text):
        match = re.match("[а-яА-Я]-", text)
        return bool(match)

    def convert_ua(self):
        """General Ua func"""
        noun = self.insert_noun_line 
        num = self.insert_number_line.text()
        noun_str = self.insert_noun_line.text()
        noun = morph_ua.parse(noun_str)[0]
        noun_ord_res = noun.normal_form
        if self.what_number_4.isChecked() and self.what_number_3.checkState() == Qt.Unchecked and self.what_number_2.checkState() == Qt.Unchecked and self.what_number_1.checkState() == Qt.Unchecked:
            if self.num_is_ok(str(self.insert_number_line.text())) == True:
                self.exit_text.append("|--------------------------------------|")
                self.exit_text.append("           Числительное в валюте:           ")
                self.exit_text.append("|--------------------------------------|")
                self.exit_text.append("Значение в рублях: " + self.fln.money(float(num),False))
            else:
                self.exit_text.setText(" Ошибка: Ввод некорректен")
        elif self.what_number_1.isChecked() or self.what_number_2.isChecked() or self.what_number_3.isChecked() and self.what_number_4.checkState() == Qt.Unchecked:
            if self.num_is_ok(str(self.insert_number_line.text())) == True:
                if '.' in num and self.what_number_1.isChecked() and self.what_number_2.checkState() == Qt.Unchecked and self.what_number_3.checkState() == Qt.Unchecked: # дробные значения
                    num_1 = self.fln.in_words(float(num),False)
                    self.exit_text.append("|--------------------------------------|")
                    self.exit_text.append("   Склонение дробного числительного по падежам:  ")
                    self.exit_text.append("|--------------------------------------|")
                    for x in range(0, 5):
                        inf = (self.ua.inflect_float_num_noun(noun_ord_res,num_1,to_inflect[x]))
                        self.exit_text.append(inflect_str_ua[x] + " : " + inf)
                    self.exit_text.append("|--------------------------------------|")
                elif self.what_number_3.isChecked() and 'Pltm' in noun.tag and self.what_number_1.checkState() == Qt.Unchecked and self.what_number_2.checkState() == Qt.Unchecked:
                    int_num = int(num)
                    cardinal_num = self.ua.number_to_words(int_num) #собирательное
                    num_1 = (self.ua.end_way(self.ua.type_num(int_num),self.ua.corr_num(cardinal_num),int_num)) #собирательное 
                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append(" Собирательное числительное + сущ.: " + self.ua.correct_card_num(int_num,num_1,noun_str)) 
                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append("         Склонение числительного по падежам:       ")
                    self.exit_text.append("|-------------------------------------------------|")
                    sob = re.split(" ",self.ua.correct_card_num(int_num,num_1,noun_str))
                    if sob[0] == 'мінус':
                        num_1 = sob[0] + " " + sob[1]
                        noun_ord_res = sob[2]
                    else:
                        num_1 = sob[0]
                        noun_ord_res = sob[1]
                    for x in range(0, 5):
                        inf = (self.ua.inflect_num_noun(num_1,noun_ord_res,to_inflect[x],int_num))
                        self.exit_text.append(inflect_str_ua[x] + " : " + inf)
                    self.exit_text.append("|-------------------------------------------------|")
                elif self.what_number_1.isChecked() and self.what_number_2.checkState() == Qt.Unchecked and self.what_number_3.checkState() == Qt.Unchecked:
                    int_num = int(num)
                    cardinal_num = self.ua.number_to_words(int_num) #количественные
                    num_1 = (self.ua.end_way(self.ua.type_num(int_num),self.ua.corr_num(cardinal_num),int_num)) #количественные 
                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append(" Количественное числительное + сущ.: " + self.ua.correct_card_num(int_num,num_1,noun_str)) 
                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append("         Склонение числительного по падежам:       ")
                    self.exit_text.append("|-------------------------------------------------|")
                    for x in range(0, 5):
                        inf = (self.ua.inflect_num_noun(num_1,noun_ord_res,to_inflect[x],int_num))
                        self.exit_text.append(inflect_str_ua[x] + " : " + inf)
                    self.exit_text.append("|-------------------------------------------------|")
                elif self.what_number_2.isChecked() and self.what_number_1.checkState() == Qt.Unchecked and self.what_number_3.checkState() == Qt.Unchecked:
                    int_num = int(num)
                    ordinal_num = self.ua.number_to_words(self.ua.ordinal_ua(int_num)) #порядковые
                    num_2 = (self.ua.end_way(self.ua.type_num(int_num),self.ua.corr_num(ordinal_num),int_num)) #порядковые
                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append(" Порядковое числительное + сущ.: " + self.ua.correct_ord_num(num_2,noun_ord_res))
                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append("         Склонение числительного по падежам:       ")
                    self.exit_text.append("|-------------------------------------------------|")
                    for x in range(0, 5):
                        inf = (self.ua.inflect_ord_num_noun(num_2,noun_ord_res,to_inflect[x]))
                        self.exit_text.append(inflect_str_ua[x] + " : " + inf)
                    self.exit_text.append("|-------------------------------------------------|")
            elif self.str_is_ok(str(self.insert_number_line.text())) == False: # неопредел колич
                if self.what_number_1.isChecked() and self.what_number_2.checkState() == Qt.Unchecked and self.what_number_3.checkState() == Qt.Unchecked:
                    more_num = morph_ua.parse(num)[0].normal_form
                    self.exit_text.append("|--------------------------------------|")
                    self.exit_text.append("   Склонение неопределённо-количественного числительного по падежам:  ")
                    self.exit_text.append("|--------------------------------------|")
                    # исправить множественное число
                    if more_num in uncount_num_ua:
                        for y in range(0, 5):
                            if more_num == "скільки":
                                if to_inflect[y] == 'accs':
                                    to_the_end = " ".join((sck_ua[y], noun.inflect({'gent','plur'}).word))
                                else:
                                    to_the_end = " ".join((sck_ua[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str_ua[y] + " : " + to_the_end)
                            elif more_num == "декілька":
                                if to_inflect[y] == 'accs':
                                    to_the_end = " ".join((dekil_ua[y], noun.inflect({'gent','plur'}).word))
                                else:
                                    to_the_end = " ".join((dekil_ua[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str_ua[y] + " : " + to_the_end)
                            elif more_num == "небагато":
                                if to_inflect[y] == 'accs':
                                    to_the_end = " ".join((nemnogo_ua[y], noun.inflect({'gent','plur'}).word))
                                else:
                                    to_the_end = " ".join((nemnogo_ua[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str_ua[y] + " : " + to_the_end)
                            elif more_num == "кілька":
                                if to_inflect[y] == 'accs':
                                    to_the_end = " ".join((nsck_ua[y], noun.inflect({'gent','plur'}).word))
                                else:
                                    to_the_end = " ".join((nsck_ua[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str_ua[y] + " : " + to_the_end)
                            elif more_num == "стільки":
                                if to_inflect[y] == 'accs':
                                    to_the_end = " ".join((stck_ua[y], noun.inflect({'gent','plur'}).word))
                                else:
                                    to_the_end = " ".join((stck_ua[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str_ua[y] + " : " + to_the_end)
                            elif more_num == "стільки-то":
                                if to_inflect[y] == 'accs':
                                    to_the_end = " ".join((stck_to_ua[y], noun.inflect({'gent','plur'}).word))
                                else:
                                    to_the_end = " ".join((stck_to_ua[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str_ua[y] + " : " + to_the_end)
                            elif more_num == "мало":
                                if malo_ua[y] == 'немає варіанта':
                                    self.exit_text.append(inflect_str_ua[y] + " : " + malo_ua[y])
                                else:
                                    if to_inflect[y] == 'accs':
                                        to_the_end = " ".join((malo_ua[y], noun.inflect({'gent','plur'}).word))
                                    else:
                                        to_the_end = " ".join((malo_ua[y], noun.inflect({to_inflect[y],'plur'}).word))
                                    self.exit_text.append(inflect_str_ua[y] + " : " + to_the_end)
                            elif more_num == "багато":
                                if to_inflect[y] == 'accs':
                                    to_the_end = " ".join((mnogo_ua[y], noun.inflect({'gent','plur'}).word))
                                else:
                                    to_the_end = " ".join((mnogo_ua[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str_ua[y] + " : " + to_the_end)
                            else: 
                                self.exit_text.setText(" Ошибка: Что-то пошло не так( ")
                    else: 
                        self.exit_text.setText(" Не удалось просклонять данное числительное ")
            else:
                self.exit_text.setText(" Ошибка: Ввод некорректен")
        else:
            self.exit_text.setText(" Ошибка: выбор опций некорректен ")

    def convert_ru(self):
        """General Ru func"""
        noun = self.insert_noun_line 
        num = self.insert_number_line.text()
        noun_str = self.insert_noun_line.text()
        noun = morph.parse(noun_str)[0]
        noun_ord_res = noun.normal_form
        if self.what_number_4.isChecked() and self.what_number_3.checkState() == Qt.Unchecked and self.what_number_2.checkState() == Qt.Unchecked and self.what_number_1.checkState() == Qt.Unchecked:
            if self.num_is_ok(str(self.insert_number_line.text())) == True:
                self.exit_text.append("|--------------------------------------|")
                self.exit_text.append("           Числительное в валюте:           ")
                self.exit_text.append("|--------------------------------------|")
                self.exit_text.append("Значение в рублях: " + self.fln.money(float(num),True))
            else:
                self.exit_text.setText(" Ошибка: Ввод некорректен")
        elif self.what_number_1.isChecked() or self.what_number_2.isChecked() or self.what_number_3.isChecked() and self.what_number_4.checkState() == Qt.Unchecked:
            if self.num_is_ok(str(self.insert_number_line.text())) == True:
                if 'Pltm' not in noun.tag:
                    noun_ord_res = noun.inflect({'sing'}).word
                if '.' in num and self.what_number_1.isChecked() and self.what_number_2.checkState() == Qt.Unchecked and self.what_number_3.checkState() == Qt.Unchecked: # дробные значения
                    num_1 = self.fln.in_words(float(num),True)
                    self.exit_text.append("|--------------------------------------|")
                    self.exit_text.append("   Склонение дробного числительного по падежам:  ")
                    self.exit_text.append("|--------------------------------------|")
                    for x in range(0, 5):
                        inf = (self.rus.inflect_float_num_noun(noun_ord_res,num_1,to_inflect[x]))
                        self.exit_text.append(inflect_str[x] + " : " + inf)
                    self.exit_text.append("|--------------------------------------|")
                elif self.what_number_3.isChecked() and 'Pltm' in noun.tag and self.what_number_1.checkState() == Qt.Unchecked and self.what_number_2.checkState() == Qt.Unchecked:
                    int_num = int(num)
                    cardinal_num = self.rus.number_to_words(int_num) #собирательное
                    num_1 = (self.rus.end_way(self.rus.type_num(int_num),self.rus.corr_num(cardinal_num),int_num)) #собирательное 
                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append(" Собирательное числительное + сущ.: " + self.rus.correct_card_num(int_num,num_1,noun_str)) 
                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append("         Склонение числительного по падежам:       ")
                    self.exit_text.append("|-------------------------------------------------|")
                    sob = re.split(" ",self.rus.correct_card_num(int_num,num_1,noun_str))
                    if sob[0] == 'минус':
                        num_1 = sob[0] + " " + sob[1]
                        noun_ord_res = sob[2]
                    else:
                        num_1 = sob[0]
                        noun_ord_res = sob[1]
                    for x in range(0, 5):
                        inf = (self.rus.inflect_num_noun(num_1,noun_ord_res,to_inflect[x],int_num))
                        self.exit_text.append(inflect_str[x] + " : " + inf)
                    self.exit_text.append("|-------------------------------------------------|")
                elif self.what_number_1.isChecked() and self.what_number_2.checkState() == Qt.Unchecked and self.what_number_3.checkState() == Qt.Unchecked:
                    int_num = int(num)
                    cardinal_num = self.rus.number_to_words(int_num) #количественные
                    num_1 = (self.rus.end_way(self.rus.type_num(int_num),self.rus.corr_num(cardinal_num),int_num)) #количественные 
                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append(" Количественное числительное + сущ.: " + self.rus.correct_card_num(int_num,num_1,noun_str)) 
                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append("         Склонение числительного по падежам:       ")
                    self.exit_text.append("|-------------------------------------------------|")
                    for x in range(0, 5):
                        inf = (self.rus.inflect_num_noun(num_1,noun_ord_res,to_inflect[x],int_num))
                        self.exit_text.append(inflect_str[x] + " : " + inf)
                    self.exit_text.append("|-------------------------------------------------|")
                elif self.what_number_2.isChecked() and self.what_number_1.checkState() == Qt.Unchecked and self.what_number_3.checkState() == Qt.Unchecked:
                    int_num = int(num)
                    ordinal_num = self.rus.number_to_words(self.rus.ordinal(int_num)) #порядковые
                    num_2 = (self.rus.end_way(self.rus.type_num(int_num),self.rus.corr_num(ordinal_num),int_num)) #порядковые
                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append(" Порядковое числительное + сущ.: " + self.rus.correct_ord_num(num_2,noun_ord_res))
                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append("         Склонение числительного по падежам:       ")
                    self.exit_text.append("|-------------------------------------------------|")
                    for x in range(0, 5):
                        inf = (self.rus.inflect_ord_num_noun(num_2,noun_ord_res,to_inflect[x]))
                        self.exit_text.append(inflect_str[x] + " : " + inf)
                    self.exit_text.append("|-------------------------------------------------|")
            elif self.str_is_ok(str(self.insert_number_line.text())) == False: # неопредел колич
                if self.what_number_1.isChecked() and self.what_number_2.checkState() == Qt.Unchecked and self.what_number_3.checkState() == Qt.Unchecked: 
                    more_num = morph.parse(num)[0].normal_form
                    self.exit_text.append("|--------------------------------------|")
                    self.exit_text.append("   Склонение неопределённо-количественного числительного по падежам:  ")
                    self.exit_text.append("|--------------------------------------|")
                    # исправить множественное числоч
                    if more_num in uncount_num:
                        for y in range(0, 5):
                            if more_num == "сколько":
                                to_the_end = " ".join((sck[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif more_num == "сколько-нибудь":
                                to_the_end = " ".join((sck_nbd[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif more_num == "сколько-то":
                                to_the_end = " ".join((scl_to[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif more_num == "несколько":
                                to_the_end = " ".join((nsck[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif more_num == "столько":
                                to_the_end = " ".join((stck[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif more_num == "столько-то":
                                to_the_end = " ".join((stck_to[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif more_num == "мало":
                                if malo[y] == 'нет варианта':
                                    self.exit_text.append(inflect_str[y] + " : " + malo[y])
                                else:
                                    to_the_end = " ".join((malo[y], noun.inflect({to_inflect[y],'plur'}).word))
                                    self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif more_num == "много":
                                to_the_end = " ".join((mnogo[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            else: 
                                self.exit_text.setText(" Ошибка: Что-то пошло не так( ")
                    else: 
                        self.exit_text.setText(" Не удалось просклонять данное числительное ")
            else:
                self.exit_text.setText(" Ошибка: Ввод некорректен")
        else:
            self.exit_text.setText(" Ошибка: выбор опций некорректен ")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())