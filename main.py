from crawler.crawler import Crawler
from models.lotto import SelectLottoDto
from database.db import DBManger


def get_lotto_round(lotto_id: int) -> SelectLottoDto:
    """
    특정 회차의 로또 정보를 가져오는 함수
    :return: SelectLottoDto
    """
    db = DBManger()

    sql = """
    select lotto_numbers, lotto_bonus, lotto_first, lotto_second, lotto_third, lotto_4th, lotto_5th 
    from lottos where lotto_id = %s;
    """
    result = db.excute_query(sql, lotto_id)[0]

    return SelectLottoDto(lotto_numbers=result["lotto_numbers"], lotto_bonus=result["lotto_bonus"],
                          lotto_first=result["lotto_first"], lotto_second=result["lotto_second"], lotto_third=result["lotto_third"],
                          lotto_4th=result["lotto_4th"], lotto_5th=result["lotto_5th"])


def compare_lotto_numbers():

    lotto_id = int(input("회차를 입력").strip())

    select_lotto_dto = get_lotto_round(lotto_id=lotto_id)

    lotto_numbers = select_lotto_dto.lotto_numbers.split(",")
    lotto_bonus = select_lotto_dto.lotto_bonus

    user_lotto_numbers = input("로또 번호를 6개 입력: ,로 구분").strip().split(",")
    user_lotto_numbers.sort()

    correct_count = 0
    bonus = False

    for user_lotto_number in user_lotto_numbers:
        if user_lotto_number in lotto_numbers:
            correct_count = correct_count + 1
        if user_lotto_number == lotto_bonus:
            bonus = True

    if correct_count == 6:
        print(f"축하합니다! 1등 당첨되었습니다 당첨금액은 {select_lotto_dto.lotto_first}입니다")
    elif correct_count == 5 and bonus:
        print(f"축하합니다! 2등 당첨되었습니다 당첨금액은 {select_lotto_dto.lotto_second}입니다")
    elif correct_count == 5:
        print(f"축하합니다! 3등 당첨되었습니다 당첨금액은 {select_lotto_dto.lotto_second}입니다")
    elif correct_count == 4:
        print(f"축하합니다! 4등 당첨되었습니다 당첨금액은 {select_lotto_dto.lotto_second}입니다")
    elif correct_count == 3:
        print(f"축하합니다! 5등 당첨되었습니다 당첨금액은 {select_lotto_dto.lotto_second}입니다")
    else:
        print("아쉽지만 다음기회에")




if __name__ == "__main__":
    # app = Crawler()
    # app.crawling_lottos()
    compare_lotto_numbers()

