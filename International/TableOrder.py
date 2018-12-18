
class TableOrder:
    def __init__(self, country, shop_id):
        self.country = country
        self.shop_id = shop_id

    def orderTables(self):
        if self.country == 'ru':
            if self.shop_id not in [1, 2, 3, 4, 5, 6, 7]:
                raise Exception('Shop does not exists in country')
        elif self.country == 'at':
            if self.shop_id not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                raise Exception('Shop does not exists in country')
        elif self.country == 'es':
            if self.shop_id not in [1, 2, 3, 4, 5, 6, 7]:
                raise Exception('Shop does not exists in country')
        elif self.country == 'uk':
            if self.shop_id not in [1, 2, 3, 4, 5, 6, 7]:
                raise Exception('Shop does not exists in country')
        elif self.country == 'fr':
            if self.shop_id not in [1, 2, 3, 4, 5, 6]:
                raise Exception('Shop does not exists in country')
        else:
            raise Exception('Country does not exist in project')
