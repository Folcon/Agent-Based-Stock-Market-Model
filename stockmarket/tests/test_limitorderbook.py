"""This file runs tests for all functions in agents"""
import pytest

from stockmarket.limitorderbook import *
from stockmarket.agent import Trader
from stockmarket.firms import Firm
from stockmarket.stock import Stock
from stockmarket.valuationfunctions import *
from numpy.testing import assert_equal, assert_raises

@pytest.fixture()
def agents():
    return [Trader(name="Agent1", money=1000, bid_ask_spread=0, ma_short=2, ma_long=3,
                   valuation_function=lambda **x: extrapolate_average_profit(**x),
                   propensity_to_switch=1.1, price_to_earnings_window=(6,12), trader_volume_risk_aversion= 0.1),
            Trader(name="Agent2", money=1000, bid_ask_spread=0, ma_short=2, ma_long=3,
                   valuation_function=lambda **x: extrapolate_ma_price(**x),
                   propensity_to_switch=1.1, price_to_earnings_window=(6,12), trader_volume_risk_aversion= 0.1),
            Trader(name="Agent3", money=1000, bid_ask_spread=0, ma_short=2, ma_long=3,
                   valuation_function=lambda **x: extrapolate_average_profit(**x),
                   propensity_to_switch=1.1, price_to_earnings_window=(6, 12), trader_volume_risk_aversion=0.1),
            Trader(name="Agent4", money=1000, bid_ask_spread=0, ma_short=2, ma_long=3,
                   valuation_function=lambda **x: extrapolate_ma_price(**x),
                   propensity_to_switch=1.1, price_to_earnings_window=(6, 12), trader_volume_risk_aversion=0.1),
            Trader(name="Agent5", money=1000, bid_ask_spread=0, ma_short=2, ma_long=3,
                   valuation_function=lambda **x: extrapolate_average_profit(**x),
                   propensity_to_switch=1.1, price_to_earnings_window=(6, 12), trader_volume_risk_aversion=0.1),
            Trader(name="Agent6", money=1000, bid_ask_spread=0, ma_short=2, ma_long=3,
                   valuation_function=lambda **x: extrapolate_ma_price(**x),
                   propensity_to_switch=1.1, price_to_earnings_window=(6, 12), trader_volume_risk_aversion=0.1),
            Trader(name="Agent7", money=1000, bid_ask_spread=0, ma_short=2, ma_long=3,
                   valuation_function=lambda **x: extrapolate_average_profit(**x),
                   propensity_to_switch=1.1, price_to_earnings_window=(6, 12), trader_volume_risk_aversion=0.1),
            Trader(name="Agent8", money=1000, bid_ask_spread=0, ma_short=2, ma_long=3,
                   valuation_function=lambda **x: extrapolate_ma_price(**x),
                   propensity_to_switch=1.1, price_to_earnings_window=(6, 12), trader_volume_risk_aversion=0.1),
            Trader(name="Agent9", money=1000, bid_ask_spread=0, ma_short=2, ma_long=3,
                   valuation_function=lambda **x: extrapolate_average_profit(**x),
                   propensity_to_switch=1.1, price_to_earnings_window=(6, 12), trader_volume_risk_aversion=0.1),
            Trader(name="Agent10", money=1000, bid_ask_spread=0, ma_short=2, ma_long=3,
                   valuation_function=lambda **x: extrapolate_ma_price(**x),
                   propensity_to_switch=1.1, price_to_earnings_window=(6, 12), trader_volume_risk_aversion=0.1)


            ]

@pytest.fixture()
def limitorderbooks():
    # create a firm
    firm = Firm("Firm1", 10000, [200, 300, 400, 300])
    # create a stock of that firm
    stocks = Stock(firm, 1000)
    return [LimitOrderBook(stocks, 100, 120, initial_bid_ask=(1, 1))]

def test_add_bid(limitorderbooks):
    limitorderbooks[0].add_bid(10, 20, 'trader-1')
    limitorderbooks[0].add_bid(5, 20, 'trader-2')
    limitorderbooks[0].add_bid(7, 20, 'trader-3')
    limitorderbooks[0].add_bid(7, 20, 'trader-4')
    limitorderbooks[0].add_bid(7, 20, 'trader-5')
    # highest bid is 10
    assert_equal(limitorderbooks[0].bids[-1].price, 10)
    # lowest bid is 5
    assert_equal(limitorderbooks[0].bids[0].price, 5)
    # second highest bid trader = trader-2
    assert_equal(limitorderbooks[0].bids[-2].owner, 'trader-3')

def test_add_ask(limitorderbooks):
    limitorderbooks[0].add_ask(11, 20, 'trader-1')
    limitorderbooks[0].add_ask(5, 20, 'trader-2')
    limitorderbooks[0].add_ask(7, 20, 'trader-3')
    limitorderbooks[0].add_ask(7, 20, 'trader-4')
    limitorderbooks[0].add_ask(7, 20, 'trader-5')
    # highest ask is 11
    assert_equal(limitorderbooks[0].asks[-1].price, 11)
    # lowest ask is 5
    assert_equal(limitorderbooks[0].asks[0].price, 5)
    # second highest ask trader = trader-5
    assert_equal(limitorderbooks[0].asks[-2].owner, 'trader-5')

def test_clean_book(limitorderbooks, agents):
    limitorderbooks[0].add_bid(10, 20, agents[0])
    limitorderbooks[0].add_bid(5, 20, agents[1])
    limitorderbooks[0].add_ask(11, 20, agents[0])
    limitorderbooks[0].add_ask(5, 20, agents[1])
    for n in range(119):
        limitorderbooks[0].clean_book()
    assert_equal(len(limitorderbooks[0].bids), 2)
    assert_equal(len(limitorderbooks[0].asks), 2)
    limitorderbooks[0].clean_book()
    assert_equal(len(limitorderbooks[0].bids), 0)
    assert_equal(len(limitorderbooks[0].asks), 0)

def test_match_orders(limitorderbooks, agents):
    # add some asks
    limitorderbooks[0].add_ask(5, 20, agents[0])
    limitorderbooks[0].add_ask(7, 20, agents[1])
    limitorderbooks[0].add_ask(7, 20, agents[2])
    limitorderbooks[0].add_ask(7, 20, agents[3])
    # and bids
    limitorderbooks[0].add_bid(10, 20, agents[4])
    limitorderbooks[0].add_bid(4, 20, agents[5])
    limitorderbooks[0].add_bid(9, 20, agents[6])
    matched_orders = limitorderbooks[0].match_orders()
    # after an orderbook match both order books are reduced by 1
    assert_equal(len(limitorderbooks[0].bids), 2)
    assert_equal(len(limitorderbooks[0].asks), 3)
    # and the highest bid was matched to the lowest ask, difference is 5
    assert_equal(matched_orders[2].price - matched_orders[3].price, 5)
    # the second match is bid p9 and ask p7, difference is 2
    matched_orders = limitorderbooks[0].match_orders()
    assert_equal(matched_orders[2].price - matched_orders[3].price, 2)
    # Once again the order books are reduced by 1 in size
    assert_equal(len(limitorderbooks[0].bids), 1)
    assert_equal(len(limitorderbooks[0].asks), 2)
    # then no more match is possible
    matched_orders = limitorderbooks[0].match_orders()
    assert_equal(matched_orders, None)
    for n in range(500):
        limitorderbooks[0].clean_book()
    limitorderbooks[0].add_ask(5, 10, agents[7])
    limitorderbooks[0].add_ask(7, 8, agents[8])
    limitorderbooks[0].add_bid(10, 20, agents[9])
    # first match should reduce asks book by 1
    matched_orders = limitorderbooks[0].match_orders()
    assert_equal(len(limitorderbooks[0].bids), 1)
    assert_equal(len(limitorderbooks[0].asks), 1)
    assert_equal(matched_orders[2].price - matched_orders[3].price, 5)
    # the bid should have a remaining volume of 10
    assert_equal(limitorderbooks[0].bids[0].volume, 10)
    # second match
    matched_orders = limitorderbooks[0].match_orders()
    # should reduce the lenght of the asks book to zero and bids should remain 1
    assert_equal(len(limitorderbooks[0].bids), 1)
    assert_equal(len(limitorderbooks[0].asks), 0)
    # the bid should have a remaining volume of 2
    assert_equal(limitorderbooks[0].bids[0].volume, 2)
    # price should be 7 and volume 8
    assert_equal(matched_orders[0], 7)
    assert_equal(matched_orders[1], 8)
    # no more matches should be possible, leaving the order in the orderbook
    assert_equal(limitorderbooks[0].match_orders(), None)


def test_cleanse_book(limitorderbooks, agents):
    # add some asks
    limitorderbooks[0].add_ask(5, 20, agents[0])
    limitorderbooks[0].add_ask(7, 20, agents[1])
    limitorderbooks[0].add_ask(7, 20, agents[2])
    limitorderbooks[0].add_ask(7, 20, agents[3])
    # and bids
    limitorderbooks[0].add_bid(10, 20, agents[4])
    limitorderbooks[0].add_bid(4, 20, agents[5])
    limitorderbooks[0].add_bid(9, 20, agents[6])
    matched_orders = limitorderbooks[0].match_orders()
    # cleanse book
    transvolhist1 = limitorderbooks[0].transaction_volumes_history
    matched_orders_hist1 = limitorderbooks[0].matched_bids_history
    limitorderbooks[0].cleanse_book()
    transvolhist2 = limitorderbooks[0].transaction_volumes_history
    matched_orders_hist2 = limitorderbooks[0].matched_bids_history
    # test if volume history and matched orders history where updated
    assert_equal(len(transvolhist1) < len(transvolhist2), False)
    assert_equal(len(matched_orders_hist1) < len(matched_orders_hist2), False)


def test_update_bid_ask_spread(limitorderbooks, agents):
    """test if the bid_ask spread is correctly updated"""
    # first add lower ask
    lowest_ask1 = limitorderbooks[0].lowest_ask_price
    limitorderbooks[0].add_ask(98, 20, agents[0])
    lowest_ask2 = limitorderbooks[0].lowest_ask_price
    assert_equal(lowest_ask2 < lowest_ask1, True)
    # add higher bid and check if the highest bid is correctly updated
    highest_bid1 = limitorderbooks[0].highest_bid_price
    limitorderbooks[0].add_bid(102, 20, agents[1])
    highest_bid2 = limitorderbooks[0].highest_bid_price
    assert_equal(highest_bid2 > highest_bid1, True)
    # check if the correct error is thrown if anything other than bid or ask is used in the method
    assert_raises(ValueError, limitorderbooks[0].update_bid_ask_spread, 'something_else')
