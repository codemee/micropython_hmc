# 源由

由於要使用 [MOTC Transport API V2](https://ptx.transportdata.tw/MOTC?t=Rail&v=2#) 查詢鐵路資訊, 但此平台 API 需要使用 API id、API key 認證, 而且不是單純傳送 API key 認證, 而是需要使用 base64 以及 hmac+sha1 將 API key 與目前時間做出電子簽章, 而且此電子簽章只有 5 分鐘有效, 所以必須在 MicroPython 程式中即時產生電子簽章。

# 問題

在 [micropython-lib](https://github.com/micropython/micropython-lib) 中雖然有提供 [hmac](https://github.com/micropython/micropython-lib/tree/master/hmac) 模組, 不過這個模組需要搭配 [micropython-lib 的 hashlib](https://github.com/micropython/micropython-lib/tree/master/hashlib) 使用, 但是這個版本的 hashlib 並不提供 sha1, 而原本 MicroPython 內建的 uhashlib 的 sha1 確認 hmac 模組不相容, 所以無法直接使用。

另外, 使用 upip 安裝 [micropython-lib 的 base64](https://github.com/micropython/micropython-lib/tree/master/base64) 會連帶安裝依賴的 [micropython-lib 的 re 模組](https://github.com/micropython/micropython-lib/tree/master/re-pcre), 這個模組在 import 時會出錯, 所以也不能直接使用 base64 模組。

# 解法

還好在網路上有善心人士實作了 CircuitPython 版本的 [hmac+sha1 程式]( https://learn.adafruit.com/circuitpython-totp-otp-2fa-authy-authenticator-friend/software), 由於是純 Python 實作, 不依賴特定模組, 所以就可以借過來使用。

另外, import re 模組主要是在 decode base64 上, 如果只是要用 base64 編碼, 並不涉及 re 模組, 因此我們也可以從 base64 模組中單獨搬出 b64encode 函式來用, 這樣就解決了以上的問題了。
