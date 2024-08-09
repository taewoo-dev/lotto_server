from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

from models.lotto import Lotto
from database.db import DBManger


class Crawler:

    def __init__(self):
        ChromeDriverManager().install()
        browser = webdriver.Chrome()

        self._lotto_list: list[Lotto] = []
        self._browser = browser
        self._db_manager = DBManger()

    def crawling_lottos(self):
        url = "https://dhlottery.co.kr/gameResult.do?method=byWin"
        self._browser.get(url)
        self._browser.set_window_size(1920, 1080)

        # (1). 회차 선택

        for input_id in range(1,1301):

            select = Select(self._browser.find_element(By.ID, "hdrwComb"))
            select2 = Select(self._browser.find_element(By.ID, "dwrNoList"))

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

            lotto_id: int = int(elem.find_element(By.TAG_NAME, "strong").text[:-1])

            lotto_date: str = elem.find_element(By.CLASS_NAME, "desc").text[1:-4]

            lotto_numbers: str = ",".join(self._browser.find_element(By.CLASS_NAME, "num.win").text.split("\n")[1:])

            lotto_bonus: str = self._browser.find_element(By.CLASS_NAME, "num.bonus").find_element(By.TAG_NAME, "p").text

            table = self._browser.find_element(By.CLASS_NAME, "tbl_data.tbl_data_col").find_elements(By.TAG_NAME, "tr")

            lotto_amounts = dict()
            for index, value in enumerate(table[1:]):
                lotto_amounts[index + 1] = value.text.split(" ")[3]

            self._lotto_list.append(
                Lotto(lotto_id=lotto_id, lotto_date=lotto_date, lotto_numbers=lotto_numbers, lotto_bonus=lotto_bonus, lotto_first=lotto_amounts[1],
                      lotto_second=lotto_amounts[2], lotto_third=lotto_amounts[3], lotto_4th=lotto_amounts[4],
                      lotto_5th=lotto_amounts[5]))

            self.save_lotto(
                Lotto(lotto_id=lotto_id, lotto_date=lotto_date, lotto_numbers=lotto_numbers, lotto_bonus=lotto_bonus, lotto_first=lotto_amounts[1],
                      lotto_second=lotto_amounts[2], lotto_third=lotto_amounts[3], lotto_4th=lotto_amounts[4],
                      lotto_5th=lotto_amounts[5]))

        self._browser.quit()

    def save_lotto(self, insert_lotto: Lotto):
        sql = """
        insert into lottos (lotto_id, lotto_date, lotto_numbers, lotto_bonus, lotto_first, lotto_second, lotto_third, lotto_4th, lotto_5th)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        self._db_manager.excute_query(sql, insert_lotto.lotto_id, insert_lotto.lotto_date, insert_lotto.lotto_numbers, insert_lotto.lotto_bonus,
                                      insert_lotto.lotto_first, insert_lotto.lotto_second, insert_lotto.lotto_third,
                                      insert_lotto.lotto_4th,insert_lotto.lotto_5th)

