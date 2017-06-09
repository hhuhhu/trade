# -*- coding: utf-8 -*-
"""
@author: Daniel
@contact: 511735184@qq.com
@file: rqalpha_data_insert.py
@time: 2017/6/9 10:38
"""

import os
import json

import pandas as pd
from data.mongo import mongo_connect

from data.daybar_store import DayBarStore
from data.instrument_store import InstrumentStore
from data.converter import StockBarConverter, FutureDayBarConverter


class DataInsert:
    def __init__(self):

        self.client = mongo_connect()
        self.dir_path = self.path_get()

    def stock_insert(self):
        stock_db = self.client.stock
        stock = DayBarStore(os.path.join(self.dir_path, 'stocks.bcolz'), StockBarConverter)
        for stock_id in stock.index:
            stock_np = stock.get_bars(stock_id)
            stock_pd = pd.DataFrame(data=stock_np, columns=stock.fields)
            stock_pd['code'] = stock_id
            stock_db.daily.insert(json.loads(stock_pd.to_json(orient='records')))

    def future_insert(self):
        future_db = self.client.future
        future = DayBarStore(os.path.join(self.dir_path, 'futures.bcolz'), FutureDayBarConverter)
        for future_id in future.index:
            future_np = future.get_bars(future_id)
            future_pd = pd.DataFrame(data=future_np, columns=future.fields)
            future_pd['code'] = future_id
            future_db.daily.insert(json.loads(future_pd.to_json(orient='records')))

    def instrument_insert(self):
        stock_db = self.client.stock

        instrument = InstrumentStore(os.path.join(self.dir_path, 'instruments.pk'))
        instruments = instrument.instruments
        for _ in instruments:
            stock_db.instrument.insert(_)

    def dividend_insert(self):

        return

    def path_get(self):
        data_bundle_path = 'data/bundle/'
        path = os.path.abspath(os.path.dirname(__file__))
        dir_path = os.path.join(path, data_bundle_path)
        return dir_path


if __name__ == '__main__':
    di = DataInsert()
    # di.stock_insert()
    # di.instrument_insert()
