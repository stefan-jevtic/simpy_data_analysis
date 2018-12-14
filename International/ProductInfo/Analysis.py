import numpy as np
import pandas as pd
from International.Server.DB import DB
from International.ProductInfo.TableOrder import TableOrder
import datetime

class ProductAnalysis(TableOrder):

    def __init__(self, country, shop):
        super().__init__(country, shop)
        self.db = DB(country)
        self.main_frame = pd.DataFrame(
            self.db.getData(shop, self.order),
            columns=['img_url', 'vid_url', 'price', 'title', 'availability', 'product_link', 't_val_from', 't_val_to', 't_val_active', 'desc_plaintext']
        )

    def analyze(self):
        self.main_frame.t_val_to = pd.to_datetime(self.main_frame.t_val_to, errors='coerce')
        print(len(self.main_frame))
        matrix = []
        for date in self.main_frame['t_val_to'].dt.date.unique():
            price = len(self.main_frame[self.main_frame['t_val_to'].dt.date == date].product_link.unique())
            media = len(self.main_frame[self.main_frame['t_val_to'].dt.date == date].img_url.unique())
            desc = len(self.main_frame[self.main_frame['t_val_to'].dt.date == date].desc_plaintext.unique())
            matrix.append([price, media, desc])
        preview_frame = pd.DataFrame(matrix, columns=['price', 'media', 'description'],
                                     index=[date for date in self.main_frame['t_val_to'].dt.date.unique()])
        print(preview_frame)
