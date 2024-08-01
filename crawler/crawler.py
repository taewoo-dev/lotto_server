from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

from models.lotto import Lotto


class Crawler:

    def __init__(self):
        ChromeDriverManager().install()
        browser = webdriver.Chrome()

        self._lotto_list: list[Lotto] = []
        self._browser = browser
        self._db_manager = None

    def crawling_lottos(self):
        url = "https://dhlottery.co.kr/gameResult.do?method=byWin"
        self._browser.get(url)
        self._browser.set_window_size(1920, 1080)

        # (1). 회차 선택
        # input_id = int(input("").strip())
        input_id = 500
        select = Select(self._browser.find_element(By.ID, "hdrwComb"))
        select2 = Select(self._browser.find_element(By.ID,"dwrNoList"))

        # 1~600 회차
        if input_id <= 600:
            select.select_by_value("2")
            select2.select_by_value(str(input_id))
            self._browser.find_element(By.CLASS_NAME, "header_article").click()
            button = WebDriverWait(self._browser, 20).until(
                EC.element_to_be_clickable((By.ID, "searchBtn"))
            )
            button.click()

        # 601~현재까지 회차
        else:
            select.select_by_value("1")
            select2.select_by_value(str(input_id))
            self._browser.find_element(By.CLASS_NAME, "header_article").click()
            button = WebDriverWait(self._browser, 20).until(
                EC.element_to_be_clickable((By.ID, "searchBtn"))
            )
            button.click()

        # (2). 로또 데이터 크롤링
        elem = self._browser.find_element(By.CLASS_NAME, "win_result")

        lotto_id: str = elem.find_element(By.TAG_NAME, "strong").text
        lotto_date: str = elem.find_element(By.CLASS_NAME, "desc").text[1:-4]

        lotto_numbers: list[str] = self._browser.find_element(By.CLASS_NAME, "num.win").text.split("\n")[1:]

        table = self._browser.find_element(By.CLASS_NAME, "tbl_data.tbl_data_col").find_elements(By.TAG_NAME, "tr")
        lotto_amounts = dict()
        for index, value in enumerate(table[1:]):
            lotto_amounts[index+1] = value.text.split(" ")[3]

        self._lotto_list.append(Lotto(lotto_id=lotto_id, lotto_date=lotto_date, lotto_numbers=lotto_numbers, lotto_amounts=lotto_amounts))

    @property
    def lotto_list(self):
        return self._lotto_list

