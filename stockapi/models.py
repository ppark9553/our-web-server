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


class MarketCapital(models.Model):
    date = models.CharField(max_length=10)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    comm_cls_prc = models.IntegerField() # 종가
    comm_stk_qty = models.IntegerField() # 보통주 상장주식수
    pref_stk_qty = models.IntegerField() # 우선주 상장주식수
    comm_stk_qty_af = models.IntegerField() # 보통주 상장예정주식수
    pref_stk_qty_af = models.IntegerField() # 우선주 상장예정주식수
    mkt_cap_comm = models.IntegerField() # 보통주 시가총액
    mkt_cap = models.IntegerField() # 시가총액

    def __str__(self):
        return '{} {}'.format(self.date, self.code)


class BuySell(models.Model):
    date = models.CharField(max_length=10)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    forgn_b = models.IntegerField()
    forgn_s = models.IntegerField()
    forgn_n = models.IntegerField()
    private_b = models.IntegerField()
    private_s = models.IntegerField()
    private_n = models.IntegerField()
    inst_b = models.IntegerField()
    inst_s = models.IntegerField()
    inst_n = models.IntegerField()
    trust_b = models.IntegerField()
    trust_s = models.IntegerField()
    trust_n = models.IntegerField()
    pension_b = models.IntegerField()
    pension_s = models.IntegerField()
    pension_n = models.IntegerField()
    etc_inst_b = models.IntegerField()
    etc_inst_s = models.IntegerField()
    etc_inst_n = models.IntegerField()

    def __str__(self):
        return '{} {}'.format(self.date, self.code)


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
