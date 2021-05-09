import sys
import ast
import re
import pymorphy2
import decimal
from float_nums import in_words
from float_nums import rubles
from typing import Dict, Union
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

morph = pymorphy2.MorphAnalyzer()
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

ordinal_ua = dict(
    ty="ий",
    нуль = "нульовий", один = "перший", два = "другий", три = "третій", чотири = "четвертий", шість = "шостий", сім = "сьомий", вісім = "восьмий",
    сорок = "сороковий", пятдесят = "п'ятдесятий", шістдесят = "шістдесятий", сімдесят = "семидесятих", вісімдесят = "восьмидесятих", девяносто = "дев'яностий",
    сто = "сотий", двісті = "двохсотий", триста = "трьохсот", чотириста = "чотирьохсотий", пятсот = "п'ятисотий", шістсот = "шестисотий", сімсот = "семисотий", вісімсот = "восмісотий", девятсот = "дев'ятисотий",
    тисяча = "тисячний", мільйон = "мілліoнний", мільярд = "мілліaрдний", трильйон = "трілліoнний", квадрильйон = "квaдрілліонний", квінтильйон = "квінтілліoнний"
)

ordinal_tens = dict(
    тысяча="тысячный",миллион="миллиoнный",миллиард="миллиaрдный",триллион="триллиoнный",квадриллион="квaдриллионный",квинтиллион="квинтиллиoнный"
)

ordinal_tens_ua = dict(
    тисяча = "тисячний", мільйон = "мілліoнний", мільярд = "мілліaрдний", трильйон = "трілліoнний", квадрильйон = "квaдрілліонний", квінтильйон = "квінтілліoнний"
)

ordinal_suff = "|".join(list(ordinal.keys()))

to_inflect = ["gent","datv","accs","ablt","loct"]
inflect_str = ["Родительный","Дательный","Винительный","Творительный","Предложный"]

# NUMBERS
(u'один', u'одна', u'одно')
(u'два', u'две')

digits = [2,3,4,5,6,7,8,9]
unit = ["", "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять"]
unit_ua = ["", "один", "два", "три", "чотири", "п'ять", "шість", "сім", "вісім", "дев'ять"]
unit_cardinal = ["", "одна", "две", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять"]
unit_cardinal_ua = ["", "одна", "дві", "три", "чотири", "п'ять", "шість", "сім", "вісім", "дев'ять"]
unit_coll = ["", "двое", "трое", "четверо", "пятеро", "шестеро", "семеро", "восьмеро", "девятеро", "десятеро"]
unit_coll_ua = ["", "двоє", "троє", "четверо", "п'ятеро", "шестеро", "семеро", "восьмеро", "дев'ятеро", "десятеро"]
uncount_num = ["сколько","сколько-нибудь","сколько-то","несколько","столько","столько-то"]
sck = ["сколько""сколька","скольку","сколько","скольком","скольке"]
sck_nbd = ["сколько-нибудя","сколько-нибудю","сколько-нибудя","сколько-нибудём","сколько-нибуде"]
scl_to = ["сколько-то","сколько-то","сколько-то","сколько-то","сколько-то"]
nsck = ["нескольких","нескольким","несколько","несколькими","нескольких"]
stck = ["столька","стольку","столько","стольком","стольке"]
stck_to = ["столько-то","столько-то","столько-то","столько-то","столько-то"]

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
    "сорок","пятдесят","шістдесят",
    "сімдесят","вісімдесят","девяносто",
]

hundred = [
    "","сто","двести","триста","четыреста","пятьсот","шестьсот","семьсот","восемьсот","девятьсот",
]

hundred_ua = [
    "","сто","двісті","триста","чотириста","пятсот","шістсот","сімсот","вісімсот","девятсот",
]

mill = [
    ""," тысяча"," миллион"," миллиард"," триллион"," квадриллион"," квинтиллион"
]

mill_ua = [
    ""," тисяча"," мільйон"," мільярд"," трильйон"," квадрильйон"," квінтильйон"
]


def_classical = dict(all=False, zero=False)

class BadChunkingOptionError(Exception):
    pass

class NumOutOfRangeError(Exception):
    pass

class Example(QWidget):
    class ru_engine:
        def __init__(self):
            self.classical_dict = def_classical.copy()

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
                            # реализация дробных значений,
                            n = int(num[-1])

                        except ValueError:  # ends with '.', so need to use whole string
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
                print3("Заданное число превосходит допустимое значение")
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
            while num:
                num //=1000
                if num > 0:
                    array.append(int(num))
            return array
        
        def end_way(self, array, endstr, num):
            result = []
            if num > 1000 or num < 0:
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
                    if pup[x] == 'один' and x == rang - 1:
                        if 'masc' in noun_res.tag:
                            pup[x] = morph.parse(pup[x])[0].inflect({"gent",'masc'}).word
                        else:
                            pup[x] = morph.parse(pup[x])[0].inflect({"accs",gen}).word
                    elif num % 10 in [2,3,4]:
                        if 'neut' in noun_res.tag and pup[x] == 'два' and x == rang - 1:
                            pup[x] = morph.parse(pup[x])[0].inflect({"nomn",'masc'}).word
                        else:
                            # if 'Pltm' in noun_res.tag and num % 100 in [12,13,14] and num < 100:
                            #     pup[x] = morph.parse(pup[x])[0].inflect({"nomn"}).word
                            if 'Pltm' in noun_res.tag:
                                num %= 10 
                                if pup[len(pup)-1] == unit[num]: 
                                    pup[len(pup)-1] = unit_coll[num-1]
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
                    if num % 10 == 1 and num % 100 not in [11]: 
                        if 'Pltm' in noun_res.tag: 
                            noun_res = noun_res.inflect({"accs"}).word
                        else:
                            noun_res = noun_res.inflect({"sing","accs",gen}).word
                    elif num % 10 in [2,3,4]:
                        if 'Pltm' in noun_res.tag:
                            noun_res = noun_res.inflect({"gent"}).word
                        else:
                            if num % 100 in [12,13,14]:
                                noun_res = noun_res.inflect({"plur","gent"}).word
                            else:
                                noun_res = noun_res.inflect({"sing","gent"}).word
                    else:
                        noun_res = noun_res.inflect({"plur","gent"}).word
                elif ('accs' in typeinf) and ('inan' in noun_res.tag):
                    if pup[x] == 'один' and x == rang - 1:
                        if 'masc' in noun_res.tag:
                            pup[x] = morph.parse(pup[x])[0].inflect({"nomn",'masc'}).word
                        else: 
                            pup[x] = morph.parse(pup[x])[0].inflect({"accs",gen}).word
                    elif num % 10 in [2,3,4]:
                        if 'Pltm' in noun_res.tag:
                            num %= 10 
                            if pup[len(pup)-1] == unit[num]: 
                                pup[len(pup)-1] = unit_coll[num-1]
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
                    if num % 10 == 1 and num % 100 not in [11]:
                        if 'Pltm' in noun_res.tag:
                            noun_res = noun_res.inflect({"gent"}).word
                        else:
                            noun_res = noun_res.inflect({"sing","accs"}).word
                    elif num % 10 in [2,3,4]:
                        if 'Pltm' in noun_res.tag:
                            noun_res = noun_res.inflect({"gent"}).word
                        else:
                            if num % 100 in [12,13,14]:
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
                        else:
                            pup[x] = morph.parse(pup[x])[0].inflect({typeinf}).word
                        noun_res = noun_res.inflect({typeinf,"plur"}).word
                result = "{}".format(" ".join(pup))
                total = " ".join((result, noun_res))
            return total

        def inflect_float_num_noun(self, noun, endstr, typeinf):
            result = []
            tyt = re.split(" ",endstr)
            if endstr == 'одна целая пять десятых':
                tyt = 'полтора'
                noun_res = morph.parse(noun)[0]
                gen = noun_res.tag.gender 
                tyt = morph.parse(tyt)[0].inflect({typeinf}).word
                tyt = morph.parse(tyt)[0].inflect({gen}).word
                noun_res = noun_res.inflect({"gent"}).word
                float_noun = " ".join((tyt, noun_res))
            else:
                for x in range(len(tyt)):  #Добавить полтора и т.д
                    noun_res = morph.parse(noun)[0]
                    if ('accs' in typeinf) and (tyt[x] == 'десятых'): 
                        tyt[x] = 'десятых'
                    else:
                        tyt[x] = morph.parse(tyt[x])[0].inflect({typeinf}).word
                    noun_res = noun_res.inflect({"gent"}).word
                    result = "{}".format(" ".join(tyt))
                    float_noun = " ".join((result, noun_res))
            return float_noun

        
        def correct_ord_noun(self, endstr, noun, num): #порядковое числительное 
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
                print(gen)
                print(olo)
                print(last)
                print(olo[len(olo) - 1])
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
            if (('Pltm' in noun_res.tag) and (num % 10 in digits) or (('anim' in noun_res.tag) and ('gent' in noun_res.tag or 'accs' in noun_res.tag) and ('plur' in noun_res.tag) and (num % 10 in digits))): #нужно брать 2-10 числа и менять на собирательные
                print("Here-1")
                num %= 10
                aka[len(aka) - 1] = unit_coll[num-1] #тут error
                result = "{}".format(" ".join(aka))
                noun_res = noun_res.inflect({'plur','gent'}).word
            else: #Склоняем 1,2 в конце числительного + существителное 
                if aka[len(aka) - 1] == 'один' or aka[len(aka) - 1] == 'два':
                    aka[len(aka) - 1] = morph.parse(aka[len(aka) - 1])[0].inflect({what_gen}).word
                    result = "{}".format(" ".join(aka))
                else:
                    result = endstr
                if num % 10 == 1 and num % 100 != 11:
                    noun_res = noun_res.inflect({'nomn','sing'}).word   #Возможны ошибки 
                elif num % 10 in [2,3,4] and (num % 100 < 10 or num % 100 >= 20):
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
        def __init__(self):
            self.classical_dict = def_classical.copy()

        def ordinal_ua(self, num):
            if re.match(r"\d", str(num)):
                try:
                    num % 2
                    n = num
                except TypeError:
                    if "." in str(num):
                        try:
                            # реализация дробных значений,
                            n = int(num[-1])

                        except ValueError:  # ends with '.', so need to use whole string
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
                    post = ordinal_ua[mo.group(1)]
                    return re.sub(r"(%s)\Z" % ordinal_suff, post, num)
                except AttributeError:
                    return "%sый" % num

        def millfn(self, ind=0):
            if ind > len(mill_ua) - 1:
                print3("Заданное число превосходит допустимое значение")
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
                        r"(%s)\Z" % ordinal_suff, ordinal_ua[mo.group(1)], numchunks[-1]
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
            while num:
                num //=1000
                if num > 0:
                    array.append(int(num))
            return array
        
        def end_way(self, array, endstr, num):
            result = []
            if num > 1000 or num < 0:
                for i in range(len(array)):
                    result = re.sub(mill_ua[i+1],morph_ua.parse(mill_ua[i+1])[0].make_agree_with_number(array[i]).word, endstr)
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
                if ('accs' in typeinf) and ('anim' in noun_res.tag): 
                    if pup[x] == 'один' and x == rang - 1:
                        if 'masc' in noun_res.tag:
                            pup[x] = morph_ua.parse(pup[x])[0].inflect({"gent",'masc'}).word
                        else:
                            pup[x] = morph_ua.parse(pup[x])[0].inflect({"accs",gen}).word
                    elif num % 10 in [2,3,4]:
                        if 'neut' in noun_res.tag and pup[x] == 'два' and x == rang - 1:
                            pup[x] = morph_ua.parse(pup[x])[0].inflect({"nomn",'masc'}).word
                        else:
                            # if 'Pltm' in noun_res.tag and num % 100 in [12,13,14] and num < 100:
                            #     pup[x] = morph_ua.parse(pup[x])[0].inflect({"nomn"}).word
                            if 'Pltm' in noun_res.tag:
                                num %= 10 
                                if pup[len(pup)-1] == unit[num]: 
                                    pup[len(pup)-1] = unit_coll[num-1]
                            else:
                                if pup[len(pup)-1] == "два":
                                    pup[len(pup)-1] = morph_ua.parse(pup[len(pup)-1])[0].inflect({"nomn",gen}).word
                                else:
                                    pup[x] = morph_ua.parse(pup[x])[0].inflect({"nomn"}).word
                    else: 
                        a = pup[x]
                        for i in range(1,6):
                            nrm = morph_ua.parse(pup[x])[0].normal_form
                            if nrm == mill[i].replace(' ', ''):
                                pup[x] = a
                                break
                            else:
                                pup[x] = morph_ua.parse(pup[x])[0].inflect({"accs"}).word
                    if num % 10 == 1 and num % 100 not in [11]: 
                        if 'Pltm' in noun_res.tag: 
                            noun_res = noun_res.inflect({"accs"}).word
                        else:
                            noun_res = noun_res.inflect({"sing","accs",gen}).word
                    elif num % 10 in [2,3,4]:
                        if 'Pltm' in noun_res.tag:
                            noun_res = noun_res.inflect({"gent"}).word
                        else:
                            if num % 100 in [12,13,14]:
                                noun_res = noun_res.inflect({"plur","gent"}).word
                            else:
                                noun_res = noun_res.inflect({"sing","gent"}).word
                    else:
                        noun_res = noun_res.inflect({"plur","gent"}).word
                elif ('accs' in typeinf) and ('inan' in noun_res.tag):
                    if pup[x] == 'один' and x == rang - 1:
                        if 'masc' in noun_res.tag:
                            pup[x] = morph_ua.parse(pup[x])[0].inflect({"nomn",'masc'}).word
                        else: 
                            pup[x] = morph_ua.parse(pup[x])[0].inflect({"accs",gen}).word
                    elif num % 10 in [2,3,4]:
                        if 'Pltm' in noun_res.tag:
                            num %= 10 
                            if pup[len(pup)-1] == unit_ua[num]: 
                                pup[len(pup)-1] = unit_coll_ua[num-1]
                        else:
                            if pup[len(pup)-1] == "два":
                                pup[len(pup)-1] = morph_ua.parse(pup[len(pup)-1])[0].inflect({"nomn",gen}).word
                            else:
                                pup[x] = morph_ua.parse(pup[x])[0].inflect({"nomn"}).word    
                    else:
                        a = pup[x]
                        for i in range(1,6):
                            nrm = morph_ua.parse(pup[x])[0].normal_form
                            if nrm == mill[i].replace(' ', ''):
                                pup[x] = a
                                break
                            else:
                                pup[x] = morph_ua.parse(pup[x])[0].inflect({"accs"}).word
                    if num % 10 == 1 and num % 100 not in [11]:
                        if 'Pltm' in noun_res.tag:
                            noun_res = noun_res.inflect({"gent"}).word
                        else:
                            noun_res = noun_res.inflect({"sing","accs"}).word
                    elif num % 10 in [2,3,4]:
                        if 'Pltm' in noun_res.tag:
                            noun_res = noun_res.inflect({"gent"}).word
                        else:
                            if num % 100 in [12,13,14]:
                                noun_res = noun_res.inflect({"plur","gent"}).word
                            else:
                                noun_res = noun_res.inflect({"sing","gent"}).word
                    else:
                        noun_res = noun_res.inflect({"plur","gent"}).word
                else:
                    if pup[x] == 'один' and x == rang - 1: 
                        noun_res = noun_res.inflect({typeinf,"sing"}).word
                        pup[x] = morph_ua.parse(pup[x])[0].inflect({typeinf,gen}).word
                    else:
                        if pup[x] == 'сто':
                            pup[x] = 'ста'
                        else:
                            print(pup[x])
                            pup[x] = morph_ua.parse(pup[x])[0].inflect({typeinf}).word
                        noun_res = noun_res.inflect({typeinf}).word # убрал "plur"
                result = "{}".format(" ".join(pup))
                total = " ".join((result, noun_res))
            return total

        def inflect_float_num_noun(self, noun, endstr, typeinf):
            result = []
            tyt = re.split(" ",endstr)
            if endstr == 'одна целая пять десятых':
                tyt = 'півтора'
                noun_res = morph_ua.parse(noun)[0]
                gen = noun_res.tag.gender 
                tyt = morph_ua.parse(tyt)[0].inflect({typeinf}).word
                tyt = morph_ua.parse(tyt)[0].inflect({gen}).word
                noun_res = noun_res.inflect({"gent"}).word
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

        
        def correct_ord_noun(self, endstr, noun, num): #порядковое числительное 
            noun = morph_ua.parse(noun)[0]
            result = [] 
            olo = re.split(" ",endstr)
            last = morph_ua.parse(olo[len(olo) - 1])[0]
            gen = noun.tag.gender 
            if 'Pltm' in noun.tag:
                olo[len(olo) - 1] = last.inflect({'plur','nomn'}).word
                result = "{}".format(" ".join(olo))
                total = " ".join((result, noun.normal_form))
            else:
                olo[len(olo) - 1] = last.inflect({'nomn'}).word
                result = "{}".format(" ".join(olo))
                total = " ".join((result, noun.normal_form))
            # else:
            #     total = endstr
            return total
        
        def correct_card_num(self, num, endstr, noun): #собирательные и количественные 
            noun_res = morph_ua.parse(noun)[0]
            print(noun_res)
            what_gen = noun_res.tag.gender
            result = []
            aka = re.split(" ",endstr) #изменить что последняя цифра, а не одна цифра
            if (('Pltm' in noun_res.tag) and (num % 10 in digits) or (('anim' in noun_res.tag) and ('gent' in noun_res.tag or 'accs' in noun_res.tag) and ('plur' in noun_res.tag) and (num % 10 in digits))): #нужно брать 2-10 числа и менять на собирательные
                print("Here-1")
                num %= 10
                aka[len(aka) - 1] = unit_coll[num-1] #тут error
                result = "{}".format(" ".join(aka))
                noun_res = noun_res.inflect({'plur','gent'}).word
            else: #Склоняем 1,2 в конце числительного + существителное 
                if aka[len(aka) - 1] == 'один' or aka[len(aka) - 1] == 'два':
                    aka[len(aka) - 1] = morph_ua.parse(aka[len(aka) - 1])[0].inflect({what_gen}).word
                    result = "{}".format(" ".join(aka))
                else:
                    result = endstr
                if num % 10 == 1 and num % 100 != 11:
                    noun_res = noun_res.inflect({'nomn','sing'}).word   #Возможны ошибки 
                elif num % 10 in [2,3,4] and (num % 100 < 10 or num % 100 >= 20):
                    if 'Pltm' in noun_res.tag:
                        noun_res = noun_res.inflect({'gent'}).word
                    else:
                        if 'plur' in noun_res.tag:
                            noun_res = noun_res.inflect({'gent','sing'}).word
                        else: 
                            noun_res = noun_res.inflect({'gent'}).word
                else:
                    noun_res = noun_res.inflect({'gent','plur'}).word
            total_2 = " ".join((result, noun_res))
            return total_2

    def __init__(self):
        super().__init__()
        self.rus = self.ru_engine()
        self.ua = self.ua_engine()

        # start button
        self.go_button = QPushButton('&Start')

        # line for inserting
        # self.insert_number_line = QDoubleSpinBox()
        # self.insert_number_line.setRange(0, 2147483647)
        # self.insert_number_line.editingFinished.connect(self.convert)

        # for testing validator==================
        self.insert_number_line = QLineEdit()
        self.validator = QRegExpValidator(QRegExp(r'\d{1,7}\.\d{1,2}'), self)
        self.insert_number_line.setValidator(self.validator)

        self.insert_noun_line = QLineEdit()
        self.validator = QRegExpValidator(QRegExp("[а-яА-Я\\s]+"), self)
        self.insert_noun_line.setValidator(self.validator)

        # language list
        self.language_title = QLabel('Language:')
        self.number_title = QLabel('Number:')
        self.what_number_1 = QCheckBox('Numeral')
        self.what_number_2 = QCheckBox('Indefinite')
        self.what_number_3 = QCheckBox('Money')
        self.noun_title = QLabel('Noun:')
        self.language = QComboBox()
        self.language.setFixedWidth(70)
        self.language.addItem('En')
        self.language.addItem('Ru')
        self.language.addItem('Ua')

        # exit text
        self.exit_text = QTextEdit()
        # self.exit_text.setEnabled(0)

        self.initui()

    def change_separator(self):
        if self.language.currentText() == "En":
            self.insert_number_line.setText("")
            self.exit_text.setText("")
            self.validator = QRegExpValidator(QRegExp(r'\d{1,7}\.\d{1,5}'), self)
            self.insert_number_line.setValidator(self.validator)
            self.insert_noun_line.setText("")
            self.exit_text.setText("")
            self.validator = QRegExpValidator(QRegExp("[а-яА-Я\\s]+"), self)
            self.insert_noun_line.setValidator(self.validator)
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
            self.validator = QRegExpValidator(QRegExp('[а-яА-Я0-9.-\\s]+'), self)
            self.insert_number_line.setValidator(self.validator)
            self.insert_noun_line.setText("")
            self.exit_text.setText("")
            self.validator = QRegExpValidator(QRegExp("[а-яА-Я\\s]+"), self)
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
        grid.addWidget(self.noun_title, 4, 0, 1, 4)
        grid.addWidget(self.insert_noun_line, 4, 1, 1, 4)
        grid.addWidget(self.exit_text, 5, 0, 1, 5)
        self.setLayout(grid)

        self.setGeometry(70, 70, 550, 300)
        self.setWindowTitle('Convert number to text')
        self.show()

        self.language.currentIndexChanged.connect(self.change_separator)
        # self.insert_number_line.textEdited.connect(self.convert)

        self.go_button.clicked.connect(self.convert)

    def convert(self):
        self.exit_text.setText("")

        self.number = []

        self.insert_number = self.insert_number_line.text().replace(',', '.')
        

        for arg in self.insert_number.split("."):
            self.number.append(arg)
        if (len(self.number)) == 1:
            self.number.append("00")
        if self.number[1] == '':
            self.number[1] = "00"
        if self.number[0] == '':
            self.number[0] = "00"

        if self.language.currentText() == "Ua":
            self.convert_ua(self.number)
        
        if self.language.currentText() == "Ru":
            self.convert_ru()

        if self.language.currentText() == "En":
            self.convert_en(self.number)
    
    def num_is_ok(self,text):
        try:
            float(text)
            return True
        except ValueError:
            return False

    def str_is_ok(self,text):
        match = re.match("[а-яА-Я]-", text)
        return bool(match)

    def convert_ua(self, number):
        """General Ua func"""
        noun = self.insert_noun_line 
        num = self.insert_number_line.text()
        noun_str = self.insert_noun_line.text()
        noun = morph.parse(noun_str)[0]
        noun_ord_res = noun.normal_form
        if self.num_is_ok(str(self.insert_number_line.text())) == True:
            if self.what_number_3.isChecked() and self.what_number_2.checkState() == Qt.Unchecked and self.what_number_1.checkState() == Qt.Unchecked:
                self.exit_text.append("|--------------------------------------|")
                self.exit_text.append("           Числительное в валюте:           ")
                self.exit_text.append("|--------------------------------------|")
                # self.exit_text.append("Значение в рублях: " + rubles(float(num)))
                coin = number[1]
                if int(coin) > 9:
                    coin = coin[1]
                coin = int(coin)

                if int(number[0]) == 1 and int(number[1]) == 0:
                    self.exit_text.setText("одна гривня")
                elif (int(number[0][-1]) == 2  or int(number[0][-1]) == 3 or int(number[0][-1]) == 4) and int(number[1]) == 0:
                    self.exit_text.setText(self.int_to_ua(int(number[0])) + " гривні")
                else:
                    self.exit_text.setText(
                    self.int_to_ua(int(number[0])) + " гривень")

                    self.uah = self.exit_text.toPlainText()

                    if int(number[0]) == 0 and int(number[1]) != 0:
                        if coin == 1 and int(number[1]) != 11:
                            self.exit_text.setText(self.int_to_ua(int(number[1])) + " копійка")
                        elif int(coin) == 4 or int(coin) == 3 or int(coin) == 2:
                            if int(number[1]) == 14 or int(number[1]) == 13 or int(number[1]) == 12 or int(number[1]) == 11:
                                self.exit_text.setText(self.int_to_ua(int(number[1])) + " копійок")
                            else:
                                self.exit_text.setText(self.int_to_ua(int(number[1])) + " копійки")
                        else:
                            self.exit_text.setText(self.int_to_ua(int(number[1])) + " копійок")
                    else:
                        if coin == 1 and int(number[1]) != 11:
                            self.exit_text.setText(
                                self.uah + " та " +
                                self.int_to_ua(int(number[1])) + " копійка")
                        elif int(coin) == 4 or int(coin) == 3 or int(coin) == 2:
                            if int(number[1]) == 14 or int(number[1]) == 13 or int(number[1]) == 12 or int(number[1]) == 11:
                                self.exit_text.setText(
                                    self.uah + " та " +
                                    self.int_to_ua(int(number[1])) + " копійок")
                            else:
                                self.exit_text.setText(
                                    self.uah + " та " +
                                    self.int_to_ua(int(number[1])) + " копійки")
                        else:
                            if int(number[1]) != 0:
                                self.exit_text.setText(
                                    self.uah + " та " +
                                    self.int_to_ua(int(number[1])) + " копійок")
            elif self.what_number_1.isChecked() and self.what_number_2.checkState() == Qt.Unchecked and self.what_number_3.checkState() == Qt.Unchecked:
                if 'Pltm' not in noun.tag:
                    noun_ord_res = noun.inflect({'sing'}).word
                if '.' in num and self.what_number_1.isChecked() and self.what_number_2.checkState() == Qt.Unchecked: # дробные значения
                    num_1 = in_words(float(num))
                    self.exit_text.append("|--------------------------------------|")
                    self.exit_text.append("   Склонение дробного числительного по падежам:  ")
                    self.exit_text.append("|--------------------------------------|")
                    for x in range(0, 5):
                        inf = (self.ua.inflect_float_num_noun(noun_ord_res,num_1,to_inflect[x]))
                        self.exit_text.append(inflect_str[x] + " : " + inf)
                    self.exit_text.append("|--------------------------------------|")
                elif self.what_number_1.isChecked() and self.what_number_2.checkState() == Qt.Unchecked:
                    int_num = int(num)
                    cardinal_num = self.ua.number_to_words(int_num) #количественные
                    ordinal_num = self.ua.number_to_words(self.ua.ordinal_ua(int_num)) #порядковые
                    num_1 = (self.ua.end_way(self.ua.type_num(int_num),self.ua.corr_num(cardinal_num),int_num)) #количественные 
                    num_2 = (self.ua.end_way(self.ua.type_num(int_num),self.ua.corr_num(ordinal_num),int_num)) #порядковые
                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append("Количественное числительное + сущ.: " + self.ua.correct_card_num(int_num,num_1,noun_str)) 
                    self.exit_text.append("Порядковое числительное + сущ.: " + self.ua.correct_ord_noun(num_2,noun_ord_res,int_num))
                    num_1_noun = self.ua.correct_card_num(int_num,num_1,noun_str)
                    num_2_noun = self.ua.correct_ord_noun(num_2,noun_ord_res,int_num)

                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append("         Склонение числительного по падежам:       ")
                    self.exit_text.append("|-------------------------------------------------|")
                    for x in range(0, 5):
                        inf = (self.ua.inflect_num_noun(num_1,noun_ord_res,to_inflect[x],int_num))
                        self.exit_text.append(inflect_str[x] + " : " + inf)
                    self.exit_text.append("|-------------------------------------------------|")
                else:
                    self.exit_text.setText(" Error: can't do this")
            elif self.what_number_2.isChecked() or self.what_number_3.isChecked():
                self.exit_text.setText(" Error: not correct choice")
            else: 
                self.exit_text.setText(" Error: choose what are we goona do")
        elif self.str_is_ok(str(self.insert_number_line.text())) == False:
            if self.what_number_2.isChecked() and self.what_number_1.checkState() == Qt.Unchecked and self.what_number_3.checkState() == Qt.Unchecked:
                more_num = morph.parse(num)[0].normal_form
                self.exit_text.append("|--------------------------------------|")
                self.exit_text.append("   Склонение неопределённо-количественного числительного по падежам:  ")
                self.exit_text.append("|--------------------------------------|")
                for x in range(0, 6):
                    if uncount_num[x] == more_num:
                        for y in range(0, 5):
                            if x == 0:
                                to_the_end = " ".join((sck[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif x == 1:
                                to_the_end = " ".join((sck_nbd[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif x == 2:
                                to_the_end = " ".join((scl_to[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif x == 3:
                                to_the_end = " ".join((nsck[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif x == 4:
                                to_the_end = " ".join((stck[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif x == 5:
                                to_the_end = " ".join((stck_to[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            else: 
                                self.exit_text.setText(" Error ")
            elif self.what_number_1.isChecked() or self.what_number_3.isChecked():
                    self.exit_text.setText(" Error: can't do this")
            else:
                self.exit_text.setText(" Error: choose what are we goona do")
        else:
            self.exit_text.setText(" Error : Your input is incorrect")

    def convert_ru(self):
        """General Ru func"""
        noun = self.insert_noun_line 
        num = self.insert_number_line.text()
        noun_str = self.insert_noun_line.text()
        noun = morph.parse(noun_str)[0]
        noun_ord_res = noun.normal_form
        if self.num_is_ok(str(self.insert_number_line.text())) == True:
            if self.what_number_3.isChecked() and self.what_number_2.checkState() == Qt.Unchecked and self.what_number_1.checkState() == Qt.Unchecked:
                self.exit_text.append("|--------------------------------------|")
                self.exit_text.append("           Числительное в валюте:           ")
                self.exit_text.append("|--------------------------------------|")
                self.exit_text.append("Значение в рублях: " + rubles(float(num)))
            elif self.what_number_1.isChecked() and self.what_number_2.checkState() == Qt.Unchecked and self.what_number_3.checkState() == Qt.Unchecked:
                if 'Pltm' not in noun.tag:
                    noun_ord_res = noun.inflect({'sing'}).word
                if '.' in num and self.what_number_1.isChecked() and self.what_number_2.checkState() == Qt.Unchecked: # дробные значения
                    num_1 = in_words(float(num))
                    self.exit_text.append("|--------------------------------------|")
                    self.exit_text.append("   Склонение дробного числительного по падежам:  ")
                    self.exit_text.append("|--------------------------------------|")
                    for x in range(0, 5):
                        inf = (self.rus.inflect_float_num_noun(noun_ord_res,num_1,to_inflect[x]))
                        self.exit_text.append(inflect_str[x] + " : " + inf)
                    self.exit_text.append("|--------------------------------------|")
                elif self.what_number_1.isChecked() and self.what_number_2.checkState() == Qt.Unchecked:
                    int_num = int(num)
                    cardinal_num = self.rus.number_to_words(int_num) #количественные
                    ordinal_num = self.rus.number_to_words(self.rus.ordinal(int_num)) #порядковые
                    num_1 = (self.rus.end_way(self.rus.type_num(int_num),self.rus.corr_num(cardinal_num),int_num)) #количественные 
                    num_2 = (self.rus.end_way(self.rus.type_num(int_num),self.rus.corr_num(ordinal_num),int_num)) #порядковые
                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append("Количественное числительное + сущ.: " + self.rus.correct_card_num(int_num,num_1,noun_str)) 
                    self.exit_text.append("Порядковое числительное + сущ.: " + self.rus.correct_ord_noun(num_2,noun_ord_res,int_num))
                    num_1_noun = self.rus.correct_card_num(int_num,num_1,noun_str)
                    num_2_noun = self.rus.correct_ord_noun(num_2,noun_ord_res,int_num)

                    self.exit_text.append("|-------------------------------------------------|")
                    self.exit_text.append("         Склонение числительного по падежам:       ")
                    self.exit_text.append("|-------------------------------------------------|")
                    for x in range(0, 5):
                        inf = (self.rus.inflect_num_noun(num_1,noun_ord_res,to_inflect[x],int_num))
                        self.exit_text.append(inflect_str[x] + " : " + inf)
                    self.exit_text.append("|-------------------------------------------------|")
                else:
                    self.exit_text.setText(" Error: can't do this")
            elif self.what_number_2.isChecked() or self.what_number_3.isChecked():
                self.exit_text.setText(" Error: not correct choice")
            else: 
                self.exit_text.setText(" Error: choose what are we goona do")
        elif self.str_is_ok(str(self.insert_number_line.text())) == False:
            if self.what_number_2.isChecked() and self.what_number_1.checkState() == Qt.Unchecked and self.what_number_3.checkState() == Qt.Unchecked:
                more_num = morph.parse(num)[0].normal_form
                self.exit_text.append("|--------------------------------------|")
                self.exit_text.append("   Склонение неопределённо-количественного числительного по падежам:  ")
                self.exit_text.append("|--------------------------------------|")
                for x in range(0, 6):
                    if uncount_num[x] == more_num:
                        for y in range(0, 5):
                            if x == 0:
                                to_the_end = " ".join((sck[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif x == 1:
                                to_the_end = " ".join((sck_nbd[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif x == 2:
                                to_the_end = " ".join((scl_to[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif x == 3:
                                to_the_end = " ".join((nsck[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif x == 4:
                                to_the_end = " ".join((stck[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            elif x == 5:
                                to_the_end = " ".join((stck_to[y], noun.inflect({to_inflect[y],'plur'}).word))
                                self.exit_text.append(inflect_str[y] + " : " + to_the_end)
                            else: 
                                self.exit_text.setText(" Error ")
            elif self.what_number_1.isChecked() or self.what_number_3.isChecked():
                    self.exit_text.setText(" Error: can't do this")
            else:
                self.exit_text.setText(" Error: choose what are we goona do")
        else:
            self.exit_text.setText(" Error : Your input is incorrect")



    def convert_en(self, number):
        self.exit_text.append("|--------------------------------------|")
        self.exit_text.append("           Числительное в валюте:           ")
        self.exit_text.append("|--------------------------------------|")

        if int(number[0]) == 0 and int(number[1]) == 0:
            self.exit_text.setText("zero dollar")
        else:
            if int(number[0]) == 1:
                self.exit_text.setText("one dollar")
            else:
                self.exit_text.setText(
                    self.int_to_en(int(number[0])) + " dollars")
            if int(number[0]) == 0 and int(number[1]) != 0:
                if int(number[1]) == 1:
                    self.exit_text.setText("one cent")
                else:
                    self.dollars = self.exit_text.toPlainText()
                    self.exit_text.setText(
                        self.int_to_en(int(number[1])) + " cents")

            else:
                if int(number[1]) == 1:
                    self.dollars = self.exit_text.toPlainText()
                    self.exit_text.setText(self.dollars + " and one cent")
                else:
                    if int(number[1]) != 0:
                        self.dollars = self.exit_text.toPlainText()
                        self.exit_text.setText(
                            self.dollars + " and " +
                            self.int_to_en(int(number[1])) + " cents")

    def int_to_en(self, num):
        """convert int value to en text"""

        d = {
            0: 'zero',
            1: 'one',
            2: 'two',
            3: 'three',
            4: 'four',
            5: 'five',
            6: 'six',
            7: 'seven',
            8: 'eight',
            9: 'nine',
            10: 'ten',
            11: 'eleven',
            12: 'twelve',
            13: 'thirteen',
            14: 'fourteen',
            15: 'fifteen',
            16: 'sixteen',
            17: 'seventeen',
            18: 'eighteen',
            19: 'nineteen',
            20: 'twenty',
            30: 'thirty',
            40: 'forty',
            50: 'fifty',
            60: 'sixty',
            70: 'seventy',
            80: 'eighty',
            90: 'ninety'
        }
        k = 1000
        m = k * 1000
        b = m * 1000
        t = b * 1000

        assert (0 <= num)

        if num < 20:
            return d[num]

        if num < 100:
            if num % 10 == 0:
                return d[num]
            else:
                return d[num // 10 * 10] + '-' + d[num % 10]

        if num < k:
            if num % 100 == 0:
                return d[num // 100] + ' hundred'
            else:
                return d[num // 100] + ' hundred and ' + self.int_to_en(
                    num % 100)

        if num < m:
            if num % k == 0:
                return self.int_to_en(num // k) + ' thousand'
            else:
                return self.int_to_en(
                    num // k) + ' thousand, ' + self.int_to_en(num % k)

        if num < b:
            if (num % m) == 0:
                return self.int_to_en(num // m) + ' million'
            else:
                return self.int_to_en(
                    num // m) + ' million, ' + self.int_to_en(num % m)

        if num < t:
            if (num % b) == 0:
                return self.int_to_en(num // b) + ' billion'
            else:
                return self.int_to_en(
                    num // b) + ' billion, ' + self.int_to_en(num % b)

        if num % t == 0:
            return self.int_to_en(num // t) + ' trillion'
        else:
            return self.int_to_en(num // t) + ' trillion, ' + self.int_to_en(
                num % t)

            # ======================= Ua section ===============

    ua_units = (u'нуль', (u'одна', u'одна'), (u'два', u'дві'), u'три', u'чотири',
             u"п'ять", u'шість', u'сім', u'вісім', u"дев'ять")

    teens = (u'десять', u'одинадцять', u'дванадцять', u'тринадцять',
             u'чотирнадцять', u"п'ятнадцять", u'шістнадцять', u'сімнадцять',
             u'вісімнадцять', u"дев'ятнадцять")

    tens = (teens, u'двадцять', u'тридцять', u'сорок', u'пятдесят',
            u'шістдесят', u'сімдесят', u'вісімдесят', u"дев'яносто")

    hundreds = (u'сто', u'двісті', u'триста', u'чотириста', u"п'ятсот",
                u'шістсот', u'сімсот', u'вісімсот', u"дев'ятсот")

    orders = (
        ((u'тисяча', u'тисячі', u'тисяч'), 'f'),
        ((u'мільйон', u'мільйона', u'мільйонів'), 'm'),
        ((u'мільярд', u'мільярда', u'мільярдів'), 'm'),
    )

    def thousand(self, rest, sex):
        """Converts numbers from 19 to 999"""
        prev = 0
        plural = 2
        name = []
        use_teens = 10 <= rest % 100 <= 19
        if not use_teens:
            data = ((self.ua_units, 10), (self.tens, 100), (self.hundreds, 1000))
        else:
            data = ((self.tens, 10), (self.hundreds, 1000))
        for names, x in data:
            cur = int(((rest - prev) % x) * 10 / x)
            prev = rest % x
            if x == 10 and use_teens:
                plural = 2
                name.append(self.teens[cur])
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
                name.append(names[cur - 1])
        return plural, name

    def int_to_ua(self, num, main_units=((u'', u'', u''), 'm')):
        _orders = (main_units,) + self.orders
        if num == 0:
            return ' '.join((self.ua_units[0], _orders[0][0][2])).strip()

        rest = abs(num)
        ord = 0
        name = []
        while rest > 0:
            plural, nme = self.thousand(rest % 1000, _orders[ord][1])
            if nme or ord == 0:
                name.append(_orders[ord][0][plural])
            name += nme
            rest = int(rest / 1000)
            ord += 1

        name.reverse()
        return ' '.join(name).strip()

    def decimal2text(self,
                     value,
                     places=2,
                     int_units=(('', '', ''), 'm'),
                     exp_units=(('', '', ''), 'm')):
        value = decimal.Decimal(value)
        q = decimal.Decimal(10) ** -places

        integral, exp = str(value.quantize(q)).split('.')
        return u'{} {}'.format(
            self.int_to_ua(int(integral), int_units),
            self.int_to_ua(int(exp), exp_units))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())