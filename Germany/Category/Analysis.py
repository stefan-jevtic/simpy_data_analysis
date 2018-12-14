import numpy as np
import pandas as pd
from pandas import ExcelWriter
from Germany.Server.DB import DB
pd.set_option('max_colwidth', 400)


class CategoryAnalysis:

    def __init__(self):
        self.db = DB()
        self.inactive = pd.DataFrame(self.db.getCategoryDataSmileTest(),  columns=['id', 'price_id', 'position', 'category_link', 'category', 'depth', 'domain_pzn_id', 'brand_theme_shops', 'screen_category', 't_val_from',
                                                      't_val_to', 't_val_update', 't_val_del', 't_val_active',
                                                      'b_val_from', 'b_val_to'])
        self.active = pd.DataFrame(self.db.getCategoryDataSmile(), columns=['id', 'price_id', 'position', 'category_link', 'category', 'domain_pzn_id', 'product_url', 't_val_from',
                                                      't_val_to', 't_val_update', 't_val_del', 't_val_active',
                                                      'b_val_from', 'b_val_to', 'screenshot'])
        self.dates = self.inactive['t_val_from'].dt.date.unique()
        self.id_shops = self.active.domain_pzn_id.str.slice(0, 5).unique()
        self.domains = pd.DataFrame(self.db.getDomains(), columns=['id', 'domain', 'name', 'keywords_link'])

    def overallNumber(self):
        
        if self.active.empty:
            print('Fresh data not available at the moment, please try later. Thank you!')
            return False
        print("Differnce in number of inserted product: {0} and by percentage {1}%".format(
            (len(self.active)-len(self.inactive[self.inactive.t_val_active == 1])), round(self.diffPerc(len(self.inactive[self.inactive.t_val_active == 1]), len(self.active)), 3)
        ))
        inactive_categories = self.inactive['category_link'].unique()
        active_categories = self.active['category_link'].unique()
        print('Number of categories in inactive scrape: {0}'.format(len(inactive_categories)))
        print('Number of categories in active scrape: {0}'.format(len(active_categories)))
        print("Differnce in number of inserted categories: {0} and by percentage {1}%".format(
            (len(active_categories) - len(inactive_categories)), round(self.diffPerc(len(inactive_categories), len(active_categories)), 3)
        ))

        all_mask = np.in1d(inactive_categories, active_categories, invert=True)
        overall_missing = pd.DataFrame(self.inactive[self.inactive.category_link.isin(inactive_categories[all_mask])].category_link.unique(), columns=['category_link'])
        if overall_missing.empty:
            print('There is no missing categories this time compared with last five scrapes! Bravo Obade!!!11\n\n')
        else:
            print('Categories not included in last scrape compared with last five scrapes: ')
            print(overall_missing)

        matrix = []

        for shop in self.id_shops:
            active_data_for_shop = self.active[self.active.domain_pzn_id.str.contains('{0}_'.format(shop))]
            inactive_data_for_shop = self.inactive[self.inactive.domain_pzn_id.str.contains('{0}_'.format(shop))]
            inactive_categories = inactive_data_for_shop['category_link'].unique()
            active_categories = active_data_for_shop['category_link'].unique()
            mask = np.in1d(inactive_categories, active_categories, invert=True)
            num_missing = pd.DataFrame(inactive_data_for_shop[inactive_data_for_shop.category_link.isin(inactive_categories[mask])].category_link.unique(), columns=['category_link'])
            matrix.append(np.array([int(shop), len(num_missing)]))
        missing_cat_for_all_shops = pd.DataFrame(matrix, columns=['shop_id', 'number_missing_cat'])
        print('Number of missing categories by each shop.')
        print(missing_cat_for_all_shops)

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
        inactive_categories = inactive_data_for_shop['category_link'].unique()
        active_categories = active_data_for_shop['category_link'].unique()
        print('Number of categories in inactive scrape: {0}'.format(len(inactive_categories)))
        print('Number of categories in active scrape: {0}'.format(len(active_categories)))
        print("Differnce in number of inserted categories: {0} and by percentage {1}%".format(
            (len(active_categories) - len(inactive_categories)),
            round(self.diffPerc(len(inactive_categories), len(active_categories)), 3)
        ))
        mask = np.in1d(inactive_categories, active_categories, invert=True)

        missing_cat = pd.DataFrame(self.inactive[self.inactive.category_link.isin(inactive_categories[mask])].category_link.unique(), columns=['category_link'])
        if missing_cat.empty:
            print('There is no missing categories this time! Bravo Obade!!!11\n\n')
        else:
            print('categories not included in last scrape: ')
            print(missing_cat)
            print('\n')

        return missing_cat

    def exportExcel(self):
        writer = ExcelWriter('/home/kica/MissingCategoriesByShop.xlsx')
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

