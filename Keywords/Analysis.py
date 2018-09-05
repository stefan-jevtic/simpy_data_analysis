import numpy as np
import pandas as pd
from Server.DB import DB


class KeywordsAnalysis:

    def __init__(self, shop_id):
        self.db = DB()
        self.shop_id = shop_id
        self.data = self.db.getData()
        self.frame = pd.DataFrame(self.data, columns=['id', 'keyword_id', 'position', 'domain_pzn_id', 't_val_from',
                                            't_val_to', 't_val_update', 't_val_del', 't_val_active', 'b_val_from',
                                            'b_val_to'])
        self.active = self.frame[self.frame.t_val_active == 1]
        self.inactive = self.frame[self.frame.t_val_active == 0]
        self.dates = self.inactive['t_val_from'].dt.date.unique()
        self.keywords = pd.DataFrame(self.db.getKeywords(), columns=['id', 'keyword', 'keyword_remove', 'negative_kws', 't_val_from',
                                            't_val_to', 't_val_update', 't_val_del', 't_val_active', 'b_val_from',
                                            'b_val_to'])

    def overallNumber(self):
        print("Differnce in number of inserted product: {0} and by percentage {1}%".format(
            (len(self.active)-len(self.inactive)), round(self.diffPerc(len(self.inactive), len(self.active)), 3)
        ))
        inactive_keywords = self.inactive['keyword_id'].unique()
        active_keywords = self.active['keyword_id'].unique()
        print('Number of keywords in inactive scrape: {0}'.format(len(inactive_keywords)))
        print('Number of keywords in active scrape: {0}'.format(len(active_keywords)))
        print("Differnce in number of inserted keywords: {0} and by percentage {1}%".format(
            (len(active_keywords) - len(inactive_keywords)), round(self.diffPerc(len(inactive_keywords), len(active_keywords)), 3)
        ))
        mask = np.in1d(inactive_keywords, active_keywords, invert=True)

        missing_kws = self.keywords[self.keywords.id.isin(inactive_keywords[mask])][['id', 'keyword']]
        if missing_kws.empty:
            print('There is no missing keywords this time! Bravo Obade!!!11')
        else:
            print('Keywords not included in last scrape: ')
            print(missing_kws)

    def analysisByShop(self):
        if len(self.shop_id) < 2:
            self.shop_id = '00' + str(self.shop_id)
        else:
            self.shop_id = '0' + str(self.shop_id)

        active_data_for_shop = self.active[self.active.domain_pzn_id.str.contains('{0}_'.format(self.shop_id))]
        inactive_data_for_shop = self.inactive[self.inactive.domain_pzn_id.str.contains('{0}_'.format(self.shop_id))]

        print("Differnce in number of inserted product: {0} and by percentage {1}%".format(
            (len(active_data_for_shop) - len(inactive_data_for_shop)), round(self.diffPerc(len(inactive_data_for_shop), len(active_data_for_shop)), 3)
        ))
        inactive_keywords = inactive_data_for_shop['keyword_id'].unique()
        active_keywords = active_data_for_shop['keyword_id'].unique()
        print('Number of keywords in inactive scrape: {0}'.format(len(inactive_keywords)))
        print('Number of keywords in active scrape: {0}'.format(len(active_keywords)))
        print("Differnce in number of inserted keywords: {0} and by percentage {1}%".format(
            (len(active_keywords) - len(inactive_keywords)),
            round(self.diffPerc(len(inactive_keywords), len(active_keywords)), 3)
        ))
        mask = np.in1d(inactive_keywords, active_keywords, invert=True)

        missing_kws = self.keywords[self.keywords.id.isin(inactive_keywords[mask])][['id', 'keyword']]
        if missing_kws.empty:
            print('There is no missing keywords this time! Bravo Obade!!!11')
        else:
            print('Keywords not included in last scrape: ')
            print(missing_kws)

    def diffPerc(self, old, new):
        return (new-old)/old*100

