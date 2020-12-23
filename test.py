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

print("Input what lang you want to write")
print(" 0 -- Russian ")
print(" 1 -- Ukranian ")
write_lang = bool(input())
if (write_lang != 1) & (write_lang != 0):
    print ('Error: Invalid argument!') 
    sys.exit()
print("Input what lang you want to read")
print(" 0 -- Russian ")
print(" 1 -- Ukranian ")
read_lang = bool(input())
if (read_lang != 1) & (read_lang != 0):
    print ('Error: Invalid argument!') 
    sys.exit()