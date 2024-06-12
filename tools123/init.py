import requests

from config import dev
from tools123.Database_Processor import Database_Processor


def get_zj_userid(cea):

    print(dev["urls"]["queryAgentByCea"])
    a = requests.post(dev["urls"]["queryAgentByCea"], data=cea)

    print(a.json())

    return a.json()['data']


def init_jk_database():
    db_processor1 = Database_Processor(dev["databaseConfig"])
    db_processor1.connect()

    # 清空接口状态表
    db_processor1.truncate_table(table_name="request_result")


def init_zj_database():
    db_processor1 = Database_Processor(dev["databaseConfig"])
    db_processor1.connect()

    datas = db_processor1.fetch_data_as_dict(table_name="agent_ids")
    for data1 in datas:
        # 修改数据库时间戳
        data = {

            'times': 0,
            "userID": get_zj_userid(cea=data1["cea"])

        }

        db_processor1.update_data(
            table_name="agent_ids",
            update_dict=data,
            condition_column="cea",
            condition_value=data1["cea"],
        )


def init_cj_database():
    db_processor1 = Database_Processor(dev["databaseConfig"])
    db_processor1.connect()

    # 初始化采集表状态
    datas = db_processor1.fetch_data_as_dict(table_name="property_listings")
    for data1 in datas:
        # 修改数据库时间戳
        data = {

            'state': 0,
            'file_type': 0,
            'zr_type': 0,
            'file_time': 0,
            'zr_time': 0,
            'type_time': 0,

        }

        db_processor1.update_data(
            table_name="property_listings",
            update_dict=data,
            condition_column="id",
            condition_value=data1["id"],
        )


class Init:

    def init_database(self):
        # 清空接口状态表
        init_jk_database()

        # 初始化中介表
        init_zj_database()

        # 初始化采集表
        init_cj_database()
