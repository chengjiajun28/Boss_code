import datetime
import re


class Data_Processor:

    #   截取数字
    def find_numbers(self, text):
        """
         从文本中查找并提取所有的数字（包括小数）。

         参数:
         text: str - 需要搜索数字的文本。

         返回值:
         str - 找到的所有数字，以字符串形式返回，数字间没有空格。
         """

        # 使用正则表达式匹配数字字符，包括小数点后的数字部分
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        return ''.join(numbers)

    def get_today_timestamp(self):
        """

        """

        # 获取当前日期
        today = datetime.date.today()

        # 将当前日期转换为当天零点的 datetime 对象
        today_start = datetime.datetime.combine(today, datetime.time.min)

        # 将当天零点的 datetime 对象转换为时间戳（单位为秒）
        time_str = int(today_start.timestamp())

        return time_str

    def get_todo_strtime(self, *args, **kwargs):
        current_time = datetime.datetime.now()

        return current_time
