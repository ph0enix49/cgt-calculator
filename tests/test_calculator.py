import unittest

import pandas as pd

from lib.calculator import Calculator
from lib.io import Importer

FIXTURES = "tests/fixtures.csv"


class TestCalculator(unittest.TestCase):
    def setUp(self):
        csv_importer = Importer(FIXTURES)
        transactions_df = csv_importer.import_csv()
        self.calculator = Calculator(
            transactions_df      
        )
        self.calculator.calculate()
    
    def test_init(self):
        assert isinstance(self.calculator, Calculator)

    def test_get_gains(self):
        gains_ref = ('{"index":{"0":{"gain":{"2019":82.8801608579,"2020":49.4627604496,"2018":0},"queue":[]},"1":{"gain":{"2020":248.97,"2018":0,"2019":0},"queue":[]},"2":{"gain":{"2020":-294.0870149755,"2018":0,"2019":0},"queue":[]},"3":"Grand Totals"},"2018":{"0":0.0,"1":0.0,"2":0.0,"3":0.0},"2019":{"0":82.8801608579,"1":0.0,"2":0.0,"3":82.8801608579},"2020":{"0":49.4627604496,"1":248.97,"2":-294.0870149755,"3":4.3457454741},"Total":{"0":132.3429213075,"1":248.97,"2":-294.0870149755,"3":87.225906332}}')
        assert self.calculator.get_gains().to_json() == gains_ref


if __name__ == '__main__':
    unittest.main()