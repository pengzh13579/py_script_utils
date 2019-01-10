# Author pengzihao
# Date 2019/1/4

"""
地理位置信息类
area：地区
country：国家
subdivisions：省
city：城市
longitude：经度
latitude：纬度
time_zone：时区
code：邮编
"""

class Location(object):
    def __init__(self, area, country, subdivisions, city, longitude, latitude, time_zone, code):
        self.area = area
        self.country = country
        self.subdivisions = subdivisions
        self.city = city
        self.longitude = longitude
        self.latitude = latitude
        self.time_zone = time_zone
        self.code = code
