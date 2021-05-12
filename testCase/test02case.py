import datetime
import json
import unittest

import requests

import readConfig
from common.configHttp import RunMain
import paramunittest
import geturlParams
import urllib.parse
# import pythoncom
import readExcel
import writeexcel

# pythoncom.CoInitialize()

url = geturlParams.geturlParams().get_Url()  # 调用我们的geturlParams获取我们拼接的URL
login_xls = readExcel.readExcel().get_xls('userCase.xlsx', 'login')
read_conf = readConfig.ReadConfig()
write = writeexcel.WriteExcel()


@paramunittest.parametrized(*login_xls)
class testAPI_shuikong(unittest.TestCase):

    def setParameters(self, case_name, path, query, method, exception, result, msg):
        """
        set params
        :param case_name:
        :param path
        :param query
        :param method
        :return:
        """
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = str(query)
        self.method = str(method)
        self.exception = str(exception)

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

        # def setUp(self):
        """

        :return:
        """

    #   print(self.case_name + "测试开始前准备")

    def test02case(self):
        self.checkResult()

    # def tearDown(self):
    #   print("测试结束，输出log完结\n\n")

    def checkResult(self):  # 断言
        """
        check test result
        :return:
        """
        # url1 = "http://zhumadian.tomsung.cn:9888/tcmgs/main/log"
        # new_url = url1 + self.query
        # data1 = dict(urllib.parse.parse_qsl(
        # urllib.parse.urlsplit(new_url).query))  # 将一个完整的URL中的name=&pwd=转换为{'name':'xxx','pwd':'bbb'}
        url = "http://tcmgs.tomsung.cn/tcmgs/main/login?phone=18049441262&password=654321"
        Headers = {'Content-Type': 'application/json;charset=UTF-8'}
        response = requests.post(url, headers=Headers)
        headers = {
            "token": response.json()['content']['token']
        }
        headers = json.dumps(headers)
        url = geturlParams.geturlParams().get_Url() + self.path
        info = RunMain().run_main(self.method, url, self.query,
                                  headers)  # 根据Excel中的method调用run_main来进行requests请求，并拿到响应
        ss = json.loads(info)  # 将响应转换为字典格式
        print("参数为：", self.query)

        print("提示： ", ss['message'])
        case_name = self.case_name.split("/")[0]
        today = datetime.date.today()
        now = int(today.strftime('%d')) - 1
        month = int(today.strftime('%m')) - 1
        if case_name == 'gun_oil':
            list = ss['content']['pageInfo']['list']
            print(list)
            if not list:
                value = 'fail'
                # print(value)
                write.write_data(self.case_name, 'list为空', value)
            else:
                value = 'pass'
            self.assertTrue(ss['content']['pageInfo']['list'], msg='list为空')
            # print(value)
            write.write_data(self.case_name, ss['message'], value)
        elif case_name == 'export_total':
            if ss['code'] == 1000 and ss['content']['oilAll'] > 130000:
                value = 'pass'
                write.write_data(self.case_name, ss['message'], value)
            else:
                value = 'fail'
                write.write_data(self.case_name, '月汇总异常', value)
            self.assertNotEqual(ss['content']['oilAll'], 0)
            self.assertTrue(ss['content']['exportStationVo']['list'], msg='list为空')
        elif case_name == 'oil_volume_day':
            list = ss['content'].__len__()
            if list == now:
                value = 'pass'
                write.write_data(self.case_name, ss['message'], value)
            else:
                value = 'fail'
                write.write_data(self.case_name, '日汇总异常', value)
            self.assertEqual(list, now, msg='日汇总异常')
        elif case_name == 'oil_volume_month':
            list = ss['content'][month]
            if list:
                value = 'pass'
                write.write_data(self.case_name, ss['message'], value)
            else:
                value = 'fail'
                write.write_data(self.case_name, '月汇总异常', value)
            self.assertTrue(list, msg='月汇总异常')
        else:
            if self.exception == ss['message']:
                value = 'pass'
                write.write_data(self.case_name, ss['message'], value)

            if self.exception != ss['message']:
                value = 'fail'
                write.write_data(self.case_name, str(ss), value)

            self.assertEqual(ss['message'], self.exception)
        '''
        # 登录
 
        if self.case_name == 'login':  # 如果case_name是login，说明合法，返回的code应该为200
            self.assertEqual(ss['code'], 1000)
            value = self.get_value(ss['message'])
            write.write_data(self.case_name, ss['message'], value)
        # 首页地图
        if self.case_name == 'map':  # 如果case_name是login，说明合法，返回的code应该为200
            self.assertEqual(ss['code'], 1000)
            value = self.get_value(ss['message'])
            write.write_data(self.case_name, ss['message'], value)
        # 注销
        if self.case_name == 'quit':  # 如果case_name是login，说明合法，返回的code应该为200
            self.assertEqual(ss['code'], 1000)
            value = self.get_value(ss['message'])
            write.write_data(self.case_name, ss['message'], value)
        # 获取加油的实时数据作为冒泡
        if self.case_name == 'maopao':  # 如果case_name是login，说明合法，返回的code应该为200
            self.assertEqual(ss['code'], 1000)
            value = self.get_value(ss['message'])
            write.write_data(self.case_name, ss['message'], value)

        # 加油机列表

        # 有告警的加油站下拉列表
        # 首页测试
        # 加油站下拉列表
        # 首页获得油站排名
        if self.case_name == 'getstation_all_1':
            self.assertEqual(ss['code'], 1000)
            value = self.get_value(ss['message'])
            write.write_data(self.case_name, ss['message'], value)
        if self.case_name == 'getstation_#0_1':
            self.assertEqual(ss['code'], 1000)
            value = self.get_value(ss['message'])
            write.write_data(self.case_name, ss['message'], value)
        if self.case_name == 'getstation_#92_1':
            self.assertEqual(ss['code'], 1000)
        if self.case_name == 'getstation_#98_1':
            self.assertEqual(ss['code'], 1000)
        if self.case_name == 'getstation_all_2':
            self.assertEqual(ss['code'], 1000)
        if self.case_name == 'getstation_#0_2':
            self.assertEqual(ss['code'], 1000)
        if self.case_name == 'getstation_#92_2':
            self.assertEqual(ss['code'], 1000)
        if self.case_name == 'getstation_#98_2':
            self.assertEqual(ss['code'], 1000)
        if self.case_name == 'getstation_all_0':
            self.assertEqual(ss['code'], 1000)
        if self.case_name == 'getstation_#0_0':
            self.assertEqual(ss['code'], 1000)
        if self.case_name == 'getstation_#92_0':
            self.assertEqual(ss['code'], 1000)
        if self.case_name == 'getstation_#98_0':
            self.assertEqual(ss['code'], 1000)
        if self.case_name == 'getstation_null':
            self.assertEqual(ss['code'], 2000, )

        if self.case_name == 'getstation_error':
            self.assertEqual(ss['code'], 2002, )
            value = self.get_value(ss['message'])
            write.write_data(self.case_name, ss['message'], value)
        # 首页获得油罐、加油机的报警数和总数
        if self.case_name == 'deviceLeverSum':
            self.assertEqual(ss['code'], 1000)
            value = self.get_value(ss['message'])
            write.write_data(self.case_name, ss['message'], value)
        # 首页获得告警、预警信息列表
        if self.case_name == 'alarmList':
            self.assertEqual(ss['code'], 1000)
            value = self.get_value(ss['message'])
            write.write_data(self.case_name, ss['message'], value)
        # 首页获得油站信息列表
        if self.case_name == 'stationList':
            self.assertEqual(ss['code'], 1000)
            value = self.get_value(ss['message'])
            write.write_data(self.case_name, ss['message'], value)
        if self.case_name == 'stationList_error':
            self.assertEqual(ss['code'], 2000)
            value = self.get_value(ss['message'])
            write.write_data(self.case_name, ss['message'], value)
        # 当前用户下的所有加油站加油总量（今日或者昨日
        # 首页各油号今日加油总数
        if self.case_name == 'oilListOfType':
            self.assertEqual(ss['code'], 1000)
            value = self.get_value(ss['message'])
            write.write_data(self.case_name, ss['message'], value)
        # 实时数据
        if self.case_name == 'gun_oil':
            self.assertTrue(ss['content']['pageInfo']['list'], msg='list为空')
            value = self.get_value(ss['message'])
            write.write_data(self.case_name, ss['message'], value)
        # 进油信息
        if self.case_name == 'oilin':
            self.assertEqual(ss['code'], 1000)
            value = self.get_value(ss['message'])
            write.write_data(self.case_name, ss['message'], value)
        # 油枪信息
        if self.case_name == 'oil_gun':
            self.assertEqual(ss['code'], 1000)
            value = self.get_value(ss['message'])
            write.write_data(self.case_name, ss['message'], value)
      '''


if __name__ == '__main__':
    unittest.main()
