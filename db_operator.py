import sqlite3
import os
import pandas as pd
import datetime


class DBOperator():
    def __init__(self, dbname) -> None:
        self.conn = sqlite3.connect(os.path.join(os.getcwd(), dbname))

    def find_post(self, area, property_event):

        # return pd.read_sql_query(
        #     'SELECT * FROM post WHERE property_event=? and address LIKE ?',
        #     self.conn,
        #     params=(
        #         property_event,
        #         '%' + area +
        #         '%'))
        return pd.read_sql_query(
            'SELECT * FROM post WHERE 物件種目=? and 所在地 LIKE ?',
            self.conn,
            params=(
                property_event,
                '%' + area +
                '%'))


def get_now_date():
    dt_now = datetime.datetime.now()

    return dt_now.strftime('%Y%m%d')
