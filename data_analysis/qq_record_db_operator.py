# Author pengzihao
# Date 2019/1/9
import os
import re
from colorama import init, Fore, Back, Style


class qq_record_db_operator(object):

    # 调用一次 传递一个游标
    def __init__(self):
        self.file_list=[]


    def connect_db(self):
        # 没发现这个用dict 可以传递现在用函数传递游标也行吧
        import sqlite3
        conn = sqlite3.connect('message.db')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS "message" (
        "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        "message"  TEXT,
        "send_user"  TEXT,
        "send_time"  INTEGER
        );
        ''')
        return conn


    def get_path(self):
        file_lists = []
        root_dir = os.getcwd() + '/' + 'message' + '/'
        for i in os.listdir(root_dir):
            if '.txt' in i:
                file_lists.append(root_dir + i)

        if not file_lists:
            print("error：没有找到相关的文件")
            #raise FileError

        self.file_list = file_lists
        return file_lists

    # 目前就支持单文本导入即可，多了累赘
    def check_format(self, path_dict):
        for file in path_dict:
            file_count = 0
            with open(file, 'r', encoding="utf8") as check_file:
                count = 0
                error_tag = 0
                for line in check_file:
                    count = count + 1
                    if count == 4:
                        if '消息分组' in line:
                            print(line)
                        else:
                            error_tag += 1
                    if count == 6:
                        if '消息对象' in line:
                            print(line)
                            self.girl_name = line[9:]
                        else:
                            error_tag += 1
            if error_tag > 0:
                print(Fore.RED + '该文本不符合导入要求，已经从列表中删除')
                del path_dict[file_count]
            else:
                print(Fore.GREEN + '检测完成 下一步生成数据库文件')
            file_count += 1
        return path_dict

    def get_content(self, file_lists):
        data = []
        for file in file_lists:
            with open(file, 'r', encoding='utf8') as qq_msg:
                db_content = {}
                # 解析QQ消息并导入到数据库
                for line in qq_msg.readlines()[8:]:
                    # 判断是否为标题，格式为时间的格式，如2019-01-09 17:22:30 昵称
                    if re.findall('\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2}', line):
                        # 如果存在上一行信息封装好 那么本次运行就插入到数据库 或者自己再做一个字典
                        if db_content:
                            change_formate = (db_content['time'], db_content['content'], db_content['user'])
                            data.append(change_formate)
                            db_content = {}
                        msg_time = re.findall('\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2}', line)
                        msg_time = msg_time[0]
                        # 一般来讲 QQ的用户名20个字符就足够了
                        # 但是我发现有一个小bug 就是如果是英文好友 就会出现未查询到
                        msg_user = re.findall('[\u4e00-\u9fa5]{1,20}', line)
                        if msg_user:
                            msg_user = msg_user[0]
                        else:
                            msg_user = str(line[19:])
                        db_content['time'] = msg_time
                        db_content['user'] = msg_user
                    else:
                        if 'content' in db_content.keys():
                            db_content['content'] = str(db_content['content']).join(line).replace('\n', '')
                        else:
                            db_content['content'] = line
        return data

    def insert_db(self, data):
        db = self.connect_db()
        cursor = db.cursor()
        insert_sql = "INSERT INTO message(send_time,message,send_user) VALUES (?, ?, ?)"
        select_sql = "SELECT * FROM message"
        cursor.execute(select_sql)
        check_result = cursor.fetchall()
        # 如果数据库为空才导入，不为空则不导入 后续还是要加入判定 或者没运行一次就删除一次
        if check_result:
            print(Fore.YELLOW + '数据库中已经存在了需要检测的聊天记录,本次不会导入！')
        else:
            print(Fore.GREEN + '正在导入你的聊天数据，请稍后.....')
            cursor.executemany(insert_sql, data)
        db.commit()


def message_insert():
    message_db_name = os.getcwd()+'/message.db'
    # 删除旧有的信息，不要判断新旧
    if os.path.exists(message_db_name):
        os.remove(message_db_name)
    qq_record_db_operator().insert_db(qq_record_db_operator().get_content(qq_record_db_operator().get_path()))
