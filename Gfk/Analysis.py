import numpy as np
import pandas as pd
from numpy import inf
from Server.DB import DB


class GfkAnalysis:

    def __init__(self):
        self.db = DB()
        self.active_wkz = pd.DataFrame(self.db.getWkzDataSmile(), columns=['id', 'shop_id', 'pzn', 'position', 'placement_id', 't_val_from',
                                            't_val_to', 't_val_update', 't_val_del', 't_val_active', 'b_val_from',
                                            'b_val_to', 'placement'])
        self.inactive_wkz = pd.DataFrame(self.db.getWkzDataSmileTest(), columns=['id', 'shop_id', 'pzn', 'position', 'placement_id', 't_val_from',
                                            't_val_to', 't_val_update', 't_val_del', 't_val_active', 'b_val_from',
                                            'b_val_to', 'placement'])
        self.active_placements = pd.DataFrame(self.db.getPlacementSmile(), columns=['id', 'shop_id', 'placement', 'marken',
                                                                             'themen', 'link', 'screenshot_name',
                                                                             't_val_from', 't_val_to', 't_val_active'])
        self.inactive_placements = pd.DataFrame(self.db.getFivePlacementSmileTest(), columns=['id', 'shop_id', 'placement', 'marken',
                                                                             'themen', 'link', 'screenshot_name',
                                                                             't_val_from', 't_val_to', 't_val_active'])

    def overallNumber(self, shop_id):
        shop = self.inactive_wkz[self.inactive_wkz.shop_id == shop_id]
        if shop.empty:
            print('No data available for that shop. Try again.')
            return
        active = self.active_wkz[self.active_wkz.shop_id == shop_id]
        if active.empty:
            print('Shop didn\'t start yet. Try again later.')
            return
        inactive = self.inactive_wkz[self.inactive_wkz.shop_id == shop_id]
        dates = inactive['t_val_from'].dt.date.unique()
        sum_active = len(active)
        count_by_date = np.array([len(inactive[inactive.t_val_from.dt.date == date]) for date in dates])
        diff_by_average = self.diffPerc(np.average(count_by_date), sum_active)
        print('------------------------------------------')
        print('Number of inserted products active: %d' % sum_active)
        print('------------------------------------------')
        print('Difference by average %f' % diff_by_average)
        print('------------------------------------------')
        print('Difference between each number of inserts')
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
        print('Difference for active number of inserts for each of last 5 crawlers')
        print(diff_by_date)
        print('------------------------------------------')

    def placementAnalysis(self, shop_id):
        shop = self.inactive_wkz[self.inactive_wkz.shop_id == shop_id]
        inactive_placement = self.inactive_placements[self.inactive_placements.shop_id == shop_id]
        active_placement = self.active_placements[self.active_placements.shop_id == shop_id]
        shop_placement = pd.concat([inactive_placement, active_placement])
        if shop.empty:
            print('No data available for that shop. Try again.\n\n')
            return
        active = self.active_wkz[self.active_wkz.shop_id == shop_id]
        if active.empty:
            print('Shop didn\'t start yet. Try again later.\n\n')
            return
        inactive = self.inactive_wkz[self.inactive_wkz.shop_id == shop_id]
        shop = pd.concat([inactive, active])
        dates = inactive['t_val_from'].dt.date.unique()
        num_placements_active = len(active.placement.unique())
        num_placements_by_date = np.array([len(inactive[inactive['t_val_from'].dt.date == date].placement.unique()) for date in dates])
        num_placements_by_date = np.append(num_placements_by_date, num_placements_active)
        diff = np.diff(num_placements_by_date)
        num_placements_frame = pd.DataFrame(num_placements_by_date,
                                            index=[date for date in shop['t_val_from'].dt.date.unique()],
                                            columns=['Number of placements'])

        preview_matrix = []
        placement_matrix = []
        for date in shop['t_val_from'].dt.date.unique():
            preview_matrix.append([len(a) for a in [shop[(shop.placement == placement) & (shop.t_val_from.dt.date == date)] for placement in shop.placement.unique()]])
            placement_matrix.append([len(a) for a in [shop_placement[(shop_placement.placement == placement) & (shop_placement.t_val_from.dt.date == date)] for placement in shop_placement.placement.unique()]])

        preview_frame = pd.DataFrame(preview_matrix, columns=[placement for placement in shop.placement.unique()],
                                     index=[date for date in shop['t_val_from'].dt.date.unique()])
        placement_frame = pd.DataFrame(placement_matrix, columns=[placement for placement in shop_placement.placement.unique()],
                                     index=[date for date in shop['t_val_from'].dt.date.unique()])
        matrix = preview_matrix[:-1]
        matrix = np.array(matrix)
        active_placements = np.array(preview_matrix[-1])
        diff_matrix = []
        for arr in matrix:
            diff_matrix.append(self.diffPerc(arr, active_placements))
        diff_matrix = np.array(diff_matrix)
        diff_matrix[diff_matrix == inf] = 100.0
        diff_table = pd.DataFrame(diff_matrix, columns=[placement for placement in shop.placement.unique()], index=[date for date in dates])
        print('======================> Current state for number of products in last 6 crawlers <======================')
        print(preview_frame)
        print('------------------------------------------')
        print('======================> Difference for fresh data for each of last 5 crawlers <======================')
        print(diff_table)
        print('------------------------------------------')
        print('======================> Current state for number of placements in last 6 crawlers <====================')
        print(placement_frame)
        print('------------------------------------------')
        print('Number of placements for last 6 crawlers')
        print(num_placements_frame)
        print('Difference between each number of placements: ' + str(diff))
        print('\n')

    def diffPerc(self, old, new):
        return (new-old)/old*100

