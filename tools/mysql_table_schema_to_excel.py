# Author pengzihao
# Date 2019/1/7
"""
通过修改配置文件，连接数据库
导出特定数据库的表结构
1、读取配置文件，得到数据库的配置信息和数据库名
2、查询information_schema.TABLES中，该数据库内所有表信息
3、遍历表信息，查询information_schema.COLUMNS中所有列
4、通过xlsxwriter来导出到excel中
"""
import configparser
import pymysql
import xlsxwriter


# 生成config对象用于读取db.conf文件
conf = configparser.ConfigParser()
# 读取文件
conf.read('conf/mysql_table_to_excel.conf')
# 获得DB相关配置
db_host = conf.get('db', 'db_host')
db_user = conf.get('db', 'db_user')
db_pass = conf.get('db', 'db_pass')
db_port = conf.getint('db', 'db_port')
db_database = conf.get('db', 'db_database')

# 导出的excel的保存目录
export_path = conf.get('export_path', 'export_path')

# SQL连接（mysql）
conn = pymysql.connect(host=db_host, user=db_user, passwd=db_user, port=db_port, db=db_database, charset='utf8')
curr = conn.cursor()

workbook = xlsxwriter.Workbook(r'{export_path}/{export_name}.xlsx'.format(export_path=export_path,
                                                                          export_name=db_database))
sheet_index = workbook.add_worksheet('导航')
sheet_index.set_column(0, 0, 20)
sheet_index.set_column(1, 1, 20)


def get_schema_table():
    selectSql = "select  \
                    TABLE_NAME,  \
                    TABLE_COMMENT  \
                from information_schema.TABLES  \
                where TABLE_SCHEMA='{schemaName}';"\
        .format(schemaName=db_database)
    curr.execute(selectSql)
    table_names = curr.fetchall()
    line = 0
    for tabName in table_names:
        sheet_index.write_url(line, 0, ("#'" + tabName[1]+"-"+tabName[0]+"'!A1"), None, tabName[1])
        sheet_index.write(line, 1, tabName[0])
        mysql_table_structure_2_excel(tabName)
        line += 1


def mysql_table_structure_2_excel(tab_name):

    head_format = workbook.add_format({
        # 字体加粗
        'bold': 1,
        # 单元格边框宽度
        'border': 1,
        # 单元格背景颜色
        'fg_color': '#00CCFF',
        # 对齐方式
        'align': 'left',
        # 字体对齐方式
        'valign': 'vcenter',
    })

    info_format = workbook.add_format({
        # 单元格边框宽度
        'border': 1,
        # 对齐方式
        'align': 'left',
    })

    selectSql = "SELECT ORDINAL_POSITION colNo, \
                    COLUMN_NAME colName, \
                    COLUMN_TYPE dataType, \
                    IS_NULLABLE isNull, \
                    COLUMN_COMMENT colComment \
                FROM information_schema.COLUMNS \
                WHERE TABLE_SCHEMA = '{schemaName}' \
                AND table_name = '{tabName}';"\
        .format(schemaName=db_database, tabName=tab_name[0])

    curr.execute(selectSql)
    table_info = curr.fetchall()
    fields = curr.description
    sheet = workbook.add_worksheet('{tabName}'.format(tabName=tab_name[1] + "-" + tab_name[0]))

    # 设定第1到1列的列宽为10
    sheet.set_column(0, 0, 5)
    sheet.set_column(1, 1, 20)
    sheet.set_column(2, 2, 20)
    sheet.set_column(3, 3, 8)
    sheet.set_column(4, 4, 20)
    # 写上字段信息
    for field in range(0, len(fields)):
        sheet.write(0, field, fields[field][0], head_format)

    # 获取并写入数据段信息
    for row in range(1, len(table_info) + 1):
        for col in range(0, len(fields)):
            sheet.write(row, col, u'%s' % table_info[row - 1][col], info_format)


# Batch
get_schema_table()
workbook.close()
