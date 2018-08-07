import numpy as np
import pandas as pd
from Server.DB import DB


class Analysis:

    def __init__(self):
        self.db = DB()

    def overallNumber(self, shop_id):
        data = self.db.lastFive(shop_id)
        frame = pd.DataFrame(data, columns=['id', 'shop_id', 'pzn', 'position', 'placement', 'screenshot', 't_val_from',
                                            't_val_to', 't_val_update', 't_val_del', 't_val_active', 'b_val_from',
                                            'b_val_to'])
        active = frame[frame.t_val_active == 1]
        inactive = frame[frame.t_val_active == 0]
        dates = inactive['t_val_from'].dt.date.unique()
        sum_active = len(active)
        count_by_date = np.array([len(inactive[inactive.t_val_from.dt.date == date]) for date in dates])
        diff_by_average = self.diffPerc(np.average(count_by_date), sum_active)
        print('------------------------------------------')
        print('Difference by average %f' % diff_by_average)
        print('------------------------------------------')
        count_by_date = np.append(count_by_date, sum_active)
        diff = np.diff(count_by_date)/count_by_date[:-1]*100
        print(diff)
        print('------------------------------------------')
        each = []
        for date in dates:
            new = sum_active
            old = len(inactive[inactive.t_val_from.dt.date == date])
            each.append(self.diffPerc(old, new))

        diff_by_date = pd.DataFrame(each, index=dates, columns=['difference'])
        print(diff_by_date)

    def placementAnalysis(self, shop_id):
        data = self.db.lastFive(shop_id)
        frame = pd.DataFrame(data, columns=['id', 'shop_id', 'pzn', 'position', 'placement', 'screenshot', 't_val_from',
                                            't_val_to', 't_val_update', 't_val_del', 't_val_active', 'b_val_from',
                                            'b_val_to'])
        active = frame[frame.t_val_active == 1]
        active_date = active.t_val_from.dt.date.unique()
        inactive = frame[frame.t_val_active == 0]
        dates = inactive['t_val_from'].dt.date.unique()
        placements_active = active.placement.unique()
        matrix = []
        for date in dates:
            matrix.append([len(a) for a in [inactive[(inactive.placement == placement) & (inactive.t_val_from.dt.date == date)] for placement in inactive.placement.unique()]])
        matrix = np.array(matrix)
        placements_by_date = pd.DataFrame(matrix,
                                          columns=[placement for placement in inactive.placement.unique()],
                                          index=[date for date in dates])
        placements_active = pd.DataFrame([[len(a) for a in [active[active.placement == placement] for placement in active.placement.unique()]]],
                                         columns=[placement for placement in active.placement.unique()],
                                         index=[active.t_val_from.dt.date.unique()])
        num_placements_active = len(active.placement.unique())
        num_placements_by_date = np.array([len(inactive.placement.unique()) for date in dates])
        num_placements_by_date = np.append(num_placements_by_date, num_placements_active)
        for date in dates:
            print(self.diffPerc(placements_by_date[:date], placements_active[:active_date[0]].reindex(placements_by_date[:date].index)))
        diff = np.diff(num_placements_by_date)
        # print([active[active.placement == placement] for placement in active.placement.unique()][0])
        # kica = np.diff(matrix)/matrix[:-1]*100

        print(placements_by_date[:dates[0]])
        print(placements_active[:active_date[0]])
        print(self.diffPerc(placements_by_date[:dates[0]], placements_active[:active_date[0]]))

    def diffPerc(self, old, new):
        return round((new-old)/old*100, 3)

