import mysql.connector


class DB:
    def __init__(self, country):
        self.cnx = mysql.connector.connect(user='root', password='',
                                           host='127.0.0.1',
                                           database='smile_' + country)
        self.cursor = self.cnx.cursor()

    def getData(self, shop):
        q = ("""select *
                    from (
                         select m.img_url, m.vid_url, p.price, p.title, p.availability, p.product_link, p.t_val_from,
                    CASE
                        WHEN p.t_val_to = '9999-12-31 00:00:00' THEN '2200-12-31 00:00:00'
                        WHEN p.t_val_to != '9999-12-31 00:00:00' THEN p.t_val_to
                    END as t_val_to, p.t_val_active, d.desc_plaintext
                    from media m
                      left join price p
                        on m.price_id = p.id
                         left join description d on d.price_id = p.id
                    where date(p.t_val_to) in (
                        select *
                            from (select distinct date(t_val_to) from price where domain_pzn_id like '0000{0}%' order by date(t_val_to) desc limit 5) as t
                        )
                    and p.domain_pzn_id like '0000{0}_%'
                      union
                      select m.img_url, m.vid_url, p.price, p.title, p.availability, p.product_link, p.t_val_from,
                    CASE
                        WHEN p.t_val_to = '9999-12-31 00:00:00' THEN '2200-12-31 00:00:00'
                        WHEN p.t_val_to != '9999-12-31 00:00:00' THEN p.t_val_to
                    END as t_val_to, p.t_val_active, d.desc_plaintext
                    from price p
                      left join media m
                        on m.price_id = p.id
                         left join description d on d.price_id = p.id
                    where date(p.t_val_to) in (
                        select *
                            from (select distinct date(t_val_to) from price where domain_pzn_id like '0000{0}%' order by date(t_val_to) desc limit 5) as t
                        )
                        and p.domain_pzn_id like '0000{0}_%'
                    ) as a""".format(shop))
        self.cursor.execute(q)
        data = self.cursor.fetchall()
        return data

    def getLinks(self, domain_id):
        q = ('select distinct link from maping_products where domain_id = %s')
        params = (domain_id,)
        self.cursor.execute(q, params)
        data = self.cursor.fetchall()
        return data

    def getKwData(self, domain_id):
        q = ("""select id, keyword_c_id, position, product_link, t_val_from, CASE
                        WHEN t_val_to = '9999-12-31 00:00:00' THEN '2200-12-31 00:00:00'
                        WHEN t_val_to != '9999-12-31 00:00:00' THEN t_val_to
                    END, t_val_active from keywords_data where domain_pzn_id like '0000{0}%' and date(t_val_to) in (
                    select * from (
                        select distinct date(t_val_to) from keywords_data where domain_pzn_id like '0000{0}%' order by date(t_val_to) desc limit 5
                    ) as kica
            )""".format(domain_id))
        self.cursor.execute(q)
        data = self.cursor.fetchall()
        return data

    def getKws(self):
        q = ('select id, keyword_c_id, keyword from keyword where negative_kws = 0 and keyword_remove = 0 and t_val_active = 1')
        self.cursor.execute(q)
        data = self.cursor.fetchall()
        return data
