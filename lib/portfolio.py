import numpy as np
import pandas as pd


class Portfolio(object):
    def __init__(self, transactions):
        self.transactions = transactions
    
    def plain_view(self):
        # generate a pivot table of all transactions
        pivot = pd.pivot_table(
            self.transactions,
            index=["Product", "ISIN"],
            values=["Quantity", "Price"],
            aggfunc={"Quantity": np.sum, "Price": np.mean},
        )
        # select only open positions
        pivot = pivot.loc[pivot["Quantity"] > 0]
        # move index into columns
        pivot.reset_index(level=pivot.index.names, inplace=True)
        return pivot