import numpy as np
import pandas as pd

# -----------------------------------------------------
# Pattern Generator Module
# -----------------------------------------------------
# Generates clean candle data for training visuals.
# Each pattern returns a pandas DataFrame with OHLC data.
# -----------------------------------------------------

def generate_doji():
    open_price = 100
    close_price = open_price + np.random.uniform(-0.2, 0.2)
    high = open_price + np.random.uniform(0.5, 1.5)
    low = open_price - np.random.uniform(0.5, 1.5)
    return _create_df(open_price, high, low, close_price)


def generate_hammer():
    open_price = 100
    close_price = open_price + np.random.uniform(0.5, 1.0)
    low = open_price - np.random.uniform(2.0, 3.0)
    high = close_price + np.random.uniform(0.2, 0.5)
    return _create_df(open_price, high, low, close_price)


def generate_shooting_star():
    open_price = 100
    close_price = open_price - np.random.uniform(0.5, 1.0)
    high = open_price + np.random.uniform(2.0, 3.0)
    low = close_price - np.random.uniform(0.2, 0.5)
    return _create_df(open_price, high, low, close_price)


def generate_bullish_engulfing():
    o1 = 100
    c1 = o1 - np.random.uniform(1.0, 2.0)
    h1 = max(o1, c1) + np.random.uniform(0.2, 0.5)
    l1 = min(o1, c1) - np.random.uniform(0.2, 0.5)

    o2 = c1 - np.random.uniform(0.5, 1.0)
    c2 = o1 + np.random.uniform(1.0, 2.0)
    h2 = max(o2, c2) + np.random.uniform(0.2, 0.5)
    l2 = min(o2, c2) - np.random.uniform(0.2, 0.5)

    data = [
        [o1, h1, l1, c1],
        [o2, h2, l2, c2]
    ]
    return _df_multi(data)


def generate_bearish_engulfing():
    o1 = 100
    c1 = o1 + np.random.uniform(1.0, 2.0)
    h1 = max(o1, c1) + np.random.uniform(0.2, 0.5)
    l1 = min(o1, c1) - np.random.uniform(0.2, 0.5)

    o2 = c1 + np.random.uniform(0.5, 1.0)
    c2 = o1 - np.random.uniform(1.0, 2.0)
    h2 = max(o2, c2) + np.random.uniform(0.2, 0.5)
    l2 = min(o2, c2) - np.random.uniform(0.2, 0.5)

    data = [
        [o1, h1, l1, c1],
        [o2, h2, l2, c2]
    ]
    return _df_multi(data)


# -----------------------------------------------------
# Helper Functions
# -----------------------------------------------------

def _create_df(open_price, high, low, close_price):
    return pd.DataFrame({
        "open": [open_price],
        "high": [high],
        "low": [low],
        "close": [close_price]
    })


def _df_multi(data_list):
    o, h, l, c = [], [], [], []
    for row in data_list:
        o.append(row[0])
        h.append(row[1])
        l.append(row[2])
        c.append(row[3])

    return pd.DataFrame({
        "open": o,
        "high": h,
        "low": l,
        "close": c
    })


# -----------------------------------------------------
# Pattern Selector
# -----------------------------------------------------

def get_pattern(name):
    patterns = {
        "Doji": generate_doji,
        "Hammer": generate_hammer,
        "Shooting Star": generate_shooting_star,
        "Bullish Engulfing": generate_bullish_engulfing,
        "Bearish Engulfing": generate_bearish_engulfing,
    }
    return patterns[name]()
