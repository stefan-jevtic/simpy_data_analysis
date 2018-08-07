import mysql.connector


class DB:
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', password='',
                                           host='127.0.0.1',
                                           database='smile')
        self.cursor = self.cnx.cursor()

    def lastFive(self, shop_id):
        q = ('select * from gkf_home_banners where shop_id = %s and date(t_val_from) in (select * from (select date(t_val_from) as datum from gkf_home_banners group by datum order by datum desc limit 6) as t)')
        self.cursor.execute(q, (shop_id,))
        data = self.cursor.fetchall()
        return data
