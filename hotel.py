from DrissionPage import ChromiumPage, ChromiumOptions
import csv

path = r'/opt/microsoft/msedge/microsoft-edge'
ChromiumOptions().set_browser_path(path).save()

f = open('date.csv', mode='w', newline='')
csv_writer = csv.DictWriter(f, fieldnames=['name', 'price', 'location'])

dp = ChromiumPage()
dp.listen.start('json/HotelSearch')
dp.get('https://hotels.ctrip.com/hotels/list?countryId=1&city=1&provinceId=0&checkin=2024/08/22&checkout=2024/08/23&optionId=1&optionType=City&directSearch=0&display=%E5%8C%97%E4%BA%AC&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1&')


page = 0
while(True):
    page += 1
    print(f"page{page}")
    next_btn = dp.ele('css:.btn-box span')
    if next_btn and next_btn.text == '搜索更多酒店':
        next_btn.click()

    resp = dp.listen.wait()
    json_data = resp.response.body
    hotelList = json_data['Response']['hotelList']['list']

    for index in hotelList:
        dit = {
            'name': index['base']['hotelName'],
            'price': index['money']['priceAndTax'],
            'location': index['position']['area'] + index['position']['address']
        }
        csv_writer.writerow(dit)

    dp.scroll.to_bottom()