
class TableOrder:
    def __init__(self, country, shop_id):
        self.order = self.orderTables(country, int(shop_id))

    def orderTables(self, country, shop):
        order = ''
        if country == 'ru':
            if shop in [1, 2, 5, 6]:
                order = 'media m left join price p on m.price_id = p.id left join description d on d.price_id = p.id'
            elif shop in [3, 4, 5]:
                order = 'price p left join media m on m.price_id = p.id left join description d on d.price_id = p.id'
            else:
                raise Exception('Shop does not exists in country')
        elif country == 'at':
            pass
        elif country == 'es':
            pass
        elif country == 'uk':
            pass
        elif country == 'fr':
            pass
        else:
            raise Exception('Country does not exist in project')

        return order
