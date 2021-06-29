# from abc import ABCMeta, abstractmethod
from selenium import webdriver
import time
from selenium.webdriver.support.select import Select

# wait_time = 10

######################################################
# 共通定数
######################################################
PROPERTY_TYPE_INDEX = 0
PROPERTY_EVENT_INDEX = 1
PREFECTURE_INDEX = 2
LOCATION_NAME_INDEX = 3

# ボックスが配置されている番号
PROPERTY_TYPE_BOX_INDEX = 4
PROPERTY_EVENT_1_BOX_INDEX = 5
PROPERTY_EVENT_2_BOX_INDEX = 6
CHECK_OLD_PROPERTY_BOX_INDEX = 4
PRICE_START_BOX_INDEX = 11
PRICE_END_BOX_INDEX = 12
PREFECTURE_BOX_INDEX = 1
LOCATION_NAME_BOX_INDEX = 2
NEXT_PAGE_BUTTON_XPATH = '//button[@aria-label="Go to next page"]'


PROPERTY_TYPE_LAND_INDEX = 1
PROPERTY_TYPE_OLD_HOUSE_INDEX = 2
PROPERTY_TYPE_APART_INDEX = 3
PROPERTY_EVENT_LAND_INDEX = 1
PROPERTY_EVENT_LEASEHOLD_RIGHT_INDEX = 2
PROPERTY_EVENT_LAND_RIGHT_INDEX = 3
PROPERTY_EVENT_OLD_HOUSE_INDEX = 2
PROPERTY_EVENT_OLD_TERAS_INDEX = 4

######################################################
# 共通化関数
######################################################


def input_form_xpath(driver, xpath, text):
    form = driver.find_element_by_xpath(xpath)
    form.send_keys(text)


def input_form(driver, box_index, text):
    """form入力

    Args:
        driver (webdriver): selenium
        box_index (int): ボックス番号
        text (str): 入力テキスト
    """
    form = driver.find_elements_by_css_selector(
        '.p-textbox-input.form-control')[box_index]
    form.send_keys(text)


def click_checkbox(driver, box_index):
    """checkboxクリック

    Args:
        driver (webdriver): selenium
        box_index (str): element個数
    """
    check_box = driver.find_elements_by_class_name(
        'custom-control-input')[box_index]
    driver.execute_script("arguments[0].click();", check_box)


def click_checkbox_xpath(driver, xpath):
    """checkboxクリック

    Args:
        driver (webdriver): selenium
        box_index (str): element個数
    """
    check_box = driver.find_element_by_xpath(xpath)
    driver.execute_script("arguments[0].click();", check_box)


def click_button(driver, xpath):
    """ボタンクリック

    Args:
        xpath (str): ボタン要素のxpathを指定する
    """
    try:
        button = driver.find_element_by_xpath(xpath)
        button.click()
    except Exception:
        # クリック操作しない
        pass


def click_button_css(driver, css):
    button = driver.find_elements_by_css_selector(css)
    if len(button) == 12:
        button[5].click()
    else:
        button[6].click()


def select_dropdown(driver, box_index, index):
    """dropdown選択

    Args:
        driver (webdriver): selenium
        box_index (int): selectボックスの番号
        index (int): dropdown番号(0start)
    """
    dropdown_elements = driver.find_elements_by_css_selector(
        'select.p-selectbox-input.custom-select')
    dropdown_element = dropdown_elements[box_index]
    selected_dropdown_element = Select(dropdown_element)
    selected_dropdown_element.select_by_index(index)


###########################################################
# クラス定義
###########################################################


class PropertyType():
    """物件種別
        field:
            driver [webdriver]:selenium
            property_type_index[int]:物件種別のindex
    """

    def __init__(self, driver, property_type, xpath):
        self.driver = driver
        self.xpath = xpath

        if property_type == '売土地':
            self.property_type_index = PROPERTY_TYPE_LAND_INDEX
        elif property_type == '売一戸建':
            self.property_type_index = PROPERTY_TYPE_OLD_HOUSE_INDEX
        elif property_type == '売マンション':
            self.property_type_index = PROPERTY_TYPE_APART_INDEX

    def execute(self):
        select_dropdown(self.driver, self.xpath, self.property_type_index)


class PropertyEvent():
    def __init__(self, driver, xpath, property_event):
        self.driver = driver
        self.xpath = xpath

        if property_event == '売地':
            self.property_event_index = [PROPERTY_EVENT_LAND_INDEX, None]
        elif property_event == '借地権':
            self.property_event_index = [
                PROPERTY_EVENT_LEASEHOLD_RIGHT_INDEX, None]
        elif property_event == '底地権':
            self.property_event_index = [PROPERTY_EVENT_LAND_RIGHT_INDEX, None]
        elif property_event == '中古戸建':
            self.property_event_index = [
                PROPERTY_EVENT_OLD_HOUSE_INDEX,
                PROPERTY_EVENT_OLD_HOUSE_INDEX]
        elif property_event == '中古テラス':
            self.property_event_index = [
                PROPERTY_EVENT_OLD_HOUSE_INDEX,
                PROPERTY_EVENT_OLD_TERAS_INDEX]
        else:
            self.property_event_index = [None, None]

    def execute(self):
        # 物件種目1の入力
        if self.property_event_index[0] is not None:
            select_dropdown(
                self.driver,
                self.xpath[0],
                self.property_event_index[0])

        # 物件種目2の入力
        if self.property_event_index[1] is not None:
            select_dropdown(
                self.driver,
                self.xpath[1],
                self.property_event_index[1])


class CheckboxOldProperty():
    def __init__(self, driver, xpath):
        self.driver = driver
        self.xpath = xpath

    def execute(self):
        click_checkbox(self.driver, self.xpath)


class PriceBox():
    def __init__(self, driver, xpath, price):
        self.driver = driver
        self.xpath_start = xpath[0]
        self.xpath_end = xpath[1]
        self.price_start = price[0]
        self.price_end = price[1]

    def execute(self):
        # 開始値の入力
        input_form(self.driver, self.xpath_start, self.price_start)

        # 終値の入力
        input_form(self.driver, self.xpath_end, self.price_end)


class Area():
    def __init__(
            self,
            driver,
            xpath,
            prefecture,
            location):

        self.driver = driver
        self.xpath = xpath
        self.prefecture = prefecture
        self.location = location

    def execute(self):
        # 都道府県を入力
        input_form(self.driver, self.xpath[0], self.prefecture)

        # 所在地名1入力(存在しない場合があるのでその場合はスルー)
        if isinstance(self.location, str):
            input_form(self.driver, self.xpath[1], self.location)

# Context


class Inputter():
    def __init__(self, inputter):
        self.inputter = inputter

    def input(self):
        self.inputter.input()

# Strategy


class InputAlgorithm:
    def __init__(
            self,
            property_type,
            property_event,
            checkbox_old_property,
            price,
            area):
        self.property_type = property_type
        self.property_event = property_event
        self.checkbox_old_property = checkbox_old_property
        self.price = price
        self.area = area

    def input(self):
        # オーバーライドをしていない場合は例外を表示する
        raise NotImplementedError()


class LandInput(InputAlgorithm):
    def input(self):
        self.property_type.execute()
        self.property_event.execute()
        self.area.execute()


class OldHouseInput(InputAlgorithm):
    def input(self):
        self.property_type.execute()
        self.property_event.execute()
        self.checkbox_old_property.execute()
        self.price.execute()
        self.area.execute()


class ApartInput(InputAlgorithm):
    def input(self):
        self.property_type.execute()
        self.area.execute()


class Operator():
    def __init__(self, id, pw, url, wait_time=3):
        """初期化

        Args:
            id (str): login_id
            pw (str): login_password
            url (str): access_to_url
            wait_time (int, optional): 要素が表示されるまでの待機時間. Defaults to 10.
        """
        self.login_id = id
        self.login_pw = pw
        self.url = url
        self.wait_time = wait_time

    def open(self, profile_path, profile_dir):
        try:
            options = webdriver.chrome.options.Options()
            options.add_argument('--user-data-dir=' + profile_path)
            options.add_argument('--profile-directory=' + profile_dir)
            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(self.wait_time)
        except Exception:
            self.driver.close()

    def login(self):
        pass

    def download(self):
        html = self.driver.page_source
        return html

    def close(self):
        self.driver.close()


class ReinsOperator(Operator):

    def login(self):
        self.driver.get(self.url)

        input_form_xpath(self.driver, '//*[@id="__BVID__13"]', self.login_id)

        input_form_xpath(self.driver, '//*[@id="__BVID__16"]', self.login_pw)

        click_checkbox_xpath(self.driver, '//*[@id="__BVID__20"]')
        click_button(
            self.driver,
            '//*[@id="__layout"]/div/div/div[3]/div/div[3]/div/button')
        time.sleep(self.wait_time)

    def input_query(self, query):
        # 検索条件入力画面に遷移
        query_page_button = self.driver.find_element_by_xpath(
            '//*[@id="__layout"]/div/div/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div/div[1]/button')
        query_page_button.click()
        time.sleep(self.wait_time)

        # 検索条件をクエリから取得
        property_type = query[PROPERTY_TYPE_INDEX]
        property_event = query[PROPERTY_EVENT_INDEX]
        prefecture = query[PREFECTURE_INDEX]
        location_name = query[LOCATION_NAME_INDEX]

        # 各ボックスのインスタンス作成
        property_type_box = PropertyType(
            self.driver, property_type, PROPERTY_TYPE_BOX_INDEX)

        property_event_box = PropertyEvent(
            self.driver,
            [PROPERTY_EVENT_1_BOX_INDEX, PROPERTY_EVENT_2_BOX_INDEX],
            property_event)

        checkbox = CheckboxOldProperty(
            self.driver, CHECK_OLD_PROPERTY_BOX_INDEX)

        price = PriceBox(
            self.driver, [
                PRICE_START_BOX_INDEX, PRICE_END_BOX_INDEX], [
                0, 100000])
        area = Area(
            self.driver,
            [PREFECTURE_BOX_INDEX, LOCATION_NAME_BOX_INDEX],
            prefecture,
            location_name)

        if property_type == '売土地':
            inputter = Inputter(
                LandInput(
                    property_type_box,
                    property_event_box,
                    checkbox,
                    price,
                    area))
        elif property_type == '売一戸建':
            inputter = Inputter(
                OldHouseInput(
                    property_type_box,
                    property_event_box,
                    checkbox,
                    price,
                    area))
        else:
            inputter = Inputter(
                ApartInput(
                    property_type_box,
                    property_event_box,
                    checkbox,
                    price,
                    area))

        # 条件入力
        inputter.input()
        time.sleep(self.wait_time)
        # 検索実行
        # 検索結果が500件以上存在する場合のOKボタン操作
        buttons = self.driver.find_elements_by_css_selector(
            'button.btn.p-button.btn-primary.btn-block.px-0')
        for button in buttons:
            if button.text == '検索':
                self.driver.execute_script("arguments[0].click();", button)
                break

        time.sleep(self.wait_time)

        # 検索結果が500件以上存在する場合のOKボタン操作
        buttons = self.driver.find_elements_by_css_selector(
            'button.btn.btn-primary')
        for button in buttons:
            if button.text == 'OK':
                self.driver.execute_script("arguments[0].click();", button)
                break

        time.sleep(self.wait_time)

    def load_next_page(self):

        click_button(self.driver, NEXT_PAGE_BUTTON_XPATH)
