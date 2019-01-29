'''
money_value: dictionary of all words meaning "pow".
moneyNormalize: function convert string with price of item from query
and return integer price.
'''


money_value = {
    "k" : 1000,
    "к" : 1000,
    "тыс" : 1000,
    "тысяча" : 1000,
    "м" : 1000000,
    "миллион" : 1000000
}



def moneyNormalize(string : str) -> int:
    '''
    string : string with nubers and words from dictionary
    returns price in integer format
    '''
    apokr = ""
    keys = money_value.keys()
    price = 0
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
    return price
