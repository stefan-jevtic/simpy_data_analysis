import mysql.connector


class DB:
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', password='',
                                           host='127.0.0.1',
                                           database='smile')
        self.cursor = self.cnx.cursor()

    def lastFive(self):
        q = ('select * from gkf_home_banners where date(t_val_from) in (select * from (select date(t_val_from) as datum from gkf_home_banners group by datum order by datum desc limit 6) as t)')
        self.cursor.execute(q)
        data = self.cursor.fetchall()
        return data

    def getDataSmileTest(self):
        q = ('select * from keywords_data  where date(t_val_from) in (select * from (select date(t_val_from) as datum from keywords_data group by datum order by datum desc limit 2) as t)')
        self.cursor.execute(q)
        data = self.cursor.fetchall()
        return data

    def getDataSmile(self):
        q = ('select * from scrapers_keywords_data')
        self.cursor.execute(q)
        data = self.cursor.fetchall()
        return data

    def getKeywords(self):
        q = ('select * from keyword where t_val_active = 1 and keyword_remove = 0 and negative_kws = 0')
        self.cursor.execute(q)
        data = self.cursor.fetchall()
        return data

    def getDomains(self):
        q = ('select id, domain, name, keywords_link from domains where t_val_active = 1')
        self.cursor.execute(q)
        data = self.cursor.fetchall()
        return data
