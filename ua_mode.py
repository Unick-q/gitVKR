import sys
# import sum_prog
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import decimal
import re


class Example(QWidget):
    def __init__(self):
        super().__init__()

        # start button
        # self.go_button = QPushButton('&Start converting')

        # line for inserting
        # self.insert_number_line = QDoubleSpinBox()
        # self.insert_number_line.setRange(0, 2147483647)
        # self.insert_number_line.editingFinished.connect(self.convert)

        # for testing validator==================
        self.insert_number_line = QLineEdit()
        self.validator = QRegExpValidator(QRegExp(r'\d{1,7}\.\d{1,2}'), self)
        self.insert_number_line.setValidator(self.validator)

        self.insert_noun_line = QLineEdit()
        self.validator = QRegExpValidator(QRegExp(r'\d{1,7}\.\d{1,2}'), self)
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
            self.validator = QRegExpValidator(QRegExp(r'\d{1,7}\.\d{1,2}'), self)
            self.insert_number_line.setValidator(self.validator)
            self.insert_noun_line.setText("")
            self.exit_text.setText("")
            self.validator = QRegExpValidator(QRegExp(r'\d{1,7}\.\d{1,2}'), self)
            self.insert_noun_line.setValidator(self.validator)
        if self.language.currentText() == "Ru":
            self.insert_number_line.setText("")
            self.exit_text.setText("")
            self.validator = QRegExpValidator(QRegExp(r'\d{1,7}\,\d{1,2}'), self)
            self.insert_number_line.setValidator(self.validator)
            self.insert_noun_line.setText("")
            self.exit_text.setText("")
            self.validator = QRegExpValidator(QRegExp(r'\d{1,7}\.\d{1,2}'), self)
            self.insert_noun_line.setValidator(self.validator)
        if self.language.currentText() == "Ua":
            self.insert_number_line.setText("")
            self.exit_text.setText("")
            self.validator = QRegExpValidator(QRegExp(r'\d{1,7}\,\d{1,2}'), self)
            self.insert_number_line.setValidator(self.validator)
            self.insert_noun_line.setText("")
            self.exit_text.setText("")
            self.validator = QRegExpValidator(QRegExp(r'\d{1,7}\.\d{1,2}'), self)
            self.insert_noun_line.setValidator(self.validator)

    def initui(self):

        grid = QGridLayout()
        grid.setSpacing(10)
        # grid.addWidget(self.go_button, 2, 0)
        grid.addWidget(self.language_title, 1, 0, 0 ,4)
        grid.addWidget(self.language, 1, 1, 0 ,4)
        grid.addWidget(self.number_title, 2, 0, 0 ,4)
        grid.addWidget(self.insert_number_line, 2, 1, 0 ,4)
        grid.addWidget(self.what_number_1, 3, 1)
        grid.addWidget(self.what_number_2, 3, 2)
        grid.addWidget(self.what_number_3, 3, 3)
        grid.addWidget(self.noun_title, 4, 0, 0 ,4)
        grid.addWidget(self.insert_noun_line, 4, 1, 0 ,4)
        grid.addWidget(self.exit_text, 5, 1, 0 ,4)
        self.setLayout(grid)

        self.setGeometry(70, 70, 500, 300)
        self.setWindowTitle('Convert number to text')
        self.show()

        self.language.currentIndexChanged.connect(self.change_separator)
        self.insert_number_line.textEdited.connect(self.convert)

        # self.go_button.clicked.connect(self.convert)

    def convert(self):
        # self.exit_text.setText("")

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
            self.convert_ru(self.number)

        if self.language.currentText() == "En":
            self.convert_en(self.number)

    def convert_ua(self, number):
        """General Ua func"""
        self.exit_text.setText("")

        coin = number[1]
        if int(coin) > 9:
            coin = coin[1]
        coin = int(coin)

        if int(number[0]) == 1 and int(number[1]) == 0:
            self.exit_text.setText("одна гривня")
        elif (int(number[0]) == 2  or int(number[0]) == 3 or int(number[0]) == 4) and int(number[1]) == 0:
            self.exit_text.setText(
                self.int_to_ua(int(number[0])) + " гривні")
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

    def convert_ru(self,number):
        """General Ru func"""
        self.exit_text.setText("")



    def convert_en(self, number):
        """General En func"""

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

    units = (u'нуль', (u'одна', u'одна'), (u'два', u'дві'), u'три', u'чотири',
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
            data = ((self.units, 10), (self.tens, 100), (self.hundreds, 1000))
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
            return ' '.join((self.units[0], _orders[0][0][2])).strip()

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