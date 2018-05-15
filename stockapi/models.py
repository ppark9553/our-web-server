from django.db import models

STATE_TYPES = (
    ('P', 'Pass'),
    ('F', 'Fail'),
)

SIZE_TYPES = (
    ('L', 'Large Cap'), # large cap stocks
    ('M', 'Middle Cap'), # mid cap stocks
    ('S', 'Small Cap'), # small cap stocks
)

STYLE_TYPES = (
    ('G', 'Growth'), # growth stocks
    ('V', 'Value'), # value stocks
    ('D', 'Dividend'), # high dividend stocks
)


class StockapiState(models.Model):
    date = models.CharField(max_length=10)
    table_name = models.CharField(max_length=20)
    state = models.CharField(max_length=1, choices=STATE_TYPES)
    log = models.CharField(max_length=50,
                           blank=True,
                           null=True)

    def __str__(self):
        return '{} {}'.format(self.date, self.table_name)


class Date(models.Model):
    date = models.CharField(max_length=10)

    def __str__(self):
        return self.date


class Ticker(models.Model):
    '''
    - description: KOSPI & KOSDAQ & Index tickers updated daily
    - url: /stock-api/ticker/
    '''
    date = models.CharField(max_length=10)
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    market_type = models.CharField(max_length=10)
    state = models.BooleanField(default=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class OHLCV(models.Model):
    date = models.CharField(max_length=10)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    open_price = models.IntegerField()
    high_price = models.IntegerField()
    low_price = models.IntegerField()
    close_price = models.IntegerField()
    adj_close_price = models.IntegerField(blank=True, null=True)
    volume = models.IntegerField()
    short_volume = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.date, self.code)
