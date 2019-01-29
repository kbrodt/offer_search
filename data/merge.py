import pandas as pd
import numpy as np


def unique(data: pd.DataFrame , cols):
    new_data = []
    for gr in data.groupby('NAME'):    
        gr = gr[1]
        gr = gr.drop_duplicates(subset=cols)

        if len(gr) > 1:
            if len(gr['OFFER_TYPE'].unique()) == 1:
                gr = gr[gr['CASH_BACK_HEIGHT'] == gr['CASH_BACK_HEIGHT'].max()]
            else:
                gr1 = gr[gr['CASH_BACK_HEIGHT'] == gr['CASH_BACK_HEIGHT'].max()]
                gr2 = gr[gr['OFFER_TYPE'] == 'SPECIAL_CREDIT']
                gr = pd.concat([gr1, gr2])

        assert len(gr) <= 2

        new_data.append(gr)

    return pd.concat(new_data).sort_index()


def merge(cat):
    offer_with_cats = []
    for _, row in data.iterrows():
        cats = web[web['NAME'] == row['NAME']]
        cats = cats[cats['CATEGORY_NAME'] == cat]
        if len(cats) == 0:
            continue

        assert len(cats) == 1 or (len(cats) == 2 and len(cats['OFFER_TYPE'].unique()) == 2), cats
        offer_with_cats.append(row)
        
    return pd.DataFrame(offer_with_cats)


data = pd.read_excel('./current_offers.xlsx')
data = data[~data['WEB'].isna()]
data = data[~((data['CASH_BACK_HEIGHT'] == 0) & (data['OFFER_TYPE'] != 'SPECIAL_CREDIT'))]
data = unique(data, cols=['CASH_BACK_HEIGHT'])


web = pd.read_excel('./offers_with_categories.xlsx')
web = web[(web['CATEGORY_NAME'] == 'Спорт') | (web['CATEGORY_NAME'] == 'Еда и продукты')]
web = web[~web['CATEGORY_NAME'].isna()]
web = web[~((web['CASH_BACK_HEIGHT'] == 0) & (web['OFFER_TYPE'] != 'SPECIAL_CREDIT'))]
web = unique(web, cols=['CASH_BACK_HEIGHT', 'CATEGORY_NAME'])


sport = merge('Спорт')
sport.to_excel('sport.xls', index=False)

eda = merge('Еда и продукты')
eda.to_excel('food.xls', index=False)


names = np.intersect1d(sport['NAME'], eda['NAME'])
d = []
for name in names:
    d.append(sport[sport['NAME'] == name])
pd.concat(d).to_excel('intersect.xls', index=False)
