# Author pengzihao
# Date 2018/09/19
"""


"""
# pip3 install beautifulsoup4
from bs4 import BeautifulSoup
import re
import os
import pymysql
import configparser
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

# 统计用区划和城乡划分代码URL
start_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

# 生成config对象用于读取db.conf文件
conf = configparser.ConfigParser()
# 读取文件
conf.read('../conf/get_area_conf.conf')
# 获得DB相关配置
db_host = conf.get('db', 'db_host')
db_user = conf.get('db', 'db_user')
db_pass = conf.get('db', 'db_pass')
db_port = conf.getint('db', 'db_port')
db_database = conf.get('db', 'db_database')

# 获得相关标记位
# 是否需要爬取镇街道级区域划分
town_flag = conf.getboolean('get_flag', 'town_flag')
# 是否需要爬取村社级区域划分
village_flag = conf.getboolean('get_flag', 'village_flag')

# SQL连接（mysql）
conn = pymysql.connect(host=db_host, user=db_user, passwd=db_user, port=db_port, db=db_database, charset='utf8')

cur = conn.cursor()

# 清空已存在的表
cur.execute('truncate fix_province')
cur.execute('truncate fix_county')
cur.execute('truncate fix_district')
if town_flag:
    cur.execute('truncate fix_town')
if village_flag:
    cur.execute('truncate fix_village')

global driver


# 获取最新的行政区域和城乡划分的URL
def get_new_url(url):
    soup = get_soup_by_url(url)

    # 获得最新的行政区域划分的网页
    link = soup.select('ul.center_list_contlist > li > a')[0]
    print("当前最新的行政区域划分为：" + link.text)

    # 省级区域划分
    get_province_urls(link.get('href'))


# 获取最新的省级区域划分并保存
def get_province_urls(url):
    soup = get_soup_by_url(url)
    head = soup.select('tr.provincehead > td > strong')[0]
    print("当前最新的行政区域划分为：" + head.text)
    province_infos = soup.select('tr.provincetr > td > a')
    province_set = []
    for info in province_infos:
        # 省级代码
        province_cd = info.get("href").split('.')[0]
        # 省级名
        province_name = info.text
        province_set.append((province_cd, province_name))
        # 市级区域划分
        get_county_urls(url.split("index.html")[0] + info.get("href"), province_cd)
    # 批量插入数据库
    cur.executemany('insert into fix_province(province_id, province_name) value(%s, %s)', province_set)


# 获取最新的市级区域划分并保存
def get_county_urls(url, parent_cd):
    soup = get_soup_by_url(url)
    county_infos = soup.select('tr.citytr')
    county_set = []
    for info in county_infos:
        # 市级代码
        county_cd = re.compile('\d+').findall(info.text)[0]
        # 市级名
        county_name = info.text.split(county_cd)[1]
        county_set.append((county_cd, county_name, parent_cd))
        # 区县级区域划分
        get_district_urls(url.rsplit('/', 1)[0] + "/" + info.find_all("a")[0].get("href"), county_cd)
    # 批量插入数据库
    cur.executemany('insert into fix_county(county_id, county_name, father_province) value(%s, %s, %s)', county_set)


# 获取最新的区县级区域划分并保存
def get_district_urls(url, parent_cd):
    soup = get_soup_by_url(url)
    district_infos = soup.select('tr.countytr')
    district_set = []
    for info in district_infos:
        # 区县级代码
        district_cd = re.compile('\d+').findall(info.text)[0]
        # 区县级名
        district_name = info.text.split(district_cd)[1]
        district_set.append((district_cd, district_name, parent_cd))
        if town_flag:
            if info.find_all("a").__len__() > 0:
                # 镇街道级区域划分
                get_town_urls(url.rsplit('/', 1)[0] + "/" + info.find_all("a")[0].get("href"), district_cd)
    # 批量插入数据库
    cur.executemany('insert into fix_district(district_id, district_name, father_county) value(%s, %s, %s)', district_set)


# 获取最新的镇街道级区域划分并保存
def get_town_urls(url, parent_cd):
    soup = get_soup_by_url(url)
    town_infos = soup.select('tr.towntr')
    town_set = []
    for info in town_infos:
        # 镇街道级代码
        town_cd = re.compile('\d+').findall(info.text)[0]
        # 镇街道级名
        town_name = info.text.split(town_cd)[1]
        town_set.append((town_cd, town_name, parent_cd))
        if village_flag:
            # 村社级区域划分
            get_village_urls(url.rsplit('/', 1)[0] + "/" + info.find_all("a")[0].get("href"), town_cd)
    # 批量插入数据库
    cur.executemany('insert into fix_town(town_id, town_name, father_distinct) value(%s, %s, %s)', town_set)


# 获取最新的村社级区域划分并保存
def get_village_urls(url, parent_cd):
    soup = get_soup_by_url(url)
    village_infos = soup.select('tr.villagetr')
    village_set = []
    for info in village_infos:
        # 村社级代码
        village_cd = info.find_next("td").text
        # 村社城乡分类代码
        village_type_cd = info.find_next("td").find_next("td").text
        # 村社级名
        village_name = info.find_next("td").find_next("td").find_next("td").text
        village_set.append((village_cd, village_type_cd, village_name, parent_cd))
    # 批量插入数据库
    cur.executemany('insert into fix_village(village_cd, village_type_cd, village_name, father_town) value(%s, %s, %s, %s)', village_set)


# 通过URL爬取并解析html
def get_soup_by_url(url):

    # 这里通过get请求需要模拟登录的页面
    # 爬取网页
    time.sleep(3)
    driver.get(url)
    index_data = driver.page_source
    # index_data = requests.get(url, headers=headers)
    # decode_character = index_data.apparent_encoding

    # 避免报错：UnicodeDecodeError: 'gb2312' codec can't decode
    # 如果字符串string中有诸如某些繁体字，例如"河滘小学"
    # 那么gb2312作为简体中文编码是不能进行解析的，必须使用国标扩展码gbk，gbk支持繁体中文和日文假文
    # if index_data.apparent_encoding.upper() == "GB2312":
    #    decode_character = "GBK"

    # return BeautifulSoup(index_data.page_source.encode(index_data.encoding).decode(decode_character))
    return BeautifulSoup(index_data)


dcap = dict(DesiredCapabilities.PHANTOMJS)
chrome_driver = "../application/chromedriver"
os.environ["webdriver.chrome.driver"] = chrome_driver

# dcap["phantomjs.page.settings.userAgent"] = (r"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36")
# driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe', desired_capabilities=dcap)
driver = webdriver.Chrome(chrome_driver)
get_new_url(start_url)
