import time
import pyupbit
import datetime
import json 

with open('keys.json','r') as f:
    keys = json.load(f)

kst_timezone = datetime.timezone(datetime.timedelta(hours=9), 'KST')
access = keys['accessKey']         # 본인 값으로 변경
secret = keys['secretKey']



cryptoType = "ATOM"
cryptoRelation = "KRW-"+cryptoType
kValue = 0.5



def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        
        start_time = get_start_time(cryptoRelation)
        end_time = start_time + datetime.timedelta(days=1)
        print('start time:', start_time)
        print('now :', now)
        print(end_time - datetime.timedelta(seconds=10))

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price(cryptoRelation, 0.5)
            current_price = get_current_price(cryptoRelation)
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    print(krw)
                    upbit.buy_market_order(cryptoRelation, krw*0.9995)
        else:
            cryptoBalance = get_balance(cryptoType)
            if cryptoBalance > (5000/get_current_price(cryptoRelation)):
                print(krw)
                upbit.sell_market_order(cryptoRelation, cryptoBalance)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
