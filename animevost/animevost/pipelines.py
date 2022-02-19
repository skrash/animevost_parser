from itemadapter import ItemAdapter
import sqlite3 as sql


class AnimevostPipeline1:

    def process_item(self, item, spider):
        return item

    def open_spider(self, spider):
        try:
            connect = sql.connect('parser.db')
            with connect:
                cur = connect.cursor()
                query = cur.execute('CREATE TABLE IF NOT EXISTS anime_list (title VARCHAR(100) UNIQUE PRIMARY KEY,'
                                    'href VARCHAR(100), hash VARCHAR(20))')
                connect.commit()
                query2 = cur.execute('CREATE TABLE IF NOT EXISTS anime (id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(100), '
                                     'description TEXT, '
                                     'video_url VARCHAR(100), '
                                     'genres VARCHAR(100), '
                                     'main_pic VARCHAR(100), '
                                     'present_pic VARCHAR(300), '
                                     'FOREIGN KEY(title) REFERENCES anime_list(title) ON DELETE CASCADE)')
                connect.commit()
        except Exception as e:
            spider.log('===================================================')
            spider.log('DATABASE CREATION ERROR !')
            spider.log(str(e))
            spider.log('===================================================')

    def close_spider(self, spider):
        try:
            for anime in spider.dict_anime.items():
                connect = sql.connect('parser.db')
                with connect:
                    cur = connect.cursor()
                    query = cur.execute('INSERT INTO anime_list values (?,?,?)',
                                        tuple([anime[0], anime[1][0], anime[1][1]]))
                    connect.commit()
        except Exception as e:
            spider.log('===================================================')
            spider.log('DATABASE INSERT ERROR !')
            spider.log(str(e))
            spider.log('===================================================')

class AnimevostPipeline2:


    def process_item(self, item, spider):
        return item

    def open_spider(self, spider):
        try:
            con = sql.connect('parser.db')
            with con:
                cur = con.cursor()
                query_list = cur.execute('SELECT title,href FROM anime_list').fetchall()
        except Exception as e:
            spider.log('========================================')
            spider.log('FAILED SELECT FROM DATABASE !')
            spider.log(str(e))
            spider.log('========================================')
        spider.query = dict([i for i in query_list])

    def close_spider(self, spider):
        for anime in spider.result.items():
            try:
                con = sql.connect('parser.db')
                with con:
                    cur = con.cursor()
                    query_result = cur.execute('SELECT title FROM anime_list WHERE href = ?', (anime[0],)).fetchall()
                    cur.execute('INSERT INTO anime values (NULL, ?, NULL, ?, ?, NULL, NULL)', [query_result[0][0], anime[1][0], anime[1][1]])
                    con.commit()
            except Exception as e:
                spider.log('========================================')
                spider.log('FAILED SELECT OR INSERT TITLE FROM DATABASE !')
                spider.log(str(e))
                spider.log('========================================')
