import flag_utils
import network
import ntptime
import time

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('FLAG-SCHOOL', '12345678')
while not sta.isconnected():
    pass

gmt_time = time.localtime(
    ntptime.time()   # get network time 
)

x_date = flag_utils.to_x_date(gmt_time)
print(x_date)

# dig = HMAC(
#     b'x6jAQAhLhknObLZPJuk9Dd1047w',
#     b'x-date: Mon, 19 Apr 2021 04:25:20 GMT')
dig = flag_utils.HMAC_sha1(
    b'x6jAQAhLhknObLZPJuk9Dd1047w', # key
    x_date
)
signature = flag_utils.b64encode(dig.digest()).decode()
print(signature)


import urequests

# 讓網站認為請求是使用瀏覽器發出。因為有些網頁會擋爬蟲程式
headers = {
    'user-agent':'curl/7.76.1',
    'Accept': 'application/json',
    'Authorization':'hmac username="1c0a99d7fb1b4001ac1685acabb10e00", algorithm="hmac-sha1", headers="x-date", signature="{}"'.format(signature),
    'x-date': x_date.decode()[7:]
}

# 查詢指定火車起點與終點
train_url = 'https://ptx.transportdata.tw/MOTC/v2/Rail/Operator?$top=1&$format=JSON'
train_res = urequests.get(train_url, headers=headers)
print(train_res.text)
