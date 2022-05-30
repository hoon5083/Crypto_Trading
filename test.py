import pyupbit
import json 
with open('keys.json','r') as f:
    keys = json.load(f)

access = keys['accessKey']         # 본인 값으로 변경
secret = keys['secretKey']
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-BTC"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회