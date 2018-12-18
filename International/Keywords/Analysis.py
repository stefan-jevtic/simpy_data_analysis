import numpy as np
import pandas as pd
from International.Server.DB import DB
from International.TableOrder import TableOrder


class KeywordsAnalysis(TableOrder):

    def __init__(self, country, shop, referer):
        super().__init__(country, shop)
        self.db = DB(country)
        self.main_frame = pd.DataFrame(
            self.db.getKwData(shop),
            columns=['id', 'keyword_c_id', 'position', 'product_link', 't_val_from', 't_val_to', 't_val_active']
        )
        self.keywords = pd.DataFrame(self.db.getKws(), columns=['id', 'keyword_c_id', 'keyword'])
        self.referer = referer

    def analyze(self):
        obj = {}
        self.main_frame.t_val_to = pd.to_datetime(self.main_frame.t_val_to, errors='coerce')
        active = self.main_frame[self.main_frame.t_val_active == 1]
        inactive = self.main_frame[self.main_frame.t_val_active == 0]
        matrix = []
        for date in self.main_frame['t_val_to'].dt.date.unique():
            products = len(self.main_frame[self.main_frame['t_val_to'].dt.date == date])
            matrix.append(np.array([products]))
        preview_frame = pd.DataFrame(matrix, columns=['kw_products'],
                                     index=[date for date in self.main_frame['t_val_to'].dt.date.unique()])
        obj['table'] = preview_frame.to_json(orient='records')
        mask_all = np.in1d(np.array(self.keywords.id), np.array(active.keyword_c_id.unique()), invert=True)
        missing_kws_all = self.keywords[mask_all][['id', 'keyword']]
        missing_kws_all = missing_kws_all.set_index(np.arange(len(missing_kws_all)))
        obj['diff_all'] = missing_kws_all.to_json(orient='records')
        mask_inactive = np.in1d(np.array(inactive.keyword_c_id.unique()), np.array(active.keyword_c_id.unique()), invert=True)
        missing_kws_inactive = self.keywords[self.keywords.id.isin(inactive.keyword_c_id.unique()[mask_inactive])][['id', 'keyword']]
        missing_kws_inactive = missing_kws_inactive.set_index(np.arange(len(missing_kws_inactive)))
        obj['diff_last'] = missing_kws_inactive.to_json(orient='records')
        if self.referer == 'cli':
            print(preview_frame)
            print(len(missing_kws_all))
            print(missing_kws_inactive)
            return 1
        elif self.referer == 'web':
            return obj
