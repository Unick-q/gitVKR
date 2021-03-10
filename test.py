# print(noun_res)
# cardinal_num, inpt_str = map(str, )
# b = list(map(str, cardinal_num, inpt_str))
# print(p.type_num(int(elem)))

# type_num(inpt_num) массив тысяч 
# morph.parse(numchunks.index('один') + 1)[0].tag.gender род тысячи 

# print(p.end_way(p.type_num(inpt_num),p.corr_num(cardinal_num),inpt_num))
# print(p.end_way(p.type_num(inpt_num),p.corr_num(ordinal_num),inpt_num))

# print(p.cor_card_num(p.end_wayp.cor_card_num(p.type_num(inpt_num),cardinal_num,inpt_num)))
# print(p.cor_ord_num(p.end_way(p.type_num(inpt_num),ordinal_num,inpt_num)))

# print(cardinal_num)
# print(ordinal_num)
# print(p.end_way(p.type_num(inpt_num),cardinal_num,inpt_num).index('один'))

# test_1 = morph.parse('две')[0].tag.number 
# test_2 = morph.parse('две')[0].tag.case 
# test_3 = morph.parse('две')[0].tag.gender 
# one = morph.parse('два')[0]
# print(test_1)
# print(test_2)
# print(test_3)
# test = one.inflect({'femn',test_1,test_2})
# print(test)
# one = morph.parse('двухсот')[0].inflect({"accs", "neut"})
# two = one.word
# print(one)
# print(two)
# print(morph.parse('два')[0].inflect({'femn','accs'}).word)
# result = re.sub(r'тысяча',morph.parse('тысяча')[0].make_agree_with_number(1234).word, cardinal_num)
# print(result)
# morph.parse('двухсот')[0]

# parsed_word = morph.parse('третий')[0].normal_form
# print(parsed_word)
# one_form = morph.parse(parsed_word)[0]
# print(one_form)
# norm_form = parsed_word.inflect({"nomn", "masc"}).word




import pymorphy2

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
        # print("Gender: " + parsed_word.tag.gender)
        # print("Given form (most likely): " + parsed_word.tag.case)
        print("Nominative:    " + parsed_word.inflect({"nomn"}).word)
        # print(" Plural: " + parsed_word.inflect({"nomn", "plur"}).word)
        print("Genitive:      " + parsed_word.inflect({"gent"}).word)
        # print(" Plural: " + parsed_word.inflect({"loct", "plur"}).word)
        print("Dative:        " + parsed_word.inflect({"datv"}).word)
        # print(" Plural: " + parsed_word.inflect({"accs", "plur"}).word)
        print("Accusative:    " + parsed_word.inflect({"accs"}).word)
        # print(" Plural: " + parsed_word.inflect({"gent", "plur"}).word)
        print("Instrumental:  " + parsed_word.inflect({"ablt"}).word)
        # print(" Plural: " + parsed_word.inflect({"ablt", "plur"}).word)
        print("Prepositional: " + parsed_word.inflect({"loct"}).word)
        # print(" Plural: " + parsed_word.inflect({"datv", "plur"}).word)
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
    # else:
    #     print("Gender: " + parsed_word.tag.gender)
    #     print("Given form (most likely): " + parsed_word.tag.case)
    #     print("Nominative:    " + parsed_word.inflect({"nomn", "masc"}).word + " / " + parsed_word.inflect({"nomn", "femn"}).word + " / " + parsed_word.inflect({"nomn", "neut"}).word)
    #     print(" Plural: " + parsed_word.inflect({"nomn", "plur"}).word)
    #     print("Prepositional: " + parsed_word.inflect({"loct", "masc"}).word + " / " + parsed_word.inflect({"loct", "femn"}).word + " / " + parsed_word.inflect({"loct", "neut"}).word)
    #     print(" Plural: " + parsed_word.inflect({"loct", "plur"}).word)
    #     print("Accusative:    " + parsed_word.inflect({"accs", "masc"}).word + " / " + parsed_word.inflect({"accs", "femn"}).word + " / " + parsed_word.inflect({"accs", "neut"}).word)
    #     print(" Plural: " + parsed_word.inflect({"accs", "plur"}).word)
    #     print("Genitive:      " + parsed_word.inflect({"gent", "masc"}).word + " / " + parsed_word.inflect({"gent", "femn"}).word + " / " + parsed_word.inflect({"gent", "neut"}).word)
    #     print(" Plural: " + parsed_word.inflect({"accs", "plur"}).word)
    #     print("Instrumental:  " + parsed_word.inflect({"ablt", "masc"}).word + " / " + parsed_word.inflect({"ablt", "femn"}).word + " / " + parsed_word.inflect({"ablt", "neut"}).word)
    #     print(" Plural: " + parsed_word.inflect({"ablt", "plur"}).word)
    #     print("Dative:        " + parsed_word.inflect({"datv", "masc"}).word + " / " + parsed_word.inflect({"datv", "femn"}).word + " / " + parsed_word.inflect({"datv", "neut"}).word)
    #     print(" Plural: " + parsed_word.inflect({"datv", "plur"}).word)
    word = input("Word: ")

