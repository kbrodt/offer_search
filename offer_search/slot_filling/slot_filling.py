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
        self.dict = dict()
        self.price_rules = [PRICE_FROM, PRICE_TO]
        self.tokenizer = MorphTokenizer()
    def preprocess(self, string):
        string = string.lower()
        string = ' '.join(self.analyzer.parse(token.value)[0].normal_form for token in self.tokenizer(string))
        string = " [" + string + "] "
        return string
    def parsing(self, string):
        words = string.split(" ")
        parsed = dict()
       
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
        
        #find  price
        parsed['Price'] = {"From" : "NaN", "To": "NaN"}
        is_value = 0
        price_keys_list = list(parsed['Price'].keys())
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
                parsed['Price'][price_keys_list[i]] = money#' '.join([_.value for _ in match.tokens]).replace("до ", "").replace("до ", "")
                for token in match.tokens:
                    string = string.replace(" " + token.value + " ", " ")
        if (is_value == 0):
            parser = Parser(PRICE_VALUE)
            price_tokens = parser.findall(string)
            price = ""
            for match in price_tokens:
                price = ' '.join([_.value for _ in match.tokens])
                parsed['Price']["From"] = parsed['Price']["To"] = price
                for token in match.tokens:
                    string = string.replace(token.value + " ", "")
        
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
                    erased_string = erased_string.replace(" " + token.value + " ", " ")
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
        string = erased_string
        #find ATTRIBUTE
        parser = Parser(ATTRIBUTE)
        attr_tokens = parser.findall(string)
        attr = ""
        parsed['Attributes'] = string
        #for match in attr_tokens:
        #        attr = ' '.join([_.value for _ in match.tokens])
        #        parsed['Attributes'] = attr
        parsed['Item'] = "NaN"
        for word in words:
            #find Item
            if(self.analyzer.parse(word)[0].normal_form in self.dict['goods']):
                parsed['Item'] = word
                #while True:
                #    pass
        
        return parsed
    @overrides
    def fill(self, text: str, intent: str) -> t.Dict[str, t.Any]:
        self.dict['goods'] = Goods(int(intent))
        processed_string = self.preprocess(text)
        return self.normalize(self.parsing(processed_string))
    @overrides
    def normalize(self, form: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        apokr = ""
        keys = money_value.keys()
        price = 0
        price_keys = form['Price'].keys()
        for key in price_keys:
            string = form['Price'][key]
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
            form['Price'][key] = price
        return form