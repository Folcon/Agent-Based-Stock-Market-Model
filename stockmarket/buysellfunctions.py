"""In this file, we define buy / sell / hold functions of the agents"""

import numpy as np


# def mean_reversion(prices, shortMA, longMA, upper_threshold, lower_threshold):
#     """Buy or sell against the trend"""
#     prices = prices[(len(prices)-shortMA):]
#     t = np.array(range(len(prices)))
#     A = np.vstack([t, np.ones(len(t))]).T
#     # estimate linear regression
#     m, c = np.linalg.lstsq(A, prices)[0]
#     trend = m*t + c
#     if trend[-1] / prices[-1] > upper_threshold:
#         return 'buy'
#     elif trend[-1] / prices[-1] < lower_threshold:
#         return 'sell'
#     else:
#         return 'hold'

def mean_reversion(prices, shortMA, longMA, upper_threshold, lower_threshold):
    """Buy or sell against the trend"""
    shortMA = int(shortMA)
    longMA = int(longMA)
    short_ma = sum(prices[len(prices) - shortMA:]) / shortMA
    long_ma = sum(prices[len(prices) - longMA:]) / longMA
    momentum = short_ma / long_ma
    if momentum > upper_threshold:
        return 'sell'
    elif momentum < lower_threshold:
        return 'buy'
    else:
        return 'hold'


def momentum(prices, shortMA, longMA, upper_threshold, lower_threshold):
    """If momentum is positive, buy, if momentum is negative, sell, otherwise hold"""
    short_ma = sum(prices[len(prices)-shortMA:]) / shortMA
    long_ma = sum(prices[len(prices)-longMA:]) / longMA
    momentum = short_ma / long_ma
    if momentum > upper_threshold:
        return 'buy'
    elif momentum < lower_threshold:
        return 'sell'
    else:
        return 'hold'

def noise_trading(prices, shortMA, longMA, upper_threshold, lower_threshold):
    """buy / sell at random"""
    probability_to_buy = np.random.randint(0, 100)
    probability_to_buy = probability_to_buy / 100

    return np.random.choice(['buy', 'sell'], p=[probability_to_buy, (1-probability_to_buy)])
