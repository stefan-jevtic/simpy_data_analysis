import numpy as np
import pandas as pd
from Server.DB import DB


class Analysis:

    def __init__(self):
        self.db = DB()

    def testNp(self):
        data = self.db.test()
        frame = pd.DataFrame(data, columns=['id', 'shop_id', 'pzn', 'position', 'placement', 'screenshot', 't_val_from', 't_val_to', 't_val_update', 't_val_del', 't_val_active', 'b_val_from', 'b_val_to'])
        print(frame[(frame.t_val_active == 1) & (frame.placement == 'Markenshops')])
