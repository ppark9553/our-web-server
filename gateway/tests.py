from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from gateway.controllers import Controller

User = get_user_model()


# class StockapiTestCase(TestCase):
#     '''
#     Unit test all gateway units:
#     1. Controller
#     2. Action
#     3. Reducer
#     4. State
#     '''
#
#     def setUp(self):
#         print('Starting stockapi test')
#
#         # create Ticker data first, before saving other data
#         ticker, created = Ticker.objects.get_or_create(code='005930',
#                                                        name='삼성전자',
#                                                        market_type='KOSPI',
#                                                        state=1)
#         # ticker variable for ForeignKey
#         self.ticker = ticker
#
#         # test assertions
#         self.assertTrue(created, msg='failed to save Ticker data')
#         self.assertEqual(Ticker.objects.all().count(), 1, msg='Ticker data not created properly')
#
#     def test_controller_is_singleton(self):
#         c = Controller()
