import numpy as np
import pandas as pd
from pandas import ExcelWriter
from Server.DB import DB


class KeywordsAnalysis:

    def __init__(self):
        self.db = DB()
        self.active = pd.DataFrame(self.db.getKeywordsDataSmile(),  columns=['id', 'keyword_id', 'position', 'domain_pzn_id', 't_val_from',
                                                      't_val_to', 't_val_update', 't_val_del', 't_val_active',
                                                      'b_val_from', 'b_val_to'])
        self.inactive = pd.DataFrame(self.db.getKeywordsDataSmileTest(), columns=['id', 'keyword_id', 'position', 'domain_pzn_id', 't_val_from',
                                                      't_val_to', 't_val_update', 't_val_del', 't_val_active',
                                                      'b_val_from', 'b_val_to'])
        self.dates = self.inactive['t_val_from'].dt.date.unique()
        self.keywords = pd.DataFrame(self.db.getKeywords(), columns=['id', 'keyword', 'keyword_remove',
                                                                     'negative_kws', 't_val_from',
                                                                     't_val_to', 't_val_update', 't_val_del',
                                                                     't_val_active', 'b_val_from',
                                                                     'b_val_to'])
        self.id_shops = self.active.domain_pzn_id.str.slice(0, 5).unique()
        self.domains = pd.DataFrame(self.db.getDomains(), columns=['id', 'domain', 'name', 'keywords_link'])

    def overallNumber(self):

        if self.active.empty:
            print('Fresh data not available at the moment, please try later. Thank you!')
            return False
        print("Differnce in number of inserted product: {0} and by percentage {1}%".format(
            (len(self.active)-len(self.inactive[self.inactive.t_val_active == 1])), round(self.diffPerc(len(self.inactive[self.inactive.t_val_active == 1]), len(self.active)), 3)
        ))
        inactive_keywords = self.inactive['keyword_id'].unique()
        active_keywords = self.active['keyword_id'].unique()
        print('Number of keywords in inactive scrape: {0}'.format(len(inactive_keywords)))
        print('Number of keywords in active scrape: {0}'.format(len(active_keywords)))
        print("Differnce in number of inserted keywords: {0} and by percentage {1}%".format(
            (len(active_keywords) - len(inactive_keywords)), round(self.diffPerc(len(inactive_keywords), len(active_keywords)), 3)
        ))
        mask = np.in1d(inactive_keywords, active_keywords, invert=True)
        all_mask = np.in1d(self.keywords.id, active_keywords, invert=True)
        overall_missing = self.keywords[all_mask][['id', 'keyword']]
        if overall_missing.empty:
            print('There is no missing keywords this time for all active keywords! Bravo Obade!!!11\n\n')
        else:
            print('Keywords not included in last scrape for all active keywords: ')
            print(overall_missing)
        missing_kws = self.keywords[self.keywords.id.isin(inactive_keywords[mask])][['id', 'keyword']]
        if missing_kws.empty:
            print('There is no missing keywords this time! Bravo Obade!!!11\n\n')
        else:
            print('Keywords not included in last scrape for last 25 scrapes: ')
            print(missing_kws)

        matrix = []

        for shop in self.id_shops:
            active_data_for_shop = self.active[self.active.domain_pzn_id.str.contains('{0}_'.format(shop))]
            # inactive_data_for_shop = self.inactive[self.inactive.domain_pzn_id.str.contains('{0}_'.format(shop))]
            # inactive_keywords = inactive_data_for_shop['keyword_id'].unique()
            active_keywords = active_data_for_shop['keyword_id'].unique()
            mask = np.in1d(self.keywords.id, active_keywords, invert=True)
            num_missing = self.keywords[mask]
            matrix.append(np.array([int(shop), len(num_missing)]))
        missing_kws_for_all_shops = pd.DataFrame(matrix, columns=['shop_id', 'number_missing_kws'])
        print('Number of missing keywords by each shop.')
        print(missing_kws_for_all_shops)

    def analysisByShop(self, shop_id):
        if shop_id < 2:
            shop_id = '00' + str(shop_id)
        else:
            shop_id = '0' + str(shop_id)

        active_data_for_shop = self.active[self.active.domain_pzn_id.str.contains('{0}_'.format(shop_id))]
        inactive_data_for_shop = self.inactive[self.inactive.domain_pzn_id.str.contains('{0}_'.format(shop_id))]

        if active_data_for_shop.empty:
            print('No data available for that shop, try again.\n\n')
            return

        print("Differnce in number of inserted product: {0} and by percentage {1}%".format(
            (len(active_data_for_shop) - len(inactive_data_for_shop[inactive_data_for_shop.t_val_active == 1])),
            round(self.diffPerc(len(inactive_data_for_shop[inactive_data_for_shop.t_val_active == 1]), len(active_data_for_shop)), 3)
        ))
        inactive_keywords = inactive_data_for_shop['keyword_id'].unique()
        active_keywords = active_data_for_shop['keyword_id'].unique()
        print('Number of keywords in inactive scrape: {0}'.format(len(inactive_keywords)))
        print('Number of keywords in active scrape: {0}'.format(len(active_keywords)))
        print("Differnce in number of inserted keywords: {0} and by percentage {1}%".format(
            (len(active_keywords) - len(inactive_keywords)),
            round(self.diffPerc(len(inactive_keywords), len(active_keywords)), 3)
        ))
        mask = np.in1d(self.keywords.id, active_keywords, invert=True)

        missing_kws = self.keywords[mask][['id', 'keyword']]
        missing_kws = missing_kws.set_index(np.arange(len(missing_kws)))
        if missing_kws.empty:
            print('There is no missing keywords this time! Bravo Obade!!!11\n\n')
        else:
            print('Keywords not included in last scrape: ')
            print(missing_kws)
            print('\n')

        return missing_kws

    def exportExcel(self):
        writer = ExcelWriter('/home/kica/MissingKeywordsByShop.xlsx')
        starting_rows = 0
        for shop in self.id_shops:
            shop = int(shop)
            df = self.analysisByShop(shop)
            tmp = pd.DataFrame(np.full((len(df)), shop), columns=['shop_id'])
            pom = pd.DataFrame(np.full((len(df)), self.domains.name[self.domains.id == shop]), columns=['shop_name'])
            extended = pd.concat([df, tmp], axis=1)
            extended = pd.concat([extended, pom], axis=1)
            extended.to_excel(writer, startrow=starting_rows, index=False)
            starting_rows += len(df)+2
            writer.save()

    def diffPerc(self, old, new):
        return (new-old)/old*100

