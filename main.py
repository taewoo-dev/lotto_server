from crawler.crawler import Crawler
from models.lotto import SelectLottoDto
from database.db import DBManger


def get_lotto_round(lotto_id: int):
    lotto_id = int(input("회차를 입력").strip())
    sql = """
    select lotto_numbers, lotto_bonus, lotto_first, lotto_second, lotto_third, lotto_4th, lotto_5th 
    from lottos where lotto_id = %s;
    """
    result = DBManger.excute_query(sql, 1129)



def compare_lotto_numbers(lotto_number: list[str], lotto_amounts: list[str]):
    count = 0
    user_lotto_number = input("로또 번호를 6개 입력: ,로 구분").strip().split(",")
    user_lotto_number.sort()
    for i in user_lotto_number:
        if i in lotto_number:
            count = count + 1

    if count == 6:
        print(f"1등 상금:{lotto_amounts[1]}")
    elif count == 5:
        print(f"2등 상금:{lotto_amounts[2]}")
    elif count == 4:
        print(f"3등 상금:{lotto_amounts[3]}")
    elif count == 3:
        print(f"4등 상금:{lotto_amounts[4]}")
    else:
        print("0원")

# (4). 로또 규칙 구체화
# (5). 보너스 점수


if __name__ == "__main__":
    # app = Crawler()
    # app.crawling_lottos()


