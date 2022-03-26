# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 17:28:08 2022

@author: PC
"""

import streamlit as st
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

def get_response(url,params):
    try:
        response = requests.get(url,params=params,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print('err: %s' % e)



def main():
	t = time.time()
	nowTime = lambda:int(round(t * 1000))
	params = {
		'callback': 'jQuery183015901735224567126_1549080604934',
		'fundCode': '161725',
		'pageIndex': '2',
		'pageSize': '0',
		'_': nowTime()
	}
	
	text = get_response('http://api.fund.eastmoney.com/f10/lsjz',params=params)
	res = text.replace('jQuery183015901735224567126_1549080604934(','')
	tar_str = res[:-1]
	get_json = json.loads(tar_str)
	return get_json#print(get_json)

data = pd.DataFrame(main()['Data']['LSJZList'])
st.dataframe(data)
