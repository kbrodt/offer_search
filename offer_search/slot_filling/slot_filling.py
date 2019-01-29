from base import SlotFiller
from dictionaries import Goods
from yargy_rules import *
from overrides import overrides
import typing as t
import pymorphy2 as pmh

goods = []

class SlotFillerWithRules(SlotFiller):
    def __init__(self):
        self.analyzer = pmh.MorphAnalyzer()
        self.dict = dict()
        self.price_rules = [PRICE_FROM, PRICE_TO]
    def preprocess(self, string):
        string = string.lower()
        string = " " + string + " "
        return string
    def parsing(self, string):
        words = string.split(" ")
        parsed = dict()
       
        #FIND CASHBACK
        parsed['Cashback'] = "NaN"
        cashback_rules = [CASHBACK_AFTER, CASHBACK_BEFORE]
        erased_string = string
        for rule in cashback_rules:
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
        #find  price
        parsed['Price'] = {"From" : "NaN", "To": "NaN"}
        is_value = 0
        price_keys_list = list(parsed['Price'].keys())
        for i in range(2):
            parser = Parser(self.price_rules[i])
            price_tokens = parser.findall(string)
            for match in price_tokens:
                is_value += 1
                parsed['Price'][price_keys_list[i]] = ' '.join([_.value for _ in match.tokens])
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
        
        parser = Parser(ATTRIBUTE)
        attr_tokens = parser.findall(string)
        attr = ""
        parsed['Attributes'] = "NaN"
        for match in attr_tokens:
                attr = ' '.join([_.value for _ in match.tokens])
                parsed['Attributes'] = attr
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
        return self.parsing(processed_string)