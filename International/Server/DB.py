import mysql.connector


class DB:
    def __init__(self, country):
        self.cnx = mysql.connector.connect(user='root', password='',
                                           host='127.0.0.1',
                                           database='smile_' + country)
        self.cursor = self.cnx.cursor()

    def getData(self, shop, order):
        q = ("""select m.img_url, m.vid_url, p.price, p.title, p.availability, p.product_link, p.t_val_from,
                CASE
                    WHEN p.t_val_to = '9999-12-31 00:00:00' THEN '2200-12-31 00:00:00'
                    WHEN p.t_val_to != '9999-12-31 00:00:00' THEN p.t_val_to
                END as t_val_to, p.t_val_active, d.desc_plaintext
                from {0}
                where date(p.t_val_to) in (
                  select *
                  from (select distinct date(t_val_to) from price where domain_pzn_id like '0000{1}%'  limit 5) as t
                  )
                and p.domain_pzn_id like '0000{2}_%'""".format(order, shop, shop))
        self.cursor.execute(q)
        data = self.cursor.fetchall()
        return data
