# Author pengzihao
# Date 2019/1/4
"""
查询上网IP/域名对应的信息
1、根据输入的信息，判断输入的是域名还是IP地址
2-1、输入的是域名时，返回域名对应的IP地址和IP所在地
2-2、输入的是IP时，返回IP地址所在地
"""

import requests
import re


# 判断是否是IP，判定是否大于0且小于255
def is_ip(ip):
    return len([i for i in ip.split('.') if (0 <= int(i) <= 255)]) == 4


# 输入是IP处理函数
def find_ip(ip):
    s = requests.session()
    ip_content = s.get('http://wap.ip138.com/ip.asp?ip=%s' % ip).content.decode('utf-8')
    rex_ip = re.compile(r'<br/><b>查询结果：(.*)</b><br/>')
    result = rex_ip.findall(ip_content)
    return "查询IP：%s \t %s" % (ip, result[0])


# 输入是域名的处理函数
def domain(dm):
    s = requests.session()
    dm_content = s.get('http://wap.ip138.com/ip.asp?ip=%s' % dm).content.decode('utf-8')
    rex_dm = re.compile(r'&gt; (.*)\t\r\n<br/><b>查询结果：(.*)</b><br/>')
    result = rex_dm.findall(dm_content)
    return '查询域名：%s \t IP地址：%s\t%s' % (dm, result[0][0], result[0][1])


# 输入是域名的处理函数
def check_input_info(info):
    # 判断是否为IP地址的格式
    if not re.findall('(\d{1,3}\.){3}\d{1,3}', info):
        # 判断域名的格式是否正确
        if re.findall(r'(\w+\.)?(\w+)(\.\D+){1,2}', info):
            return domain(info)
        else:
            return "输入的域名格式不正确，请重新输入"
    else:
        if is_ip(info):
            return find_ip(info)
        else:
            return "IP地址不合法，请重新输入"


if __name__ == "__main__":
    print("输入IP地址:")
    input_info = input()
    result_info = check_input_info(input_info)
    print(result_info)
