import re
from datetime import datetime


def re_search(text, regex_list):
    res = {}
    text = text.replace(' ', '').replace('\n', '')
    for key, regexes in regex_list.items():
        for regex in regexes:
            matches = re.findall(regex, text)
            date_ls = []
            for match in matches:
                if isinstance(match, tuple):
                    date_start = '-'.join(match[0:3])
                    date_end = '-'.join(match[3:])
                    dt = datetime.strptime(date_start, "%Y-%m-%d").strftime('%Y-%m-%d')
                    de = datetime.strptime(date_end, "%Y-%m-%d").strftime('%Y-%m-%d')
                    date_ls.append(dt)
                    date_ls.append(de)
                    res['换股期限'] = date_ls
                else:
                    res['标的证券'] = match
    return res

text = """
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债
券。
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
日至 2027 年 6 月 1 日止。
"""

regex_list = {
    '标的证券': [
        r'股票代码：\s*(\d{6}\.(?:SH|SZ))'
    ],
    '换股期限': [
        r'(\d{4})年\s*(\d{1,2})月\s*(\d{1,2})日\s*至\s*(\d{4})年\s*(\d{1,2})月\s*(\d{1,2})日'
    ]
}
if __name__ == '__main__':
    print(re_search(text, regex_list))
