
import base64
import datetime
import hashlib
import hmac
import json
import time
import urllib.parse
import mysql.connector
import requests
import schedule
from datetime import datetime



# 1、此处填上Webhook链接和密钥
webhook = "https://oapi.dingtalk.com/robot/send?access_token=b362a6fc2f7e1fbc84d885f8968872fbd004cf783e212e18b6675b59c7664282"
secret = "SECba0e803e323e231493446e8c909c4c95dfe1f2767c34b3731b64fd44c3b9b2e0"


# 2、验证密钥（无需改动，直接照搬，返回url）
def sign():
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    print("sign值：" + sign)
    url = webhook + '&timestamp=' + timestamp + '&sign=' + sign
    return url


# 3、拿到上一步的URL，就可以发送消息了，根据需要选择信息样式
def ding_message(data):
    url = sign()
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    #     markdown样式
    message = {
        "msgtype": "markdown",
        "markdown": {
            "title": "每日一报",  # 窗口标题
            "text": data,
        },
        "at": {
            "atMobiles": [],
            "atUserIds": [],
            "isAtAll": False
        }
    }
    proxies = {
        'http': '127.0.0.1:38888',
        'https': '127.0.0.1:38888'
    }
    message_json = json.dumps(message)
    send_message = requests.post(url=url, data=message_json, headers=header)
    print(send_message.text)


def my_func():
    today = datetime.now().day
    number = int(today)+4
    print(number)
    mydb = mysql.connector.connect(
        host="pla123456.rwlb.rds.aliyuncs.com",
        user="user",
        password="u2fSu2fS",
        database="epubdatabase",
    )

    mycursor = mydb.cursor()
    # 查询所有的数据字段,使用占位符％s方法来转义查询值：
    sql = "SELECT text FROM markdown_table where id=%s"

    addr = (number,)
    mycursor.execute(sql, addr)
    myresult = mycursor.fetchall()

    for x in myresult:
        #     # 拆分元组中的字符串，组成正常的发送格式
        strings = [string.strip() for string in x[0].split('\n')]
        strings = [string.strip() for string in x[0].split('\\n')]
        print('\n\n'.join(strings))
        sql_result = '\n\n'.join(strings)
        ding_message(sql_result)

    now = datetime.now()
    print("推送成功:", now)
    print("--------------------------------------------------------------------------------------------")


# my_func(9)
# 每天12:00执行my_function()函数
# schedule.every().day.at("14:33:53").do(my_func, 3)
# 每分钟执行一次
# my_func()
schedule.every().day.at("14:00:30").do(my_func)

while True:
    schedule.run_pending()
    time.sleep(1)
    # 让程序暂停一段时间，以确保任务有足够时间执行完毕
