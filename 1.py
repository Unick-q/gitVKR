def days_ago(self):
    """Возвращает количество прошедших дней с последнего входа пользователя"""
    if self.created:
        result = (datetime.datetime.utcnow() - self.created).days
        if result < 1:
            return 'сегодня'
        elif result >= 1 and result < 2:
            return 'вчера'
        elif result >= 2 and result < 3:
            return 'позавчера'
        elif result % 10 == 1 and result % 100 != 11:
            return str(result) + ' день назад'
        elif result % 10 in [2, 3, 4] and result % 100 not in [12, 13, 14]:
            return str(result) + ' дня назад'
        elif result % 10 == 0 or result % 10 in [5, 6, 7, 8, 9] or result % 100 in [11, 12, 13, 14]:
            return str(result) + ' дней назад'
        return result
    else:
        return 'никогда'



#Склонения слова 
import pymorphy2
 
word = input().strip()
morph = pymorphy2.MorphAnalyzer()
word = morph.parse(word)[0]
cases = (('nomn', 'именительный'),
         ('gent', 'родительный'),
         ('datv', 'дательный'),
         ('accs', 'винительный'),
         ('ablt', 'творительный'),
         ('loct', 'предложный'))
numbers = (('sing', 'Единственное'), ('plur', 'Множественное'))
if 'NOUN' in word.tag:
    for i in numbers:
        print(f"{i[1]} число:")
        for j in cases:
            print(f"{j[1].capitalize()} падеж: {word.inflect({i[0], j[0]}).word}")
else:
    print('Не существительное')

    MAXUNUS = 3
UNUSW  =  ['ОДИН','ОДНА','ОДНО']
MAXSMALL = 8
SMALLW  = ['ДВА','ДВЕ','ОБА','ОБЕ','ПОЛТОРА','ПОЛТОРЫ','ТРИ','ЧЕТЫРЕ']
MAXBIG1 = 9
BIGW1 = ['ДВОЕ','ТРОЕ','ЧЕТВЕРО','ПЯТЕРО','ШЕСТЕРО','СЕМЕРО','ВОСЬМЕРО','ДЕВЯТЕРО','ДЕСЯТЕРО']
MAXBIG2 = 39
mBIGW2  = ['ПЯТЬ','ШЕСТЬ','СЕМЬ','ВОСЕМЬ','ДЕВЯТЬ','ДЕСЯТЬ','ОДИННАДЦАТЬ','ДВЕНАДЦАТЬ','ТРИНАДЦАТЬ','ЧЕТЫРНАДЦАТЬ','ПЯТНАДЦАТЬ','ШЕСТНАДЦАТЬ','СЕМНАДЦАТЬ','ВОСЕМНАДЦАТЬ','ДЕВЯТНАДЦАТЬ','ДВАДЦАТЬ','ТРИДЦАТЬ','ТРИДЕВЯТЬ','СОРОК','ПЯТЬДЕСЯТ','ШЕСТЬДЕСЯТ','СЕМЬДЕСЯТ','ВОСЕМЬДЕСЯТ','ДЕВЯНОСТО','ДВЕСТИ','СТО','ПОЛСТА','ПОЛТОРАСТА','ТРИСТА','ЧЕТЫРЕСТА','ПЯТЬСОТ','ШЕСТЬСОТ','СЕМЬСОТ','ВОСЕМЬСОТ','ДЕВЯТЬСОТ','СКОЛЬКО','НЕМАЛО','НЕСКОЛЬКО','МНОГО']

