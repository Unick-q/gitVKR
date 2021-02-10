
import pymorphy2
<<<<<<< HEAD

morph = pymorphy2.MorphAnalyzer()
# Prompt user for input
print("Enter a russian word. If its a verb (any form), the conjugations will be given.\nIf noun/adjective (any form, not just nominative), declentions will be printed.")
print("Word (exit to leave): ")
word = input()
while(not word == "exit"):
    parsed_word = morph.parse(word)[0]
    # This case if for verbs, it can either be conjugated or infinitive
    if(parsed_word.tag.__contains__("VERB") or parsed_word.tag.__contains__("INFN")):
        # I'm so sorry that this print is going to look hideous.
        print("Я " + parsed_word.inflect({"1per"}).word)
        print("Ты " + parsed_word.inflect({"2per"}).word)
        print("Он/Она " + parsed_word.inflect({"3per"}).word)
        print("Вы " + parsed_word.inflect({"2per", "plur"}).word)
        print("Мы " + parsed_word.inflect({"1per", "plur"}).word)
        print("Они " + parsed_word.inflect({"3per", "plur"}).word)
        print("Past:")
        print("Он " + parsed_word.inflect({"past"}).word)
        print("Она " + parsed_word.inflect({"past", "femn"}).word)
        print("Они " + parsed_word.inflect({"past", "plur"}).word)
    elif(parsed_word.tag.__contains__("NOUN")):
        # We don't need to worry about gender of declentions with nouns.
        print("Gender: " + parsed_word.tag.gender)
        print("Given form (most likely): " + parsed_word.tag.case)
        print("Nominative:    " + parsed_word.inflect({"nomn"}).word)
        print(" Plural: " + parsed_word.inflect({"nomn", "plur"}).word)
        print("Prepositional: " + parsed_word.inflect({"loct"}).word)
        print(" Plural: " + parsed_word.inflect({"loct", "plur"}).word)
        print("Accusative:    " + parsed_word.inflect({"accs"}).word)
        print(" Plural: " + parsed_word.inflect({"accs", "plur"}).word)
        print("Genitive:      " + parsed_word.inflect({"gent"}).word)
        print(" Plural: " + parsed_word.inflect({"gent", "plur"}).word)
        print("Instrumental:  " + parsed_word.inflect({"ablt"}).word)
        print(" Plural: " + parsed_word.inflect({"ablt", "plur"}).word)
        print("Dative:        " + parsed_word.inflect({"datv"}).word)
        print(" Plural: " + parsed_word.inflect({"datv", "plur"}).word)
    elif(parsed_word.tag.__contains__("ADJF")):
        print("Gender: " + parsed_word.tag.gender)
        print("Given form (most likely): " + parsed_word.tag.case)
        print("Nominative:    " + parsed_word.inflect({"nomn", "masc"}).word + " / " + parsed_word.inflect({"nomn", "femn"}).word + " / " + parsed_word.inflect({"nomn", "neut"}).word)
        print(" Plural: " + parsed_word.inflect({"nomn", "plur"}).word)
        print("Prepositional: " + parsed_word.inflect({"loct", "masc"}).word + " / " + parsed_word.inflect({"loct", "femn"}).word + " / " + parsed_word.inflect({"loct", "neut"}).word)
        print(" Plural: " + parsed_word.inflect({"loct", "plur"}).word)
        print("Accusative:    " + parsed_word.inflect({"accs", "masc"}).word + " / " + parsed_word.inflect({"accs", "femn"}).word + " / " + parsed_word.inflect({"accs", "neut"}).word)
        print(" Plural: " + parsed_word.inflect({"accs", "plur"}).word)
        print("Genitive:      " + parsed_word.inflect({"gent", "masc"}).word + " / " + parsed_word.inflect({"gent", "femn"}).word + " / " + parsed_word.inflect({"gent", "neut"}).word)
        print(" Plural: " + parsed_word.inflect({"accs", "plur"}).word)
        print("Instrumental:  " + parsed_word.inflect({"ablt", "masc"}).word + " / " + parsed_word.inflect({"ablt", "femn"}).word + " / " + parsed_word.inflect({"ablt", "neut"}).word)
        print(" Plural: " + parsed_word.inflect({"ablt", "plur"}).word)
        print("Dative:        " + parsed_word.inflect({"datv", "masc"}).word + " / " + parsed_word.inflect({"datv", "femn"}).word + " / " + parsed_word.inflect({"datv", "neut"}).word)
        print(" Plural: " + parsed_word.inflect({"datv", "plur"}).word)
    word = input("Word: ")
=======
 
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
>>>>>>> 6f99ccb23e931538472bcc7344739d9230c4a2b1
