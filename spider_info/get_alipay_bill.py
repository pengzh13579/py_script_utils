# Author pengzihao
# Date 2019/1/9
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import re


def login_alipay(login_name, login_password):

    chrome_driver = "../application/chromedriver"
    os.environ["webdriver.chrome.driver"] = chrome_driver
    driver = webdriver.Chrome(chrome_driver)
    driver.get("https://auth.alipay.com/login/index.htm")
    # 获取当前窗口的handle
    driver.current_window_handle
    driver.find_element_by_xpath('//*[@data-status="show_login"]').click()
    user_name = WebDriverWait(driver, 10, 1).until(
        EC.presence_of_element_located((By.ID, "J-input-user"))
    )
    password = WebDriverWait(driver, 10, 1).until(
        EC.presence_of_element_located((By.ID, "password_rsainput"))
    )
    login_btn = WebDriverWait(driver, 10, 1).until(
        EC.presence_of_element_located((By.ID, "J-login-btn"))
    )
    if user_name and password and login_btn:
        # 支付宝帐号
        user_name.send_keys(login_name)
        # 点击输入密码的文本框
        password.click()
        # 支付宝密码
        password.send_keys(login_password)
        time.sleep(10)
        # 点击登录按钮
        login_btn.click()
        time.sleep(10)
    return driver


def get_alipay_record(driver, month_date):
    # 获取当前窗口的handle
    driver.current_window_handle
    driver.get('https://consumeprod.alipay.com/record/standard.htm')
    time.sleep(2)

    flag = True
    keep_safe(driver, flag)
    year_button = driver.find_element_by_xpath('//*[@id="J-one-year"]')
    three_month_button = driver.find_element_by_xpath('//*[@id="J-three-month"]')
    one_month_button = driver.find_element_by_xpath('//*[@id="J-one-month"]')
    if month_date == 1:
        one_month_button.send_keys(Keys.ENTER)
    elif month_date == 3:
        three_month_button.send_keys(Keys.ENTER)
    elif month_date == 12:
        year_button.send_keys(Keys.ENTER)
    keep_safe(driver, flag)
    rex_page = re.compile(r'1 - 10条，共(.*)条')
    total_page = rex_page.findall(driver.find_element_by_xpath('//*[@class="page-link"]').text)[0]
    for i in range(int(total_page)):
        if i == 0:
            pass
        else:
            element = driver.find_element_by_class_name('page-next')
            element.click()
        time.sleep(3)
        keep_safe(driver)
        try:
            get_bill_info(driver)
        except:
            pass


def keep_safe(driver, flag):
    try:
        while(flag):
            qr_code = driver.find_element_by_xpath('//*[@id="container"]/h2').text
            text = "安全校验"
            if qr_code == text:
                print(text)
                print("请在30s内验证")
                time.sleep(30)
                if text == "安全校验":
                    qr_code_2 = driver.find_element_by_xpath('//*[@id="container"]/h2').text
                    if qr_code == qr_code_2:
                        flag = True
                    else:
                        flag = False
                elif text == "登录":
                    qr_code_2 = driver.find_element_by_xpath('/html/body/div/div[1]/div/h1/a[2]').text
                    if qr_code == qr_code_2:
                        flag = True
                    else:
                        flag = False
    except:
        pass


def get_bill_info(driver):
    global N
    for num in range(10):
        num = num + 1
        al_day_xpath = '//*[@id="J-item-' + str(num) + '"]/td[2]/p[1]'  # //*[@id="J-item-1"]/td[2]/p[1]    日期
        al_time_xpath = '//*[@id="J-item-' + str(num) + '"]/td[2]/p[2]'  # //*[@id="J-item-1"]/td[2]/p[2]    时刻
        al_way_xpath = '//*[@id="J-item-' + str(num) + '"]/td[3]/p[1]'  # //*[@id="J-item-1"]/td[3]/p[1]    方式
        al_payee_xpath = '//*[@id="J-item-' + str(num) + '"]/td[3]/p[2]'  # //*[@id="J-item-1"]/td[3]/p[2]/span 收款人
        al_snum_xpath = '//*[@id="J-tradeNo-' + str(num) + '"]'  # //*[@id="J-tradeNo-1"] 号#.get_attribute("title")
        al_figure_xpath = '//*[@id="J-item-' + str(num) + '"]/td[4]/span'  # //*[@id="J-item-1"]/td[4]/span    金额
        al_status_xpath = '//*[@id="J-item-' + str(num) + '"]/td[6]/p[1]'  # //*[@id="J-item-1"]/td[6]/p[1]    交易状态

        al_day = driver.find_element_by_xpath(al_day_xpath).text
        al_time = driver.find_element_by_xpath(al_time_xpath).text
        al_way = driver.find_element_by_xpath(al_way_xpath).text
        al_payee = driver.find_element_by_xpath(al_payee_xpath).text
        al_snum = driver.find_element_by_xpath(al_snum_xpath).get_attribute("title")
        al_figure = driver.find_element_by_xpath(al_figure_xpath).text
        al_status = driver.find_element_by_xpath(al_status_xpath).text
        print(str(
            N) + '.' + '日期' + ':' + al_day + '\t时间' + ':' + al_time + '\t方式' + ':' + al_way +
              '\t收款人' + ':' + al_payee + '\t流水号' + ':' + al_snum + '\t金额' + ':' + al_figure +
              '\t交易状态' + ':' + al_status)
        N = N + 1


def start_spider(login_name, login_password, month_date):
    driver = login_alipay(login_name, login_password)
    get_alipay_record(driver, month_date)


if __name__ == "__main__":
    print("输入用户名")
    username = input()
    print("输入密码")
    password = input()
    start_spider(username, password, 12)
