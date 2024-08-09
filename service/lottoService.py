"""
1. 로또 번호 입력 및 날짜 입력 -> 날짜를 기준으로 회차를 자동 판단하여 그 회차의 로또 번호 및 상금 가져오기
2. 사용자 로또 번호 생성 : 그 수에 맞춰 랜덤으로 6개 난수 생성 -> 데이터베이스 or csv파일로 유지
3. csv파일을 하나씩 읽어오면서 로또
"""
from models.lotto import SelectLottoDto
from database.db import DBManger
import random


class LottoService:
    def __init__(self):
        self._first_prize_count = 0
        self._second_prize_count = 0
        self._third_prize_count = 0
        self._4th_prize_count = 0
        self._5th_prize_count = 0
        self._total_prize_amount = 0

    def run(self):
        select_lotto_dto = self.__input_lotto_round()

        lotto_lists = self.__generate_random_numbers(int(input("로또 구매 갯수 입력 : ")))

        for lotto_list in lotto_lists:
            print(lotto_list)
            self.__compare_lotto_numbers(select_lotto_dto=select_lotto_dto, user_lotto_numbers=lotto_list)

        self.__display_lotto_results()

    def __input_lotto_round(self):
        lotto_id = int(input("원하는 회차를 입력하세요 : ").strip())
        select_lotto_dto = self.__get_lotto_round(lotto_id=lotto_id)
        print(f"{lotto_id}회차 로또 번호는 {select_lotto_dto.lotto_numbers.split(',')} + {select_lotto_dto.lotto_bonus} 입니다")
        return select_lotto_dto

    def __generate_random_numbers(self, count):
        return [sorted(random.sample(range(1, 46), 6)) for _ in range(count)]

    def __compare_lotto_numbers(self, select_lotto_dto: SelectLottoDto, user_lotto_numbers: list[str]):

        lotto_numbers = list(map(int, select_lotto_dto.lotto_numbers.split(",")))
        lotto_bonus = select_lotto_dto.lotto_bonus

        correct_count = 0
        bonus = False

        for user_lotto_number in user_lotto_numbers:
            if user_lotto_number in lotto_numbers:
                correct_count = correct_count + 1
            if user_lotto_number == lotto_bonus:
                bonus = True

        self.__check_lotto_winning_numbers(bonus, correct_count, select_lotto_dto)

    def __get_lotto_round(self, lotto_id: int) -> SelectLottoDto:
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
                              lotto_first=result["lotto_first"], lotto_second=result["lotto_second"],
                              lotto_third=result["lotto_third"],
                              lotto_4th=result["lotto_4th"], lotto_5th=result["lotto_5th"])

    def __check_lotto_winning_numbers(self, bonus, correct_count, select_lotto_dto):
        if correct_count == 6:
            print(f"축하합니다! 1등 당첨되었습니다 당첨금액은 {select_lotto_dto.lotto_first}입니다")
            self._first_prize_count += 1
            self.__calculate_total_prize(prize=int(select_lotto_dto.lotto_first[:-1].replace(',', '')))
        elif correct_count == 5 and bonus:
            print(f"축하합니다! 2등 당첨되었습니다 당첨금액은 {select_lotto_dto.lotto_second}입니다")
            self._second_prize_count += 1
            self.__calculate_total_prize(prize=int(select_lotto_dto.lotto_second[:-1].replace(',', '')))
        elif correct_count == 5:
            print(f"축하합니다! 3등 당첨되었습니다 당첨금액은 {select_lotto_dto.lotto_third}입니다")
            self._third_prize_count += 1
            self.__calculate_total_prize(prize=int(select_lotto_dto.lotto_third[:-1].replace(',', '')))
        elif correct_count == 4:
            print(f"축하합니다! 4등 당첨되었습니다 당첨금액은 {select_lotto_dto.lotto_4th}입니다")
            self._4th_prize_count += 1
            self.__calculate_total_prize(prize=int(select_lotto_dto.lotto_4th[:-1].replace(',', '')))
        elif correct_count == 3:
            print(f"축하합니다! 5등 당첨되었습니다 당첨금액은 {select_lotto_dto.lotto_5th}입니다")
            self._5th_prize_count += 1
            self.__calculate_total_prize(prize=int(select_lotto_dto.lotto_5th[:-1].replace(',', '')))

    def __calculate_total_prize(self, prize):
        self._total_prize_amount += prize

    def __display_lotto_results(self):
        print(f"총 당첨 횟수:")
        print(f"1등: {self._first_prize_count}회")
        print(f"2등: {self._second_prize_count}회")
        print(f"3등: {self._third_prize_count}회")
        print(f"4등: {self._4th_prize_count}회")
        print(f"5등: {self._5th_prize_count}회")
        print(f"\n총 상금: {self._total_prize_amount:,}원")


app = LottoService()
app.run()
