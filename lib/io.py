import pandas as pd


class Importer(object):
    def __init__(self, filename):
        self.filename = filename
    
    def import_csv(self):
        # tested on Degiro transactions
        out = pd.read_csv(
            self.filename,
            parse_dates=[[0,1]],
            infer_datetime_format=True,
            dayfirst=True,
        )
        out = out.fillna(value={
            "Exchange rate": 1.0,
            "Transaction": 0,
        })
        return out