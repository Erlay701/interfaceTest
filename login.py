#!/usr/bin/env python
# coding:utf-8
import requests, json
import datetime
from common.configHttp import RunMain

url = "http://39.100.77.117:7021/tcmgs/main/login?phone=18991212345&password=654321"
Headers = {'Content-Type': 'application/json;charset=UTF-8'}
response = requests.post(url, headers=Headers)
print(response.text)
token = response.json()['content']['token']
headers = {
    'token': token
}
headers = json.dumps(headers)
print(headers)
'''
url0 = "http://tcmgs.tomsung.cn/tcmgs/data/gun_oil"
headers = {"token": "51d0f1b0-a65c-4138-96a5-e5370f692662"}
data = {"pageNum": "1", "pageSize": "10", "beginTime": "2021-04-06 00:00:00", "endTime": "2021-05-06 23:59:59",
        "oilFlow": "5"}
response = requests.post(url=url0, headers=headers, data=data)
print(response.text)
list = response.json()['content']['pageInfo']['list']
print(list)

red = xlwt.XFStyle()
font1 = xlwt.Font()
font1.name = '宋体'
font1.bold = True
font1.height = 220
font1.colour_index = 2
alignment = xlwt.Alignment()
alignment.horz = 2
alignment.vert = 1
alignment.wrap = 1
red.font = font1
red.alignment = alignment'''

today = datetime.date.today()
now = today.strftime('%d')
month = int(today.strftime('%m'))-1
print(now)
print(month)
ss ={"code":1000,"message":"成功","content":[{"value":1728579.97,"time":"2020-12-01"},{"value":1413792.59,"time":"2021-01-01"},{"value":1302057.05,"time":"2021-02-01"},{"value":1834715.12,"time":"2021-03-01"}]}
print(ss['content'][3])