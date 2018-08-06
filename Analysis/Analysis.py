import numpy as np
import pandas as pd
from Server.DB import DB


class Analysis:

    def __init__(self):
        self.db = DB()

    def overallNumber(self):
        data = self.db.lastFive(2)
        frame = pd.DataFrame(data, columns=['id', 'shop_id', 'pzn', 'position', 'placement', 'screenshot', 't_val_from', 't_val_to', 't_val_update', 't_val_del', 't_val_active', 'b_val_from', 'b_val_to'])
        active = frame[frame.t_val_active == 1]
        inactive = frame[frame.t_val_active == 0]
        dates = inactive['t_val_from'].dt.date.unique()
        sum_active = len(active)
        count_by_date = np.array([len(inactive[inactive.t_val_from.dt.date == date]) for date in dates])
        diff_by_average = self.diffPerc(np.average(count_by_date), sum_active)
        print(diff_by_average)
        count_by_date = np.append(count_by_date, sum_active)
        diff = np.diff(count_by_date)/count_by_date[:-1]*100
        print(diff)
        each = []
        for date in dates:
            new = sum_active
            old = len(inactive[inactive.t_val_from.dt.date == date])
            each.append(self.diffPerc(old, new))

        diff_by_date = pd.DataFrame(each, index=dates, columns=['difference'])
        print(diff_by_date)

    def diffPerc(self, old, new):
        return round((new-old)/old*100, 3)

