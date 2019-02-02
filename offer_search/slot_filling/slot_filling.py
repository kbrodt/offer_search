from .normalizing_slot_filler import NormalizingSlotFiller
from .dictionaries import Goods
from .yargy_rules import *
from overrides import overrides
import typing as t
import pymorphy2 as pmh

money_value = {
    "k" : 1000,
    "к" : 1000,
    "тыс" : 1000,
    "тысяча" : 1000,
    "косарь" : 1000,#ХД
    "м" : 1000000,
    "миллион" : 1000000
}

class SlotFillerWithRules(NormalizingSlotFiller):
    def __init__(self):
        self.analyzer = pmh.MorphAnalyzer()
        self.price_rules = [PRICE_FROM, PRICE_TO]
        self.tokenizer = MorphTokenizer()
        self.dict = dict()
    def leveinstein_distance(self, str1, str2):
        "Calculates the Levenshtein distance between a and b."
        n, m = len(str1), len(str2)
        if n > m:
            str1, str2 = str2, str1
            n, m = m, n

        current_row = range(n+1) # Keep current and previous row, not entire matrix
        for i in range(1, m+1):
            previous_row, current_row = current_row, [i]+[0]*n
            for j in range(1,n+1):
                add, delete, change = previous_row[j]+1, current_row[j-1]+1, previous_row[j-1]
                if str1[j-1] != str2[i-1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]
    def preprocess(self, string):
        string = string.lower()
        string = ' '.join(self.analyzer.parse(token.value)[0].normal_form for token in self.tokenizer(string))
        string = " " + string + " "
        return string
    def parsing(self, string):
        parsed = dict()
        parsed['Offer_type'] = 0
        #FIND INSTALLMENT
        erased_string = ""
        parser = Parser(IS_INSTALLMENT)
        for match in parser.findall(string):
            parsed['Offer_type'] = 1
            for token in match.tokens:
                erased_string = ' ' + erased_string.replace(" " + token.value + " ", " ") + ' '
        string = erased_string
        #FIND CASHBACK as %
        parsed['Cashback'] = "NaN"
        parser = Parser(PERCENT_RULE)
        percent_tokens = parser.findall(string)
        for match in percent_tokens:
            cashback = ' '.join([_.value for _ in match.tokens])
            #выбираем только числа без слов и знака %
            parser = Parser(NUMBER_RULE)
            for number_match in parser.findall(cashback):
                parsed['Cashback'] = ' '.join([_.value for _ in number_match.tokens])
            for token in match.tokens:
                string = string.replace(" " + token.value + " ", " ")    
        #find cashback with word 'cashback'
        cashback_rules = [CASHBACK_AFTER, CASHBACK_BEFORE]
        erased_string = string
        for rule in cashback_rules:
            if not (parsed['Cashback'] == "NaN" or parsed["Cashback"] == ""):
                break
            erased_string = string
            parser = Parser(rule)
            cashback_tokens = parser.findall(erased_string)
            cashback = ""
            #пока тренируемся на том, чnо кэшбек только на один товар
            for match in cashback_tokens:
                cashback += ' '.join([_.value for _ in match.tokens])
                if(cashback == ""):
                    continue
                for token in match.tokens:
                    erased_string = ' ' + erased_string.replace(" " + token.value + " ", " ") + ' '
            #вытаскиваем значения с размерностями:
            parser = Parser(CASHBACK_VALUE)
            cashback_tokens = parser.findall(cashback)
            cashback = ""
            for match in cashback_tokens:
                cashback += ' '.join([_.value for _ in match.tokens])
            #проверяем просто на вхождение процентов (т.к. пока мы рассрочку не учитываем)
            if(cashback == ""):
                parser = Parser(NUMBER_RULE)
                cashback_tokens = parser.findall(cashback)
                for match in cashback_tokens:
                    cashback += ' '.join([_.value for _ in match.tokens])
            else:
                parsed['Cashback'] = cashback.replace(" ", "")
                break
        string = erased_string.replace('[', '').replace(']', '')
        
        #find
        parsed['Price_from'] = parsed['Price_to'] = 'NaN'
        price_keys = ['Price_from', 'Price_to']
        is_value = 0
        for i in range(2):
            parser = Parser(self.price_rules[i])
            price_tokens = parser.findall(string)
            for match in price_tokens:
                is_value += 1
                price_string = ' '.join([_.value for _ in match.tokens])
                parser = Parser(MONEY_RULE)
                money = ""
                for price_match in parser.findall(price_string):
                    money = ' '.join([_.value for _ in price_match.tokens])
                parsed[price_keys[i]] = money#' '.join([_.value for _ in match.tokens]).replace("до ", "").replace("до ", "")
                for token in match.tokens:
                    string = string.replace(" " + token.value + " ", " ")
        if (is_value == 0):
            parser = Parser(PRICE_VALUE)
            price_tokens = parser.findall(string)
            price = ""
            for match in price_tokens:
                price = ' '.join([_.value for _ in match.tokens])
                parsed['Price_from'] = parsed['Price_to'] = price
                for token in match.tokens:
                    string = string.replace(token.value + " ", "")
        #find ATTRIBUTE
        parser = Parser(ATTRIBUTE)
        attr = ""
        for match in parser.findall(string):
            attr += ' '.join([_.value for _ in match.tokens]) + ' '
        parsed['Attributes'] = attr[:-1]
        
        words = string.split(' ')
        parsed['Item'] = ""
        for word in words:
            #find Item
            #if(self.analyzer.parse(word)[0].normal_form in self.dict['goods']):
            #    parsed['Item'] += word + ' '
            #    #while True:
            #    #    pass
            
            #normalized_word = self.analyzer.parse(word)[0].normal_form
            normalized_word = word
            saved_word = ""
            minimum = len(normalized_word)
            for dictionary_word in self.dict['goods']:
                dis = self.leveinstein_distance(normalized_word, dictionary_word)
                if(dis < minimum and dis < min(len(dictionary_word), len(normalized_word)) / 2):
                    is_noun = False
                    for tags in self.analyzer.parse(dictionary_word):
                        if(tags.tag.POS == 'NOUN' and tags.score >= 0.125):
                            is_noun = True
                            break
                    if(is_noun):
                        minimum = dis
                        saved_word = dictionary_word
        
            parsed['Item'] += saved_word + ' '
        words_a = parsed['Attributes'].split(' ')
        words_i = parsed['Item'].split(' ')
        for word in words_a:
            if(word in words_i):
                parsed['Attributes'] = parsed['Attributes'].replace(word, '')
        #parsed['Item'] = parsed['Item'][:-1]
        if(len(parsed['Item']) == 0):
            return parsed
        while parsed['Item'][0] == ' ':
            parsed['Item'] = parsed['Item'][1:]
            if(len(parsed['Item']) == 0):
                return parsed
        while parsed['Item'][-1] == ' ':
            parsed['Item'] = parsed['Item'][:-1]
            if(len(parsed['Item']) == 0):
                return parsed
         
        return parsed
    @overrides
    def fill(self, text: str, intent: str) -> t.Dict[str, t.Any]:
        self.dict['goods'] = Goods(intent)
        processed_string = self.preprocess(text)
        return self.normalize(self.parsing(processed_string))
    @overrides
    def normalize(self, form: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        keys = money_value.keys()
        price_keys = ['Price_from', 'Price_to']
        for key in price_keys:
            apokr = ""
            price = 0
            string = form[key]
            for sym in string:
                if(sym == " "):
                    continue
                if(ord(sym) >= 48 and ord(sym) <= 57):
                    price *= 10
                    price += int(sym)
                else:
                    apokr += sym
                    #основываемся на том, что все слова - значения порядка
                    if(apokr in keys):
                        price *= money_value[apokr]
                        apokr = ""
            form[key] = price
        if(form['Price_to'] == 0):
            form['Price_to'] = 999999999
        if(form['Cashback'] == '' or form['Cashback'] == 'NaN'):
            form['Cashback'] = 0
        else:
            form['Cashback'] = int(form['Cashback'])
        return form


