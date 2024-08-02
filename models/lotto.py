# 로또 엔테티 및 DTO class


class Lotto:

    def __init__(self, lotto_id, lotto_date, lotto_numbers, lotto_bonus, lotto_first, lotto_second, lotto_third, lotto_4th, lotto_5th):
        self._lotto_id: int = lotto_id
        self._lotto_date: str = lotto_date
        self._lotto_numbers: str = lotto_numbers
        self._lotto_bonus: str = lotto_bonus
        self._lotto_first: str = lotto_first
        self._lotto_second: str = lotto_second
        self._lotto_third: str = lotto_third
        self._lotto_4th: str = lotto_4th
        self._lotto_5th: str = lotto_5th

    def __str__(self):
        return f"{self._lotto_id}, {self._lotto_date}, {self._lotto_numbers}"

    @property
    def lotto_id(self):
        return self._lotto_id

    @property
    def lotto_date(self):
        return self._lotto_date

    @property
    def lotto_numbers(self):
        return self._lotto_numbers

    @property
    def lotto_bonus(self):
        return self._lotto_bonus

    @property
    def lotto_first(self):
        return self._lotto_first

    @property
    def lotto_second(self):
        return self._lotto_second

    @property
    def lotto_third(self):
        return self._lotto_third

    @property
    def lotto_4th(self):
        return self._lotto_4th

    @property
    def lotto_5th(self):
        return self._lotto_5th


class SelectLottoDto:

    def __init__(self, lotto_numbers, lotto_bonus, lotto_first, lotto_second, lotto_third, lotto_4th, lotto_5th):
        self._lotto_numbers: str = lotto_numbers
        self._lotto_bonus: str = lotto_bonus
        self._lotto_first: str = lotto_first
        self._lotto_second: str = lotto_second
        self._lotto_third: str = lotto_third
        self._lotto_4th: str = lotto_4th
        self._lotto_5th: str = lotto_5th

