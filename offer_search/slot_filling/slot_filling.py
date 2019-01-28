from base import SlotFiller
from dictionaries import Goods
from yargy_rules import *
from overrides import overrides
import typing as t

goods = []

class SlotFillerWithRules(SlotFiller):
    def __init__(self):
        self.dict = dict()
        self.price_rules = [PRICE_FROM, PRICE_TO]
    def Preprocess(self, string):
        string = string.lower()
        string = " " + string + " "
        return string
    def Parsing(self, string):
        words = string.split(" ")
        parsed = dict()
       
        #FIND CASHBACK
        parser = Parser(CASHBACK)
        cashback_tokens = parser.findall(string)
        cashback = ""
        #пока тренируемся на том, чnо кэшбек только на один товар
        for match in cashback_tokens:
            cashback += ' '.join([_.value for _ in match.tokens])
            for token in match.tokens:
                string = string.replace(" " + token.value + " ", " ")
        #вытаскиваем значения с размерностями:
        parser = Parser(CASHBACK_VALUE)
        cashback_tokens = parser.findall(cashback)
        cashback = ""
        for match in cashback_tokens:
            cashback += ' '.join([_.value for _ in match.tokens])
        #проверяем просто на вхождение процентов (т.к. пока мы рассрочку не учитываем)
        if(cashback == ""):
            parser = Parser(PERCENT_RULE)
            cashback_tokens = parser.findall(cashback)
            for match in cashback_tokens:
                cashback += ' '.join([_.value for _ in match.tokens])
        parsed['Cashback'] = cashback.replace(" ", "")
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
                    string = string.replace(token.value, "")
        
        parser = Parser(ATTRIBUTE)
        attr_tokens = parser.findall(string)
        attr = ""
        parsed['Attributes'] = "NaN"
        for match in attr_tokens:
                attr = ' '.join([_.value for _ in match.tokens])
                parsed['Attributes'] = attr
        for word in words:
            #find Item
            if(word in self.dict['goods']):
                parsed['Item'] = word
                #while True:
                #    pass
        
        return parsed
    @overrides
    def fill(self, text: str, intent: str) -> t.Dict[str, t.Any]:
        self.dict['goods'] = Goods(int(intent))
        processed_string = self.Preprocess(text)
        return self.Parsing(processed_string)  