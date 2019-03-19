# -*- coding: utf-8 -*-

import requests

username = "915113590117"
password = "915113590117"


url_code = "http://202.119.81.113:8080/verifycode.servlet"
url_login = "http://202.119.81.113:8080/Logon.do?method=logon"

valcode = requests.get(url_code)
with open('valcode.png', 'wb') as f:
    f.write(valcode.content)

code = input('请输入验证码：')

userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
header = {
    # "origin": "https://passport.mafengwo.cn",
    "Referer": "http://202.119.81.113:8080/Logon.do?method=logon",
    'User-Agent': userAgent,
}

print("开始模拟登录njust")

postUrl = "http://202.119.81.113:8080/Logon.do?method=logon"
postData = {
    "USERNAME": username,
    "PASSWORD": password,
    "useDogCode": None,
    "RANDOMCODE": code,
}
resp = requests.post(postUrl, headers=header, cookies=requests.utils.dict_from_cookiejar(valcode.cookies),
                     data=postData)

# 无论是否登录成功，状态码一般都是 statusCode = 200
print(f"statusCode = {resp.status_code}")
with open("response.html", 'w') as f:
    f.write(resp.text)

