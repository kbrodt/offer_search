import pandas as pd


data = pd.read_excel('./sport/double-sports/data.xls')
data.to_excel('./sport/double-sports/data_cleaned.xls', index=False)
data = pd.read_excel('./sport/double-sports/data_cleaned.xls')

slots = set()
def process(text, ind=0):
    x = text
    
    x = x.strip().lower().split('~')[0]
    x = x.split('/')[:3]
    x = [x_.strip() for x_ in x if len(x_.strip()) > 0]
    slots.update(x)
    
    return text

data['Название'].apply(process)

data = pd.read_excel('./sport/gold-standart.com/data.xls')

def to_num(text):
    return int(''.join(text.replace('руб', '').split()))


data['Цена'] = data['Цена'].apply(to_num)

data.to_excel('./sport/gold-standart.com/data_cleaned.xls', index=False)
data = pd.read_excel('./sport/gold-standart.com/data_cleaned.xls')


def process_gold(text, ind=0):
    slots.update(text.strip().lower().split('~')[:1])
    
    return text

data['Название'].apply(process_gold)

data = pd.read_excel('./sport/pro-bike/data.xls')
data = data.dropna(subset=['Цена'])

def to_num_gold(text):
    return int(''.join(text.replace('pуб.', '').split()))

data['Цена'] = data['Цена'].apply(to_num_gold)

data.to_excel('./sport/pro-bike/data_cleaned.xls', index=False)
data = pd.read_excel('./sport/pro-bike/data_cleaned.xls')

def process_bike(text, ind=0):
    slots.update(text.strip().lower().split('~')[:2])
    return text

data['Название'].apply(process_bike)

data = pd.read_excel('./sport/tramontana.ru/data.xls')
data = data.dropna(subset=['Цена'])

def to_num_tramontana(text):
    return int(''.join(str(text).replace('₽', '').split()))

data['Цена'] = data['Цена'].apply(to_num_tramontana)

data.to_excel('./sport/tramontana.ru/data_cleaned.xls', index=False)
data = pd.read_excel('./sport/tramontana.ru/data_cleaned.xls')

def process_tramontana(text, ind=0):
    slots.update(str(text).strip().lower().split('~')[:2])
    return text


data['Название'].apply(process_tramontana)

#iHerb
data = pd.read_excel('./sport/iherb.com/data.xls')
data = data.dropna(subset=['Цена'])

def to_num_iherb(text):
    return int(float(''.join(text.replace('₽','').replace(',','').split())))

data['Цена'] = data['Цена'].apply(to_num_iherb)
data.to_excel('./sport/iherb.com/data_cleaned.xls', index=False)
data = pd.read_excel('./sport/iherb.com/data_cleaned.xls')

def process_iherb(text, ind=0):
    slots.update(text.strip().lower().split('~')[1:4])
    return text

data['Название'].apply(process_iherb)

slots = [s.strip() for s in slots if len(s.strip()) < 24]
slots = set(slots)

end_slots = set()
for slot in slots:
    end_slots.update(slot.replace('"','').split(', '))

end_slots = [slot.strip()  for slot in end_slots if len(slot.strip()) > 0]
end_slots.append('велосипед')
end_slots = sorted(end_slots)
save_slots = pd.Series(end_slots)
save_slots.to_csv('./sport/slots.csv', index=False, header=False)