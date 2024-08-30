from DrissionPage import ChromiumPage, ChromiumOptions
import csv
import time

path = r'/opt/microsoft/msedge/microsoft-edge'
ChromiumOptions().set_browser_path(path).save()

check_in_year = '2024'
check_in_month = '09'
check_in_day = '27'
check_out_year = '2024'
check_out_month = '10'
check_out_day = '12'
room_cnt = '02'
# adult_cnt = '04'
# children_cnt = '01'
location_search = "兴隆山"

lowest_price = "199"
highest_price = "232\n"

dp = ChromiumPage()
init_url_p1 = f'https://hotels.ctrip.com/hotels/list?countryId=1&city=1&provinceId=0&'
init_url_p2 = f'checkin={check_in_year}/{check_in_month}/{check_in_day}&checkout={check_out_year}/{check_out_month}/{check_out_day}'
init_url_p3 = f'&crn={room_cnt}'
# init_url_p3 = f'&crn={room_cnt}&adult={adult_cnt}&children={children_cnt}'
init_url = init_url_p1 + init_url_p2 + init_url_p3

dp.get(init_url)

# search
search_text = dp.ele('#hotels-destination')
search_text.clear()
search_text.input(location_search)
time.sleep(2)

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

# output first 20 hotels
prices = dp.eles('@class=real-price font-bold').get.texts()
distances = dp.eles('@class=transport').get.texts()

print(distances)
print(prices)

total_price = 0
calculate_cnt = 5

for i in range(calculate_cnt):
    total_price += int(prices[i][1:])

print(total_price / calculate_cnt)