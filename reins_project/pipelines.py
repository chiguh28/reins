# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import sqlite3


class ItemDataBase():
    _db = None
    _dbname = 'reins.db'

    @classmethod
    def get_database(cls):
        cls._db = sqlite3.connect(
            os.path.join(os.getcwd(), cls._dbname))

        # テーブル作成
        cursor = cls._db.cursor()
        # cursor.execute(
        #     'CREATE TABLE IF NOT EXISTS post(\
        #         id INTEGER PRIMARY KEY,\
        #         transaction_mode TEXT NOT NULL,\
        #         trading_conditions TEXT NOT NULL,\
        #         property_event TEXT NOT NULL,\
        #         price TEXT NOT NULL,\
        #         use_area TEXT NOT NULL,\
        #         building_coverage_ratio TEXT NOT NULL,\
        #         floor_area_ratio TEXT NOT NULL,\
        #         area_square TEXT NOT NULL,\
        #         area_unit_price TEXT NOT NULL,\
        #         tsubo_unit_price TEXT NOT NULL,\
        #         tsubo_unit_price_num INTEGER NOT NULL,\
        #         roadside_situation TEXT NOT NULL,\
        #         road TEXT NOT NULL,\
        #         address TEXT NOT NULL,\
        #         stations_along_the_line TEXT NOT NULL,\
        #         trade_name TEXT NOT NULL,\
        #         phone_number TEXT NOT NULL,\
        #         access TEXT NOT NULL\
        #     );')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS post(\
                物件番号 INTEGER PRIMARY KEY,\
                取引態様 TEXT NOT NULL,\
                取引状況 TEXT NOT NULL,\
                物件種目 TEXT NOT NULL,\
                価格 TEXT NOT NULL,\
                用途地域 TEXT NOT NULL,\
                建ぺい率 TEXT NOT NULL,\
                容積率 TEXT NOT NULL,\
                土地面積 TEXT NOT NULL,\
                ㎡単価 TEXT NOT NULL,\
                坪単価 TEXT NOT NULL,\
                坪単価数値 INTEGER NOT NULL,\
                接道状況 TEXT NOT NULL,\
                接道 TEXT NOT NULL,\
                所在地 TEXT NOT NULL,\
                沿線駅 TEXT NOT NULL,\
                商号 TEXT NOT NULL,\
                電話番号 TEXT NOT NULL,\
                交通 TEXT NOT NULL\
            );')

        return cls._db

    def save_post(self, item):
        """
        item を DB に保存する

        備考:

        """

        if self.find_post(item['id']):
            # 保存されていれば保存をしない
            return

        db = self.get_database()
        # db.execute(
        #     'INSERT INTO post (id,transaction_mode,trading_conditions,property_event,price,use_area,building_coverage_ratio,floor_area_ratio,area_square,area_unit_price,tsubo_unit_price,tsubo_unit_price_num,roadside_situation,road,address,stations_along_the_line,trade_name,phone_number,access) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        #     (item['id'],
        #      item['transaction_mode'],
        #      item['trading_conditions'],
        #      item['property_event'],
        #      item['price'],
        #      item['use_area'],
        #      item['building_coverage_ratio'],
        #      item['floor_area_ratio'],
        #      item['area_square'],
        #      item['area_unit_price'],
        #      item['tsubo_unit_price'],
        #      item['tsubo_unit_price_num'],
        #      item['roadside_situation'],
        #      item['road'],
        #      item['address'],
        #      item['stations_along_the_line'],
        #      item['trade_name'],
        #      item['phone_number'],
        #      item['access']))
        db.execute(
            'INSERT INTO post (物件番号,取引態様,取引状況,物件種目,価格,用途地域,建ぺい率,容積率,土地面積,㎡単価,坪単価,坪単価数値,接道状況,接道,所在地,沿線駅,商号,電話番号,交通) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (item['id'],
             item['transaction_mode'],
             item['trading_conditions'],
             item['property_event'],
             item['price'],
             item['use_area'],
             item['building_coverage_ratio'],
             item['floor_area_ratio'],
             item['area_square'],
             item['area_unit_price'],
             item['tsubo_unit_price'],
             item['tsubo_unit_price_num'],
             item['roadside_situation'],
             item['road'],
             item['address'],
             item['stations_along_the_line'],
             item['trade_name'],
             item['phone_number'],
             item['access']))
        db.commit()

    def find_post(self, id):
        db = self.get_database()
        # cursor = db.execute(
        #     'SELECT * FROM post WHERE id=?',
        #     (id,)
        # )
        cursor = db.execute(
            'SELECT * FROM post WHERE 物件番号=?',
            (id,)
        )
        return cursor.fetchone()

    def check_chg_post(self, item):
        '''
        DBと変化しているかを確認

        同一URLが存在した場合にのみ駆動させる
        '''
        pass

    def update_post_price(self, id, price):
        '''
        priceレコードを更新

        Parameters:
            id: レコード特定に使用
            price: 更新値
        '''

        pass


class ReinsProjectPipeline:
    item_db = ItemDataBase()

    def process_item(self, item, spider):
        """
        Pipeline にデータが渡される時に実行される
        item に spider から渡された item がセットされる
        """
        self.item_db.save_post(item)

        return item
