# Author pengzihao
# Date 2019/1/9

import logging
from data_analysis.qq_record_db_operator import qq_record_db_operator, message_insert

LOG_FILENAME_NOTE = "../log/log.txt"
logging.basicConfig(filename=LOG_FILENAME_NOTE, level=logging.INFO)


def log(msg):
    logging.info(str(msg))

class qq_record_analysis(object):
    def __init__(self):
        # 这个初始化变量还真是有点对 我把这个当做函数公共变量来使用了 不知道设计算不算合理 先用着吧
        # self.db_result = self.get_db_reslt()
        # self.first_strike_up = ''
        # self.sec_strike_up = ''
        # self.history_name = []
        # self.chat_his = []  # 聊天历史年份
        # self.year_time = 2  # 默认时长两年
        # self.time_gap = []
        # self.count_word = {}
        # self.year_list = []
        # self.day_dict = {}
        # self.row_day_dict = {}
        # self.boy_rate_list = []
        # self.girl_rate_list = []
        # self._first_time = ''
        # self._last_time = ''
        pass



if __name__ == "__main__":
    moniter = qq_record_analysis()
    message_insert()