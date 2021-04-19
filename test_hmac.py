import binascii
from hashlib import sha1

# Clone form
# https://github.com/micropython/micropython-lib/blob/master/base64/base64.py
# Importing the original base64 module would make error while importing
# the re module. So as a workaround, I take the b64encode() funciton along.def b64encode(s, altchars=None):

bytes_types = (bytes, bytearray)  # Types acceptable as binary data

def b64encode(s, altchars=None):
    """Encode a byte string using Base64.

    s is the byte string to encode.  Optional altchars must be a byte
    string of length 2 which specifies an alternative alphabet for the
    '+' and '/' characters.  This allows an application to
    e.g. generate url or filesystem safe Base64 strings.

    The encoded byte string is returned.
    """
    if not isinstance(s, bytes_types):
        raise TypeError("expected bytes, not %s" % s.__class__.__name__)
    # Strip off the trailing newline
    encoded = binascii.b2a_base64(s)[:-1]
    if altchars is not None:
        if not isinstance(altchars, bytes_types):
            raise TypeError("expected bytes, not %s"
                            % altchars.__class__.__name__)
        assert len(altchars) == 2, repr(altchars)
        return encoded.translate(bytes.maketrans(b'+/', altchars))
    return encoded

# Clone form
# https://learn.adafruit.com/circuitpython-totp-otp-2fa-authy-authenticator-friend/software
# The HMAC module in micropython-lib
# (https://github.com/micropython/micropython-lib/tree/master/hmac)
# isn't compatible with sha1 in the hashlib.
# As a workaround, I use the code sample for circuitpython.

def HMAC(k, m):
    SHA1_BLOCK_SIZE = 64
    KEY_BLOCK = k + (b'\0' * (SHA1_BLOCK_SIZE - len(k)))
    KEY_INNER = bytes((x ^ 0x36) for x in KEY_BLOCK)
    KEY_OUTER = bytes((x ^ 0x5C) for x in KEY_BLOCK)
    inner_message = KEY_INNER + m
    outer_message = KEY_OUTER + sha1(inner_message).digest()
    return sha1(outer_message)

import network
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('FLAG-SCHOOL', '12345678')

# usage sample
import ntptime
import time
gmt_time = time.localtime(
    ntptime.time()
)
print(gmt_time)

weekdays = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
months = (
    'Jan', 'Feb', 'Mar',
    'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Set',
    'Oct', 'Nov', 'Dec'
)
x_date = b'x-date: {}, {:02d} {} {:04d} {:02d}:{:02d}:{:02d} GMT'.format(
    weekdays[gmt_time[6]], # weekday
    gmt_time[2],           # date
    months[gmt_time[1] - 1],   # month
    gmt_time[0],           # year
    gmt_time[3],           # hour
    gmt_time[4],           # mineute
    gmt_time[5],           # seconds
)
print(x_date)

# dig = HMAC(
#     b'x6jAQAhLhknObLZPJuk9Dd1047w',
#     b'x-date: Mon, 19 Apr 2021 04:25:20 GMT')
dig = HMAC(
    b'x6jAQAhLhknObLZPJuk9Dd1047w', # key
    x_date
)
signature = b64encode(dig.digest()).decode()
print(signature)


import urequests

# 讓網站認為請求是使用瀏覽器發出。因為有些網頁會擋爬蟲程式
headers = {
    'user-agent':'curl/7.76.1',
    'Accept': 'application/json',
    'Authorization':'hmac username="1c0a99d7fb1b4001ac1685acabb10e00", algorithm="hmac-sha1", headers="x-date", signature="{}"'.format(signature),
    'x-date': x_date.decode()[7:]
}

# curl_cmd = "" + \
#            "curl -X GET " + \
#            "--header 'Accept: application/json' " + \
#            '--header \'Authorization: hmac username="1c0a99d7fb1b4001ac1685acabb10e00", algorithm="hmac-sha1", headers="x-date", signature="{}"\' '.format(signature) + \
#            "--header 'x-date: Mon, 19 Apr 2021 06:59:29 GMT' " + \
#            "'https://ptx.transportdata.tw/MOTC/v2/Rail/Operator?$top=1&$format=JSON'"
# print(curl_cmd)

# 查詢指定火車起點與終點
train_url = 'https://ptx.transportdata.tw/MOTC/v2/Rail/Operator?$top=1&$format=JSON'
train_res = urequests.get(train_url, headers=headers)
print(train_res.text)





