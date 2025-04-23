import csv
import json
import traceback

import requests


def get_info_ls():
    cookies = {
        'AlteonP10': 'BoXdBSw/F6xRpQhUHD69Tw$$',
        'apache': '4a63b086221745dd13be58c2f7de0338',
        'ags': '2a1ba4d47b619c011c19c1cc4b3c0c32',
        'lss': 'f7cb2cf4b1607aec30e411e90d47c685',
        'isLogin': '0',
        '_ulta_id.CM-Prod.e9dc': '2715ffb761fc82b5',
        '_ulta_ses.CM-Prod.e9dc': '258f6b218c1bda8b',
        '_ulta_id.ECM-Prod.e9dc': 'eb5fcd1cb6c63c38',
        '_ulta_ses.ECM-Prod.e9dc': '1e18064e6f1b942e',
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.chinamoney.com.cn',
        'Referer': 'https://www.chinamoney.com.cn/english/bdInfo/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'AlteonP10=BoXdBSw/F6xRpQhUHD69Tw$$; apache=4a63b086221745dd13be58c2f7de0338; ags=2a1ba4d47b619c011c19c1cc4b3c0c32; lss=f7cb2cf4b1607aec30e411e90d47c685; isLogin=0; _ulta_id.CM-Prod.e9dc=2715ffb761fc82b5; _ulta_ses.CM-Prod.e9dc=258f6b218c1bda8b; _ulta_id.ECM-Prod.e9dc=eb5fcd1cb6c63c38; _ulta_ses.ECM-Prod.e9dc=1e18064e6f1b942e',
    }
    for i in range(8):
        page = i
        data = {
            'pageNo': f'{page}',
            'pageSize': '15',
            'isin': '',
            'bondCode': '',
            'issueEnty': '',
            'bondType': '100001',
            'couponType': '',
            'issueYear': '2023',
            'rtngShrt': '',
            'bondSpclPrjctVrty': '',
        }
        response = requests.post(
            'https://www.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN',
            cookies=cookies,
            headers=headers,
            data=data,
        )

        res = json.loads(response.text)['data']['resultList']
        yield res

def process_data():git
    res_ls = get_info_ls()
    for infos in res_ls:
        for info in infos:
            write_to_csv(info)


def write_to_csv(info):
    info_file = 'res.csv'
    tags = ['ISIN', 'Bond Code', 'Issuer', 'Bond Type', 'Issue Date', 'Latest Rating']
    try:
        with open(info_file, 'a') as file:
            writer = csv.DictWriter(file, fieldnames=tags)

            if file.tell() == 0:
                writer.writeheader()
            writer.writerow({
                'ISIN': info.get('isin'),
                'Bond Code': info.get('bondCode'),
                'Issuer': info.get('entyFullName'),
                'Bond Type': info.get('bondType'),
                'Issue Date': info.get('issueEndDate'),
                'Latest Rating': info.get('debtRtng')

            })
    except Exception as e:
        print(traceback.format_exc())

if __name__ == '__main__':
    process_data()
