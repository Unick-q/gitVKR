import ast
import sys
import re
import pymorphy2
from float_nums import in_words
from float_nums import rubles
from typing import Dict, Union

morph = pymorphy2.MorphAnalyzer()

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


ordinal = dict(
    ty="ый",
    ноль="нулевой",один="первый",два="второй",три="третий",четыре="четвертый",шесть="шестой",семь="седьмой",восемь="восьмой",
    сорок="сороковой", пятьдесят="пятидесятый", шестьдесят="шестидесятый",семьдесят="семидесятый",восемьдесят="восьмидесятый",девяносто="девяностый",
    сто="сотый", двести="двухсотый",триста="трёхсотый", четыреста="четырёхсотый",пятьсот="пятисотый", шестьсот="шестисотый",семьсот="семисотый", восемьсот="восмисотый",девятьсот="девятисотый",
    тысяча="тысячный",миллион="миллиoнный",миллиард="миллиaрдный",триллион="триллиoнный",квадриллион="квaдриллионный",квинтиллион="квинтиллиoнный"
)

ordinal_tens = dict(
    тысяча="тысячный",миллион="миллиoнный",миллиард="миллиaрдный",триллион="триллиoнный",квадриллион="квaдриллионный",квинтиллион="квинтиллиoнный"
)

ordinal_suff = "|".join(list(ordinal.keys()))

to_inflect = ["gent","datv","accs","ablt","loct"]

# NUMBERS
(u'один', u'одна', u'одно')
(u'два', u'две')

unit = ["", "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять"]
unit_cardinal = ["", "одна", "две", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять"]
unit_coll = ["", "двое", "трое", "четверо", "пятеро", "шестеро", "семеро", "восьмеро", "девятеро", "десятеро"]
fractions = ["десятый","сотый","тысячная","десятитысячный","стотысячный","милллионный","десятимилллионный","стомилллионный","миллиардный"]
uncount_num = ["сколько","сколько-нибудь","сколько-то","несколько","столько","столько-то"]
sck = ["сколько""сколька","скольку","сколько","скольком","скольке"]
sck_nbd = ["сколько-нибудя","сколько-нибудю","сколько-нибудя","сколько-нибудём","сколько-нибуде"]
scl_to = ["сколько-то","сколько-то","сколько-то","сколько-то","сколько-то"]
nsck = ["нескольких","нескольким","несколько","несколькими","нескольких"]
stck = ["столька","стольку","столько","стольком","стольке"]
stck_to = ["столько-то","столько-то","столько-то","столько-то","столько-то"]

teen = [
    "десять",
    "одиннадцать",
    "двенадцать",
    "тринадцать",
    "четырнадцать",
    "пятнадцать",
    "шестнадцать",
    "семнадцать",
    "восемнадцать",
    "девятнадцать",
]
ten = [
    "",
    "",
    "двадцать",
    "тридцать",
    "сорок",
    "пятьдесят",
    "шестьдесят",
    "семьдесят",
    "восемьдесят",
    "девяносто",
]
hundred = [
    "",
    "сто", 
    "двести",
    "триста", 
    "четыреста",
    "пятьсот", 
    "шестьсот",
    "семьсот", 
    "восемьсот",
    "девятьсот",
]

mill = [
    "",
    " тысяча",
    " миллион",
    " миллиард",
    " триллион",
    " квадриллион",
    " квинтиллион"
]


def_classical = dict(
    all=False, zero=False, herd=False, names=True, persons=False, ancient=False
)

class BadChunkingOptionError(Exception):
    pass

class NumOutOfRangeError(Exception):
    pass

STDOUT_ON = False

def print3(txt):
    if STDOUT_ON:
        print(txt)

class engine:
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
                        pup[x] = morph.parse(pup[x])[0].inflect({"gent"}).word
                else: 
                    a = pup[x]
                    for i in range(1,6):
                        nrm = morph.parse(pup[x])[0].normal_form
                        if nrm == mill[i].replace(' ', ''):
                            pup[x] = a
                            break
                        else:
                            pup[x] = morph.parse(pup[x])[0].inflect({"accs"}).word
                if num % 10 == 1:
                    noun_res = noun_res.inflect({"sing","accs",gen}).word
                elif num % 10 in [2,3,4]:
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
                if num % 10 == 1:
                    noun_res = noun_res.inflect({"sing","accs"}).word #совпадает с именнительым падежом 
                elif num % 10 in [2,3,4]:
                    if 'Pltm' in noun_res.tag:
                        noun_res = noun_res.inflect({"gent"}).word
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
    
    # def inflect_apro_noun(self, noun, apro):

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
        if (('Pltm' in noun_res.tag) and (num % 10 in [1,2,3,4])) or (('anim' in noun_res.tag) and ('gent' in noun_res.tag or 'accs' in noun_res.tag) and ('plur' in noun_res.tag) and (num % 10 in [1,2,3,4])): #нужно брать 2-10 числа и менять на собирательные
            num %= 10
            aka[len(aka) - 1] = unit_coll[num-1]
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
            elif num % 10 >= 2 and num % 10 <= 4 and (num % 100 < 10 or num % 100 >= 20):
                if 'Pltm' in noun_res.tag:
                    noun_res = noun_res.inflect({'gent'}).word
                else:
                    noun_res = noun_res.inflect({'gent','sing'}).word
            else:
                noun_res = noun_res.inflect({'gent','plur'}).word
        total_2 = " ".join((result, noun_res))
        return total_2

    # def start(num, noun_str):
    # p = engine()
    # print("|--------------------------------------|")
    # print("               Введите число            ")
    # print("  Если это определнное значение то - 1  ")
    # print("                 Иначе - 2              ")
    # print("|--------------------------------------|")
    # type_num = int(input())
    # if (type_num != 1) & (type_num != 2):
    #     print(" Error ") 
    #     sys.exit() 
    # elif type_num == 1:
    #     type_num = 0
    # else:
    #     type_num = 1
    # print("|--------------------------------------|")
    # print("             Введите число              ")
    # print("|--------------------------------------|")  
    # num = input()
    # print("|--------------------------------------|")
    # print("         Введите существительное        ")
    # print("|--------------------------------------|")
    # noun_str = input()
    # noun = morph.parse(noun_str)[0]
    # noun_ord_res = noun.normal_form
    # if 'Pltm' not in noun.tag:
    #     noun_ord_res = noun.inflect({'sing'}).word
    # if '.' in num and type_num == 0: # дробные значения
    #     num_1 = in_words(float(num))
    #     print("|--------------------------------------|")
    #     print("           Значение в рублях:           ")
    #     print("|--------------------------------------|")
    #     print(rubles(float(num)))
    #     print("|--------------------------------------|")
    #     print("   Склонение дробного числительного по падежам:  ")
    #     print("|--------------------------------------|")
    #     for x in range(0, 5):
    #         inf = (p.inflect_float_num_noun(noun_ord_res,num_1,to_inflect[x]))
    #         print(to_inflect[x] + " : " + inf)
    #     print("|--------------------------------------|")
    # elif type_num == 0:
    #     int_num = int(num)
    #     cardinal_num = p.number_to_words(int_num) #количественные
    #     ordinal_num = p.number_to_words(p.ordinal(int_num)) #порядковые
    #     num_1 = (p.end_way(p.type_num(int_num),p.corr_num(cardinal_num),int_num)) #количественные 
    #     num_2 = (p.end_way(p.type_num(int_num),p.corr_num(ordinal_num),int_num)) #порядковые
    #     print("|--------------------------------------|")
    #     print("Количественное числительное + сущ.: " + p.correct_card_num(int_num,num_1,noun_str)) 
    #     print("Порядковое числительное + сущ.: " + p.correct_ord_noun(num_2,noun_ord_res,int_num))
    #     num_1_noun = p.correct_card_num(int_num,num_1,noun_str)
    #     num_2_noun = p.correct_ord_noun(num_2,noun_ord_res,int_num)

    #     print("|--------------------------------------|")
    #     print("   Склонение числительного по падежам:  ")
    #     print("|--------------------------------------|")
    #     for x in range(0, 5):
    #         inf = (p.inflect_num_noun(num_1,noun_ord_res,to_inflect[x],int_num))
    #         print(to_inflect[x] + " : " + inf)
    #     print("|--------------------------------------|")
    # else:
    #     more_num = morph.parse(num)[0].normal_form
    #     print(more_num)
    #     for x in range(0, 6):
    #         if uncount_num[x] == more_num:
    #             for y in range(0, 5):
    #                 if x == 0:
    #                     to_the_end = " ".join((sck[y], noun.inflect({to_inflect[y],'plur'}).word))
    #                     print(to_inflect[y] + " : " + to_the_end)
    #                 elif x == 1:
    #                     to_the_end = " ".join((sck_nbd[y], noun.inflect({to_inflect[y],'plur'}).word))
    #                     print(to_inflect[y] + " : " + to_the_end)
    #                 elif x == 2:
    #                     to_the_end = " ".join((scl_to[y], noun.inflect({to_inflect[y],'plur'}).word))
    #                     print(to_inflect[y] + " : " + to_the_end)
    #                 elif x == 3:
    #                     to_the_end = " ".join((nsck[y], noun.inflect({to_inflect[y],'plur'}).word))
    #                     print(to_inflect[y] + " : " + to_the_end)
    #                 elif x == 4:
    #                     to_the_end = " ".join((stck[y], noun.inflect({to_inflect[y],'plur'}).word))
    #                     print(to_inflect[y] + " : " + to_the_end)
    #                 elif x == 5:
    #                     to_the_end = " ".join((stck_to[y], noun.inflect({to_inflect[y],'plur'}).word))
    #                     print(to_inflect[y] + " : " + to_the_end)
    #                 else: 
    #                     print(" Error ")
    # согласуется так же, как и количественные 
    # print("YEs, Work")




# ordinal_num = p.number_to_words(123456, group=1)
# ordinal_num = p.number_to_words(1234, wantlist=True)
# ordinal_num = p.number_to_words(9, threshold=10)  # "nine"
# print(ordinal_num)
# ordinal_num = p.number_to_words(10, threshold=10)  # "ten"
# print(ordinal_num)
# ordinal_num = p.number_to_words(11, threshold=10)  # "11"
# print(ordinal_num)
# ordinal_num = p.number_to_words(1000, threshold=10)  # "1,000"
# print(ordinal_num)
# print(p.ordinal(cardinal_num))

