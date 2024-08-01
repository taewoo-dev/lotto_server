# 로또 엔테티 및 DTO class

class Lotto:

    def __init__(self, lotto_id, lotto_date, lotto_numbers, lotto_amounts):
        self._lotto_id: int = lotto_id
        self._lotto_date: str = lotto_date
        self._lotto_numbers: int = lotto_numbers
        self._lotto_amounts: dict[str] = lotto_amounts

    def __str__(self):
        return f"{self._lotto_id}, {self._lotto_date}, {self._lotto_numbers}, {self._lotto_amounts}"

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
    def lotto_amounts(self):
        return self._lotto_amounts


class LottoDto:

    def __init__(self):
        pass
