import n2t
import pymorphy2
 
def get_number_and_noun(numeral, noun):
    morph = pymorphy2.MorphAnalyzer()
    word = morph.parse(noun)[0]
    v1, v2, v3 = word.inflect({'sing', 'nomn'}), word.inflect({'gent'}), word.inflect({'plur', 'gent'})
    return num2text(num=numeral, main_units=((v1.word, v2.word, v3.word), 'm'))
 
result = get_number_and_noun(52, 'рубль')  
print(male_units)
print(female_units)
print(result)