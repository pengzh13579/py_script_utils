# Author pengzihao
# Date 2019/1/4
"""
查询上网IP对应的地理位置
1、获得本机的IP地址，通过
    http://pv.sohu.com/cityjson
    获得局域网外IP地址
2、通过geoip2工具，解析IP并获得具体的地理位置信息
"""

import geoip2.database
import requests
import re
import json
from tools.location_info import Location


# 根据IP地址获取位置，需要的IP地址为非局域网的ip地址
def get_local_net(ip):
    reader = geoip2.database.Reader('GeoLite2/GeoLite2-City.mmdb')
    try:
        response = reader.city(ip)
        location_info = Location(response.continent.names["zh-CN"],
                                 response.country.names["zh-CN"],
                                 response.subdivisions.most_specific.names["zh-CN"],
                                 response.city.names["zh-CN"],
                                 response.location.longitude,
                                 response.location.latitude,
                                 response.location.time_zone,
                                 response.postal.code)
        return location_info
    except Exception as e:
        print('Error:', e)


if __name__ == '__main__':

    # 本机的IP地址
    s = requests.session()
    rex_ip = r'\{[\s\S]+\}'
    rex_operator = r'(\s\S*)</b><br/>'
    # 获取本地上网的IP
    ipUrl = 'http://pv.sohu.com/cityjson'
    ipContext = re.findall(rex_ip, s.get(ipUrl).content.decode('gbk'))
    ipInfo = ipContext[0]
    # json解析
    dicIP = json.loads(ipInfo)

    # 如果直接调用json.dumps会报错，因为
    # json.dumps方法不能对自定义对象直接序列化,首先把自定义对象转换成字典
    # TypeError: Object of type 'Location' is not JSON serializable
    location = get_local_net(dicIP['cip']).__dict__
    print(json.dumps(location, ensure_ascii=False))
