from collections import defaultdict


class Calculator(object):
    def __init__(self, df):
        # pass a dataframe
        self.df = df
        self.queues = []

    def calculate(self):
        # for each product generate a Queue
        for name, group in self.df.groupby('Product'):
            q = Queue(name)
            self.queues.append(q)
            rows = (
                row
                for row in group.sort_values(by="Date_Time").itertuples(index=False)
            )
            for row in rows:
                print(row)
                if row.Number > 0:
                    t = Transaction(
                        row.Date_Time,
                        row.Product,
                        row.ISIN,
                        row.Number,
                        row.Price,
                        row.Fee,
                    )
                    q.buy(t)
                elif row.Number < 0:
                    q.sell(row.Date_Time, row.Number, row.Price)

    def get_gains(self):
        for q in self.queues:
            if len(q.gain) > 0:
                print(q)



class Transaction(object):
    def __init__(self, date_time, product, isin, number, local_price, fee):
        self.date_time = date_time
        self.product = product
        self.isin = isin
        self.number = number
        self.local_price = local_price
        self.fee = fee
    
    def __str__(self):
        return "{}-{}-{}".format(self.date_time, self.number, self.local_price)


class Queue(object):
    def __init__(self, product):
        """Per product queue"""
        self.name = product
        self.queue = []
        self.gain = defaultdict(int)  # year: value

    def __str__(self):
        return "{}:\n{}".format(
            self.name,
            "\n".join(["\t{}: {}".format(year, gain) for year, gain in self.gain.items()])
        )

    def __repr__(self):
        return self.name

    def buy(self, transaction):
        self.queue.append(transaction)

    def sell(self, date_time, number, price):
        number = abs(number)
        while number > 0:
            transaction = self.queue[0]
            if number >= transaction.number:
                self.gain[date_time.year] += (price - transaction.local_price) * transaction.number
                number -= transaction.number
                self.queue.pop(0)
            elif number < transaction.number:
                self.gain[date_time.year] += (price - transaction.local_price) * number
                transaction.number -= number
                number = 0
