import csv
from DrissionPage import ChromiumPage, ChromiumOptions
import time
import requests

attr_dict = dict([])
plan_lines = []


set_up_file = open("set-up.txt", mode='r')
set_up_info = set_up_file.read()
info = set_up_info.split('\n')
path = info[0]
confirm_num = info[1]
set_up_file.close()

ChromiumOptions().set_browser_path(path).save()
dp = ChromiumPage()

if confirm_num == 0:
    confirm = input("if you have set all websites, input \'finished\' here:\n")
    if not confirm == "finished":
        exit()

key = '597313b6dd968254c3575f075ca7f72d'


def SearchHotel(calculate_cnt = 1,
                check_date = ['2024', '09', '37', '2024', '10', '12'],
                lowest_price = '191',
                highest_price = '232',
                location_search = "兴隆山"
                ):
    
    
    init_url_p1 = f'https://hotels.ctrip.com/hotels/list?countryId=1&city=1&provinceId=0&'
    init_url_p2 = f'checkin={check_date[0]}/{check_date[1]}/{check_date[2]}&checkout={check_date[3]}/{check_date[4]}/{check_date[5]}'
    init_url = init_url_p1 + init_url_p2

    dp.get(init_url)

    # search
    search_text = dp.ele('#hotels-destination')
    search_text.clear()
    search_text.input(location_search)
    time.sleep(3)

    searchBtn = dp.ele('@class=search-btn-wrap')
    searchBtn.click()
    time.sleep(2)

    # input price
    lowest_price_input = dp.ele('@class=price-range-input-low')
    lowest_price_input.clear()
    lowest_price_input.input(lowest_price)

    # rank by distance
    distance_button = dp.ele('@aria-label=距离（由近到远）')
    distance_button.click()
    time.sleep(2)

    # output price - last input
    highest_price_input = dp.ele('@class=price-range-input-high')
    highest_price_input.clear()
    highest_price_input.input(highest_price)
    time.sleep(4)

    # output hotels
    prices = dp.eles('@class=real-price font-bold').get.texts()
    night_cnt = dp.eles('@class=nights').get.texts()
    # distances = dp.eles('@class=transport').get.texts()

    total_price = 0

    for i in range(calculate_cnt):
        total_price += float(prices[i][1:])

    return (total_price / calculate_cnt) * int(night_cnt[0][0:-1])


def CodeAddress(address, city):
    params = {'key': key, 'address': address, 'city': city}
    response = requests.get("https://restapi.amap.com/v3/geocode/geo", params=params)
    resp_json = response.json()
    location = resp_json['geocodes'][0]['location']
    return location


def SearchTaxi(pick_up, drop_off, city):
    location_pick_up = CodeAddress(pick_up, city)
    location_drop_off = CodeAddress(drop_off, city)
    params = {'key': key, 'origin': location_pick_up, 'destination': location_drop_off, 'extensions': 'all'}

    response = requests.get("https://restapi.amap.com/v3/direction/driving", params=params)
    resp_json = response.json()
    price = resp_json['route']['taxi_cost']
    return float(price)


def InputData():
    global plan_lines
    plan_file = open('plan.csv', mode = 'r')
    attraction_file = open('attractions.csv', mode = 'r')
    plan_lines = list(csv.reader(plan_file))
    attr_lines = csv.reader(attraction_file)

    for line in attr_lines:
        attr_dict[line[0]] = float(line[1])

    plan_file.close()
    attraction_file.close()


def Calculate(line, head_cnt = 1):
    if line[0] == '1':
        price_per_person = attr_dict[line[3]]
        line.insert(0, price_per_person * head_cnt)
    if line[0] == '2':
        price_item = SearchHotel(5, line[4:10], line[11], line[12]+'\n', line[3])
        line.insert(0, price_item * int(line[10]))
    if line[0] == '3':
        price_per_person = float(line[4])
        line.insert(0, price_per_person * head_cnt)
    if line[0] == '4':
        price_item = SearchTaxi(line[4], line[5], line[3])
        line.insert(0, price_item * int(line[6]))


def main():
    InputData()
    assert(plan_lines[0][0] == '0')
    head_cnt = int(plan_lines[0][1])
    total_price = 0
    idx_line = 0

    quote_file = open('quote.csv', mode = 'w')
    quote_writer = csv.writer(quote_file)

    for line in plan_lines[1:]:
        idx_line += 1
        print(f"\ncalculating line {idx_line}")
        Calculate(line, head_cnt)
        quote_writer.writerow(line)
        total_price += line[0]
    
    quote_writer.writerow([total_price])
    quote_file.close()


if __name__ == "__main__":
    main()