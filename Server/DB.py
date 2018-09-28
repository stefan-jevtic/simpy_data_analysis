import mysql.connector


class DB:
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', password='',
                                           host='127.0.0.1',
                                           database='smile')
        self.cursor = self.cnx.cursor()

    def lastFive(self):
        q = ('select b.*, p.placement from smile.wkz_home_banners_new b inner join smile.wkz_placements_new p on b.placement_id = p.id where date(b.t_val_from) in (select * from (select date(t_val_from) as datum from smile.wkz_home_banners_new group by datum order by datum desc limit 6) as t)')
        self.cursor.execute(q)
        data = self.cursor.fetchall()
        return data

    def lastFivePlacement(self):
        q = ('select * from smile.wkz_placements_new where date(t_val_from) in (select * from (select date(t_val_from) as datum from smile.wkz_placements_new group by datum order by datum desc limit 6) as t)')
        self.cursor.execute(q)
        data = self.cursor.fetchall()
        return data

    def getKeywordsDataSmileTest(self):
        q = ('select * from keywords_data  where date(t_val_from) in (select * from (select date(t_val_from) as datum from keywords_data group by datum order by datum desc limit 2) as t)')
        self.cursor.execute(q)
        data = self.cursor.fetchall()
        return data

    def getKeywordsDataSmile(self):
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

    def getCategoryDataSmileTest(self):
        q = ('select * from category  where date(t_val_from) in (select * from (select date(t_val_from) as datum from category group by datum order by datum desc limit 5) as t)')
        self.cursor.execute(q)
        data = self.cursor.fetchall()
        return data

    def getCategoryDataSmile(self):
        q = ('select * from scrapers_category')
        self.cursor.execute(q)
        data = self.cursor.fetchall()
        return data
