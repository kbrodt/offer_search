import pandas as pd


data = pd.read_excel('./food/auchan/data.xls')
data = data.dropna(subset=['Цена'])


def to_num_auchan(text):
    return int(''.join(text.replace(',','').split()))

data['Цена'] = data['Цена'].apply(to_num_auchan)
data.to_excel('./food/auchan/data_cleaned.xls', index=False)
data = pd.read_excel('./food/auchan/data_cleaned.xls')


slots = set()
def process(text, ind=0):
    slots.update(text.strip().lower().split('~')[:3])
    return text

data['Название'].apply(process)
end_slots = set()
end_slots.update([slot.split(' ')[0] for slot in slots])
slots = end_slots
data = pd.read_excel('./food/foodband/data.xls')
data.to_excel('./food/foodband/data_cleaned.xls', index=False)
data = pd.read_excel('./food/foodband/data_cleaned.xls')

def process_food(text, ind=0):
    slots.update(text.strip().lower().split('~')[:2])
    return text

data['Название'].apply(process_food)


#iHerb
data = pd.read_excel('./food/iherb.com/data.xls')
data = data.dropna(subset=['Цена'])

def to_num_iherb(text):
    return int(float(''.join(text.replace('₽','').replace(',','').split())))

data['Цена'] = data['Цена'].apply(to_num_iherb)

data.to_excel('./food/iherb.com/data_cleaned.xls', index=False)
data = pd.read_excel('./food/iherb.com/data_cleaned.xls')
data.head()


def process_iherb(text, ind=0):
    slots.update(text.strip().lower().split('~')[1:4])
    return text

data['Название'].apply(process_iherb)
slots

slots = [s.strip() for s in slots if len(s.strip()) < 24]
slots = set(slots)
slots

#abrikos
data = pd.read_excel('./food/abrikos/data.xls')
data.head()


def to_num_abrikos(text):
    return int(text)

data['Цена'] = data['Цена'].apply(to_num_abrikos)

data.to_excel('./food/abrikos/data_cleaned.xls', index=False)
data = pd.read_excel('./food/abrikos/data_cleaned.xls')
data.head()

def process_abrikos(text, ind=0):
    slots.update([s.split(' ')[0] for s in text.strip().lower().split('~')[0:3]])
    return text

data['Название'].apply(process_abrikos)


end_slots = set()
end_slots = [slot.replace('"','').replace(',','') for slot in slots]
end_slots = sorted([slot.strip() for slot in end_slots if len(slot.strip()) >0])

save_slots = pd.Series(end_slots)
save_slots.to_csv('./food/slots.csv', index=False, header=False)