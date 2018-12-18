import numpy as np
import pandas as pd
from International.Server.DB import DB
from International.TableOrder import TableOrder


class ProductAnalysis(TableOrder):

    def __init__(self, country, shop, referer):
        super().__init__(country, shop)
        self.db = DB(country)
        self.main_frame = pd.DataFrame(
            self.db.getData(shop),
            columns=['img_url', 'vid_url', 'price', 'title', 'availability', 'product_link', 't_val_from', 't_val_to', 't_val_active', 'desc_plaintext']
        )
        self.links = pd.DataFrame(self.db.getLinks(shop), columns=['link'])
        self.referer = referer

    def analyze(self):
        obj = {}
        self.main_frame.t_val_to = pd.to_datetime(self.main_frame.t_val_to, errors='coerce')
        inactive = self.main_frame[self.main_frame.t_val_active == 0]
        active = self.main_frame[self.main_frame.t_val_active == 1]
        matrix = []
        for date in self.main_frame['t_val_to'].dt.date.unique():
            price = len(self.main_frame[self.main_frame['t_val_to'].dt.date == date].product_link.unique())
            media = len(self.main_frame[self.main_frame['t_val_to'].dt.date == date].img_url.unique())
            desc = len(self.main_frame[self.main_frame['t_val_to'].dt.date == date].desc_plaintext.unique())
            matrix.append(np.array([price, media, desc]))
        preview_frame = pd.DataFrame(matrix, columns=['price', 'media', 'description'],
                                     index=[date for date in self.main_frame['t_val_to'].dt.date.unique()])
        obj['table'] = preview_frame.to_json(orient='records')
        mask_all_for_active = np.in1d(np.array(self.links.link), np.array(active.product_link.unique()), invert=True)
        not_scraped = self.links[mask_all_for_active]
        obj['diff_all'] = not_scraped.to_json(orient='records')
        mask_inactive_for_active = np.in1d(np.array(inactive.product_link.unique()), np.array(active.product_link.unique()), invert=True)
        not_scraped_last = inactive.product_link.unique()[mask_inactive_for_active]
        obj['diff_last'] = pd.Series(not_scraped_last).to_json(orient='values')
        if self.referer == 'cli':
            print(preview_frame)
            print(len(not_scraped_last))
            print(len(not_scraped))
            return 1
        elif self.referer == 'web':
            return obj
