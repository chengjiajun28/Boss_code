import requests

from config import dev
from tools123.Database_Processor import Database_Processor


def get_zj_id(id1, db_processor):
    condition_dict = {'agent_id': id1, }
    condition_rules = {'agent_id': '=', }
    datas2 = db_processor.query_data(table_name="agent_ids", condition_dict=condition_dict,
                                     condition_rules=condition_rules)

    data = datas2[0]['cea']

    a = requests.post(dev["urls"]["queryAgentByCea"], data=data)

    return a.json()['data']


def init_zj_id(id1, db_processor):
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

    # 初始化总结表状态
    datas = db_processor1.fetch_data_as_dict(table_name="agent_ids")
    for data1 in datas:
        # 修改数据库时间戳
        data = {

            'times': 0,

        }

        db_processor1.update_data(
            table_name="agent_ids",
            update_dict=data,
            condition_column="agent_id",
            condition_value=data1["agent_id"],
        )


