class Currency(models.Model):
    name = models.CharField(max_length=10)
    symbol = models.CharField(max_length=3, default="€")
    rate = models.DecimalField("exchange rate", default=1.0, decimal_places=2, max_digits=6)
    datetime = models.DateTimeField("exchange rate date & time", default=timezone.now)


class Share(models.Model):
    name = models.CharField("share name", max_length=20)
    isin = models.CharField("ISIN of the product", max_length=20)
    symbol = models.CharField("share symbol", max_length=6)
    exchange = models.CharField("stock exchange", max_length=3)
    price = models.DecimalField("price in original currency", decimal_places=2, max_digits=6)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return self.name    


class Transaction(models.Model):
    datetime = models.DateTimeField("transaction date", default=timezone.now)
    product = models.ForeignKey(Share, on_delete=models.CASCADE)
    number = models.IntegerField("number of items")
    local_value = models.DecimalField("value condsidering exchange rates", decimal_places=2, max_digits=6)
    fees = models.DecimalField("all of the associated fees", decimal_places=2, max_digits=6)
    order_id = models.CharField("unique transaction ID", unique=True, max_length=50)