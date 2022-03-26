# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 18:59:31 2022

@author: PC
"""

import requests
import json
from requests.exceptions import RequestException
import time
import pandas as pd

headers = {
    'Host': 'api.fund.eastmoney.com',
    'Referer': 'http://fundf10.eastmoney.com/jjjz_161725.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

# 链接网页
def get_response(url,params):
    try:
        response = requests.get(url,params=params,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print('err: %s' % e)

#获取基金数据
def get_data(fundcode='161725'):
	t = time.time() 
	nowTime = lambda:int(round(t * 1000))
	params = {
		'callback': 'jQuery183015901735224567126_1549080604934',
		'fundCode': fundcode, #基金代码
		'pageIndex': '2',
		'pageSize': '0',
		'_': nowTime()
	}
	
	text = get_response('http://api.fund.eastmoney.com/f10/lsjz',params=params)
	res = text.replace('jQuery183015901735224567126_1549080604934(','')
	tar_str = res[:-1]
	get_json = json.loads(tar_str)
	return get_json

def fund_data(fundcode='161725'):
    data = pd.DataFrame(get_data(fundcode)['Data']['LSJZList'])
    data = data[['FSRQ','DWJZ','LJJZ','JZZZL','SGZT','SHZT','FHFCZ','FHFCBZ','FHSP']]
    data['FSRQ'] = data['FSRQ'].apply(pd.to_datetime)
    data[['DWJZ','LJJZ','JZZZL','FHFCZ']] = data[['DWJZ','LJJZ','JZZZL','FHFCZ']].apply(pd.to_numeric)
    return data
#data.columns = [['日期','单位净值','累计净值','日增长率','申购状态','赎回状态','分红系数','分红类别','分红送配']]


