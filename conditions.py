import pandas as pd

def detect_upper_limit(df):
    df = df.loc[df['등락률'] > 29]
    return df

def detect_lower_limit(df):
    df = df.loc[df['등락률'] < -29]
    return df

def detect_higher_stock(df):
    df = df.loc[df['등락률'] > 20]
    return df

def detect_lower_stock(df):
    df = df.loc[df['등락률'] < -20]
    return df

def market_fundamental(day):
    

