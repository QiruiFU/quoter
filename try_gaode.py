import requests

key = '597313b6dd968254c3575f075ca7f72d'
address = '新街口'
city = '南京'

location_pick_up = '116.481028,39.989643'
location_drop_off = '116.434446,39.90816'
params = {'key': key, 'origin': location_pick_up, 'destination': location_drop_off, 'extensions': 'all'}
response = requests.get("https://restapi.amap.com/v3/direction/driving", params=params)
resp_json = response.json()
price = resp_json['route']['taxi_cost']
print(price)
