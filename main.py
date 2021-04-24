# TODO 
# Осталось доработать стилистический вывод с собирательными существительными 
# Добавить склонение порядковых числительных + слитное написание 
# Внедрить имеющуюся программу разбора текстов на числительные 

else:
                # print(noun_res)
                # print(pup[x])
                # noun_res = noun_res.inflect({typeinf,"plur"}).word
                # pup[x] = morph.parse(pup[x])[0].inflect({typeinf}).word
                if pup[x] == 'один' and x == rang - 1: 
                    print("Here-3") #Доходит когда уже исправили на множ число
                    if 'NOUN' in noun_res.tag:
                        print("Here-3.1")
                        noun_res = noun_res.inflect({typeinf,"sing"}).word
                        pup[x] = morph.parse(pup[x])[0].inflect({typeinf,gen}).word
                    else:
                        print("Here-3.2")
                        x = morph.parse(noun_res)[0]
                        print(x)
                        x = x.inflect({typeinf,"sing"}).word
                        print(x)
                        pup[x] = morph.parse(pup[x])[0].inflect({typeinf,gen}).word
                        noun_res = x
                else:
                    print("Here-4")
                    if 'NOUN' in noun_res.tag:
                        print("Here-4.1")
                        noun_res = noun_res.inflect({typeinf,"plur"}).word
                        pup[x] = morph.parse(pup[x])[0].inflect({typeinf}).word
                    else: 
                        print("Here-4.2")
                        x = morph.parse(noun_res)[0]
                        print(x)
                        x = x.inflect({typeinf,"sing"}).word
                        print(x)
                        pup[x] = morph.parse(pup[x])[0].inflect({typeinf,gen}).word
                        noun_res = x


def inflect_num_noun(self, endstr, noun, typeinf, num): #склонение 
        result = []
        noun_res = morph.parse(noun)[0]
        print(noun_res)
        pup = re.split(" ",endstr)
        rang = len(pup)
        gen = noun_res.tag.gender
        # Полностью переделать под accs
        for x in range(len(pup)):
            print(noun_res)
            if ('accs' in typeinf) and ('anim' in noun_res.tag): 
                print("Here-1")
                if 'masc' in noun_res.tag:
                    pup[x] = morph.parse(pup[x])[0].inflect({"gent",'masc'}).word
                else: 
                    pup[x] = morph.parse(pup[x])[0].inflect({"accs",gen}).word
                if num % 10 == 1:
                    noun_res = noun_res.inflect({"sing","accs",gen}).word
                elif num % 10 in [2,3,4]:
                    noun_res = noun_res.inflect({"plur","gent"}).word
            elif ('accs' in typeinf) and ('inan' in noun_res.tag):
                print("Here-2")
                if 'masc' in noun_res.tag:
                    pup[x] = morph.parse(pup[x])[0].inflect({"nomn",'masc'}).word
                else:
                    pup[x] = morph.parse(pup[x])[0].inflect({"accs",gen}).word
                if num % 10 == 1:
                    noun_res = noun_res.inflect({"sing","accs"}).word #совпадает с именнительым падежом 
                elif num % 10 in [2,3,4]:
                    noun_res = noun_res.inflect({"sing","gent"}).word
                else:
                    noun_res = noun_res.inflect({"plur","gent"}).word
            else:
                print(noun_res)
                if pup[x] == 'один' and x == rang - 1: #Доходит когда уже исправили на множ число
                    # print("Here-3")
                    noun_res = noun_res.inflect({typeinf,"sing"}).word
                    pup[x] = morph.parse(pup[x])[0].inflect({typeinf,gen}).word
                else:
                    print("Here-4")
                    noun_res = noun_res.inflect({typeinf,"plur"}).word
                    pup[x] = morph.parse(pup[x])[0].inflect({typeinf}).word
            result = "{}".format(" ".join(pup))
            total = " ".join((result, noun_res))
        return total
        




# import constant


# def getNumber():
#     while True:
#         getNum = input('Введите целое положительное число: ')  # перевели строку в int
#         if getNum.isdigit() : return getNum
# #print(int(getNumber()))

# unitNumber = {
#     '1': UNUS,
#     '2','3','4': SMALL,
#     '0','5','6','7','8','9': BIG2,
# }

# if getNumber()):
#     if (int(getNumber()) % 100) / 10 == 1:
#         scl = BIG2
#     elif (getNumber() % 10) in unitNumber:
#         num = unitNumber[etNumber()]
# else 
#     i = 0
    


# #print(constant.MAXUNUS)
# #print(constant.MAXSMALL)
# #print(constant.MAXBIG1)






# for x in range(len(pup)):
#             if 'anim' in noun.tag:
#                 if 'accs' in typeinf:
#                     pup[x] = morph.parse(pup[x])[0].inflect({"gent"}).word
#                     if num % 10 in [1,2,3,4]:
#                         print('YES_1')
#                         noun = noun.inflect({"sing","gent"}).word
#                     else:
#                         print('YES_2')
#                         noun = noun.inflect({"plur","gent"}).word
#                 else:
#                     pup[x] = morph.parse(pup[x])[0].inflect({typeinf}).word
#             # elif "Pltm"
#             else:
#                 pup[x] = morph.parse(pup[x])[0].inflect({typeinf}).word
#             if ('accs' in typeinf) and ('anim' in noun.tag): 
#                 if num % 10 in [1,2,3,4]:
#                     print('YES_1')
#                     noun = noun.inflect({"sing","gent"}).word
#                 else:
#                     print('YES_2')
#                     noun = noun.inflect({"plur","gent"}).word
#             elif ('accs' in typeinf) and ('inan' in noun.tag): 
#                 print('YES_3')
#                 noun = noun.inflect({"nomn"}).word
#                 # if #Можно добавить проверку на число по файлу который скинули, также добавить правильное числительное
#                 # print('YES_1')
#                 # if 'femn' in noun.tag:
#                 #     noun = noun.inflect({"plur","gent","femn"}).word
#                 # elif 'masc' in noun.tag:
#                 #     noun = noun.inflect({"plur","gent","masc"}).word
#                 # elif 'neut' in noun.tag:
#             #     noun = noun.inflect({"plur","gent"}).word
#             # elif ('accs' in typeinf) and ('inan' in noun.tag): 
#             #     print('YES_2')
#             #     noun = noun.inflect({"nomn"}).word
#             else:
#                 print('YES_4')
#                 if num % 10 == 1:
#                     noun = noun.inflect({typeinf,"sing"}).word
#                 else:
#                     print(noun.inflect({typeinf,"plur"}).word)
#                     noun = noun.inflect({typeinf,"plur"}).word



import pymorphy2


text_to_number = {'один': 1, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5,
                  'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9, 'десять': 10,
                  'одиннадцать': 11, 'двенадцать': 12, 'тринадцать': 13, 'четырнадцать': 14,
                  'пятнадцать': 15, 'шестнадцать': 16, 'семнадцать': 17, 'восемнадцать': 18,
                  'девятнадцать': 19, 'двадцать': 20, 'тридцать': 30, 'сорок': 40, 'пятьдесят': 50,
                  'шестьдесят': 60, 'семьдесят': 70, 'восемьдесят': 80, 'двевяносто': 90, 'сто': 100,
                  'двести': 200, 'триста': 300, 'четыреста': 400, 'пятьсот': 500, 'шестьсот': 600,
                  'семьсот': 700, 'воемьсот': 800, 'девятьсот': 900, 'тысяча': 1000, 'миллион': 1000000,
                  'миллиард': 1000000000, 'косарь': 1000, 'штука': 1000, 'лям': 1000000, 'сотка': 100,
                  'сотня': 100, 'лимон': 1000000, 'пол-ляма': 500000, 'пол-лимона': 500000, 'полсотни': 50,
                  'стопятьсот': 100500}


def get_key(dic, value):
    ''' Allows to get key from the dict using it's value.'''

    for k, v in dic.items():
        if v == value:
            return k



def make_word(text, c=0):
    """ Returns  numeral as compound natural number
        :type text: list
        :param text: a text to be modified.
        :type c: int
        :param c: a parameter to tell us if it is a compound number.
        Example
            >>> make_word(['двенадцать'])
            >>> [12]
            >>> make_word(['сто', 'тридцать', 'два'], c=1)
            >>> [132]
    """
    if c == 0:
        return ([text_to_number.get(text[i]) for i in range(len(text))])

    else: return [sum(text_to_number.get(text[i]) for i in range(len(text)))]



def find_nums(sent):
    morph = pymorphy2.MorphAnalyzer()

    words_after_numrs = ['рубль', 'бакс', 'штук']
    other = ['стопятьсот','один', 'штука', 'косарь', 'тысяча', 'сто', 'сотка', 'сотня', 'лям', 'лимон', 'миллион', 'миллиард']
    half_cases = ['пол-ляма', 'пол-лимона', 'полсотни']  # they have other normal forms


    new_list = []
    compound = []
    i =0

    while i<len(sent):

        if 'NUMB' in morph.parse(sent[i])[0].tag:  # check if it is a number like 10.5 or 3
            new_list.append(get_key(text_to_number, int(float(sent[i]))))

        # check slang and some controversial moments
        elif morph.parse(sent[i])[0].normalized.word in other or 'NUMR' in morph.parse(sent[i])[0].normalized.tag:

            # last word
            if (i==len(sent)-1 and morph.parse(sent[i - 1])[0].normalized.word == 'за') or \
                    (i == len(sent) - 1 and 'NUMR' in morph.parse(sent[i])[0].normalized.tag):

                new_list.append(morph.parse(sent[i])[0].normalized.word)

            # gent or dollars after
            elif i<len(sent)-1 and (morph.parse(sent[i + 1])[0].normalized.word in words_after_numrs or 'gent' in morph.parse(sent[i + 1])[0].tag):

                new_list.append(morph.parse(sent[i])[0].normalized.word)


            elif i<len(sent)-1 and 'NUMR' in morph.parse(sent[i])[0].normalized.tag:

                new_list.append(morph.parse(sent[i])[0].normalized.word)

            elif i<len(sent)-1 and (morph.parse(sent[i])[0].normalized.word in other or 'NUMR' in morph.parse(sent[i+1])[0].normalized.tag):
                k=0

                while 'NUMR' in morph.parse(sent[i + k])[0].normalized.tag or sent[i + k] in other or sent[i + k] == 'один':

                    k += 1
                    if i + k >= len(sent): break

                if k > 1:

                    for j in range(k):
                        compound.append(morph.parse(sent[i + j])[0].normalized.word)


                i=i+k


        # check some other cases as they have a special normal form
        elif sent[i] in half_cases or sent[i] in other:
            if (i == len(sent) - 1 and morph.parse(sent[i - 1])[0].normalized.word == 'за') or\
                    (i < len(sent) - 1 and ('gent' in morph.parse(sent[i + 1])[0].tag or morph.parse(sent[i + 1])[0].normalized.word in words_after_numrs)):

                new_list.append(sent[i])
        i+=1



    if new_list:
        print(make_word(new_list))
    elif compound: print(make_word(compound, c=1))
    else: print("there are no mumericals")



if __name__ == '__main__':


    all = ["Я совсем один",
           "Я закончил третий курс и пошел на четвертый",
           "У меня только сто тридцать один",
           "Мне нравится когда моя машина, стоимостью сотку штук баксов, мелькает по телевизору",
           "Я хочу квартиру за 10.5 миллионов",
           "Я купил ее за косарь",
           "Купил машину за пол-лимона",
           "Отрежь мне огурец и пол-лимона",
           "У тебя было стопятьсот причин",
           "Дай мне два яблока",
           "Дай мне пол-ляма рублей",
           "Дай мне полсотни яблок"]

    for i in range(len(all)):
        thesent = all[i].split()
        print(thesent)
        print('nums: ', end=' ')
        find_nums(thesent)
        print()
