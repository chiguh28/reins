import scrapy
import pandas as pd
from bs4 import BeautifulSoup
from reins_project.items import ReinsProjectItem
import re


class ReinsSpider(scrapy.Spider):
    name = 'reins'
    allowed_domains = ['system.reins.jp']

    def start_requests(self):
        self.query_list = pd.read_csv(
            'property_search.csv').values.tolist()
        self.index = 0
        query = self.query_list[self.index]
        print(query)
        yield scrapy.Request(url="https://system.reins.jp/login/main/KG/GKG001200",
                             meta={'query': query, 'next': False},
                             callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")

        table_body = soup.find('div', class_='p-table-body')

        property_list = table_body.find_all('div', class_='p-table-body-row')

        for property in property_list:

            id = self.getText(
                property, 'grid-row-start: 1; grid-column: 2 / span 3;')
            transaction_mode = self.getText(
                property, 'grid-row-start: 2; grid-column: 2 / span 3;')
            trading_conditions = self.getText(
                property, 'grid-row-start: 3; grid-column: 2 / span 6;')
            property_event = self.getText(
                property, 'grid-row-start: 1; grid-column: 5 / span 5;')
            price = self.getText(
                property, 'grid-row-start: 2; grid-column: 5 / span 3;')
            use_area = self.getText(
                property, 'grid-row-start: 2; grid-column: 8 / span 2;')
            building_coverage_ratio = self.getText(
                property, 'grid-row-start: 3; grid-column: 8 / span 2;')
            floor_area_ratio = self.getText(
                property, 'grid-row-start: 4; grid-column: 8 / span 2;')
            area_square = self.getText(
                property, 'grid-row-start: 1; grid-column: 10 / span 3;')
            area_unit_price = self.getText(
                property, 'grid-row-start: 2; grid-column: 10 / span 3;')

            tsubo_unit_price = self.getText(
                property, 'grid-row-start: 3; grid-column: 10 / span 3;')
            if '万円' in tsubo_unit_price:
                tsubo_unit_price_num = self.replace_price_text2price(
                    tsubo_unit_price)

                roadside_situation = self.getText(
                    property, 'grid-row-start: 4; grid-column: 10 / span 3;')
                road = self.getText(
                    property, 'grid-row-start: 5; grid-column: 10 / span 3;')
            else:
                [tsubo_unit_price, tsubo_unit_price_num] = self.calc_tsubo_unit(
                    price, area_square)
                roadside_situation = self.getText(
                    property, 'grid-row-start: 3; grid-column: 10 / span 3;')
                road = self.getText(
                    property, 'grid-row-start: 4; grid-column: 10 / span 3;')

            address = self.getText(
                property, 'grid-row-start: 1; grid-column: 13 / span 12;')
            stations_along_the_line = self.getText(
                property, 'grid-row-start: 3; grid-column: 13 / span 6;')
            trade_name = self.getText(
                property, 'grid-row-start: 4; grid-column: 13 / span 12;')
            phone_number = self.getText(
                property, 'grid-row-start: 5; grid-column: 13 / span 6;')
            access = self.getText(
                property, 'grid-row-start: 3; grid-column: 19 / span 6;')

            yield ReinsProjectItem(id=id,
                                   transaction_mode=transaction_mode,
                                   trading_conditions=trading_conditions,
                                   property_event=property_event,
                                   price=price,
                                   use_area=use_area,
                                   building_coverage_ratio=building_coverage_ratio,
                                   floor_area_ratio=floor_area_ratio,
                                   area_square=area_square,
                                   area_unit_price=area_unit_price,
                                   tsubo_unit_price=tsubo_unit_price,
                                   tsubo_unit_price_num=tsubo_unit_price_num,
                                   roadside_situation=roadside_situation,
                                   road=road,
                                   address=address,
                                   stations_along_the_line=stations_along_the_line,
                                   trade_name=trade_name,
                                   phone_number=phone_number,
                                   access=access
                                   )
        next_button = soup.find(
            'button',
            attrs={
                'role': 'menuitem',
                'class': 'page-link',
                'aria-label': 'Go to next page'})
        if next_button is not None:
            yield scrapy.Request(url="https://system.reins.jp/login/main/KG/GKG001200",
                                 meta={'query': '', 'next': True},
                                 callback=self.parse)
        elif self.index < len(self.query_list):
            self.index += 1
            query = self.query_list[self.index]
            yield scrapy.Request(url="https://system.reins.jp/login/main/KG/GKG001200",
                                 meta={'query': query, 'next': False},
                                 callback=self.parse)

    def getText(self, property, style):
        block = property.find(
            'div',
            attrs={
                'class': 'p-table-body-item',
                'style': style})
        text = ''
        if block is not None:
            span_block = block.find('span', class_='d-sm-none')
            if span_block is not None:
                text = span_block.text
            else:
                text = block.text
        return text

    def replace_price_text2price(self, price_text):
        price = 0

        # 〇〇万円を数値に変換する
        if '万円' in price_text:
            p = r",|\D"
            num = int(re.sub(p, '', price_text))
            price = num * 10000
        return int(price)

    def text2price(self, text):
        p = r",|万円|㎡"
        num = float(re.sub(p, '', text))
        return num

    def calc_tsubo_unit(self, price, area):
        tsubo_unit = self.text2price(price) / (self.text2price(area) * 0.3025)
        return [str(tsubo_unit) + '万円', tsubo_unit]
