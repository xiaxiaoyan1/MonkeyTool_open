import requests
import tkinter as tk
from tkinter import messagebox
import json

def send_dingtalk_msg(connect):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=a3f6978071326e6f9c3ba25727922d39848934284bc0db5d19ae19821ae07151'
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    post_data = {
        "msgtype": "text",
        "text": {
            "content": "%s" % (connect)
            #"content":"测试"
        },
        "at": {
            "atUserIds": ["10093530"],
        }
    }
    r = requests.post(url, headers=headers, data=json.dumps(post_data))
    #print(r.content)

# if __name__ == '__main__':
#     connect="monkey本次运行结果："+"\n"+"ANR错误数:%d"%10+"\n"+"CRASH错误数:%d"%5+"\n"+"GC错误数:%d"%0+"\n"+"Exception错误数:%d"%25
#     send_dingtalk_msg(connect)

