import numpy as np
import pandas as pd
from numpy import inf
from Server.DB import DB


class GfkAnalysis:

    def __init__(self, shop_id):
        self.db = DB()
        self.data = self.db.lastFive(shop_id)
        self.frame = pd.DataFrame(self.data, columns=['id', 'shop_id', 'pzn', 'position', 'placement', 'screenshot', 't_val_from',
                                            't_val_to', 't_val_update', 't_val_del', 't_val_active', 'b_val_from',
                                            'b_val_to'])
        self.active = self.frame[self.frame.t_val_active == 1]
        self.inactive = self.frame[self.frame.t_val_active == 0]
        self.dates = self.inactive['t_val_from'].dt.date.unique()

    def overallNumber(self):
        sum_active = len(self.active)
        count_by_date = np.array([len(self.inactive[self.inactive.t_val_from.dt.date == date]) for date in self.dates])
        diff_by_average = self.diffPerc(np.average(count_by_date), sum_active)
        print('------------------------------------------')
        print('Difference by average %f' % diff_by_average)
        print('------------------------------------------')
        print('Difference between each number of inserts')
        count_by_date = np.append(count_by_date, sum_active)
        diff = np.diff(count_by_date)/count_by_date[:-1]*100
        print(diff)
        print('------------------------------------------')
        each = []
        for date in self.dates:
            new = sum_active
            old = len(self.inactive[self.inactive.t_val_from.dt.date == date])
            each.append(self.diffPerc(old, new))

        diff_by_date = pd.DataFrame(each, index=self.dates, columns=['difference'])
        print('Difference for active number of inserts for each of last 5 crawlers')
        print(diff_by_date)
        print('------------------------------------------')

    def placementAnalysis(self):
        num_placements_active = len(self.active.placement.unique())
        num_placements_by_date = np.array([len(self.inactive[self.inactive['t_val_from'].dt.date == date].placement.unique()) for date in self.dates])
        num_placements_by_date = np.append(num_placements_by_date, num_placements_active)
        diff = np.diff(num_placements_by_date)
        num_placements_frame = pd.DataFrame(num_placements_by_date,
                                            index=[date for date in self.frame['t_val_from'].dt.date.unique()],
                                            columns=['Number of placements'])

        preview_matrix = []
        for date in self.frame['t_val_from'].dt.date.unique():
            preview_matrix.append([len(a) for a in [self.frame[(self.frame.placement == placement) & (self.frame.t_val_from.dt.date == date)] for placement in self.frame.placement.unique()]])

        preview_frame = pd.DataFrame(preview_matrix, columns=[placement for placement in self.frame.placement.unique()],
                                     index=[date for date in self.frame['t_val_from'].dt.date.unique()])
        matrix = preview_matrix[:-1]
        matrix = np.array(matrix)
        active_placements = np.array(preview_matrix[-1])
        diff_matrix = []
        for arr in matrix:
            diff_matrix.append(self.diffPerc(arr, active_placements))
        diff_matrix = np.array(diff_matrix)
        diff_matrix[diff_matrix == inf] = 100.0
        diff_table = pd.DataFrame(diff_matrix, columns=[placement for placement in self.frame.placement.unique()], index=[date for date in self.dates])
        print('======================> Current state for last 6 crawlers <======================')
        print(preview_frame)
        print('------------------------------------------')
        print('======================> Difference for fresh data for each of last 5 crawlers <======================')
        print(diff_table)
        print('------------------------------------------')
        print('Number of placements for last 6 crawlers')
        print(num_placements_frame)
        print('Difference between each number of placements: ' + str(diff))

    def diffPerc(self, old, new):
        return (new-old)/old*100

