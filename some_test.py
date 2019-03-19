

import pytesseract
import cv2
import requests
from time import sleep

path = "valcode.png"
username = "91511359017"
password = "91511359011"


def recognizer():
    img = cv2.imread(path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = pytesseract.image_to_string(img_gray)
    print("before:", result, end=" ")
    result = "".join([c for c in result if c.isalnum()])
    print("after:", result, end=" ")
    if len(result) == 4:
        return result
    else:
        return False



session = requests.session()

url_code = "http://202.119.81.113:8080/verifycode.servlet"

image = session.get(url_code, stream=True)

with open(path, 'wb') as f:
    f.write(image.content)

code = input("输入code")

userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
header = {
    "Referer": "http://202.119.81.113:8080/Logon.do?method=logon",
    'User-Agent': userAgent,
}

responseRes = session.post(
    f"http://202.119.81.113:8080/Logon.do?method=logon&USERNAME={username}&PASSWORD={password}&useDogCode=&RANDOMCODE={code}",
    headers=header)

# 无论是否登录成功，状态码一般都是 statusCode = 200
print(f"statusCode = {responseRes.status_code}", end=" ")

with open("response.html", 'w') as f:
    f.write(responseRes.text)


if "我的课表" in responseRes.text:
    print("成功")
else:
    print("失败")
