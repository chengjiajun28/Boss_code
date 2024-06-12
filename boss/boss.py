import random
import threading
import time
from DrissionPage import ChromiumOptions, ChromiumPage
from bs4 import BeautifulSoup
from pymysql.converters import escape_string
from tools123.Database_Processor import DatabaseProcessor

lock = threading.Lock()  # 创建线程锁


# 定义函数：移除HTML标签
def remove_html_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    span_tags = soup.find_all('span')

    for span_tag in span_tags:
        if span_tag.string:
            replacement = span_tag['original-value']
            span_tag.string.replace_with(replacement)
        else:
            span_tag.string = span_tag['original-value']
        span_tag.unwrap()

    html_string = soup.prettify().replace('\n', '')
    html_string = html_string.replace('<br/>', '\n')

    return html_string


# 主要处理函数
def main(page, url):
    tab = page.new_tab(url)
    details_text = ""
    for _, i in enumerate(tab.eles('x://*[@id="main"]/div[3]/div/div[2]/div[1]/div')):
        if _ < 2:
            continue
        details_text += i.html

    try:
        activity = tab.ele('x://*[@id="main"]/div[3]/div/div[2]/div[1]/div[last()]/h2/span').text
    except Exception as e:
        activity = None

    data = {
        # 标题
        "title": tab.ele('x://*[@id="main"]/div[1]/div/div/div/div[2]/h1').text,
        # 详情
        "details": escape_string(details_text),
        # 招聘人  //*[@id="main"]/div[3]/div/div[2]/div[1]/div[4]/h2/
        "name": tab.ele('x://*[@id="main"]/div[3]/div/div[2]/div[1]/div[last()]/h2').text,
        # 公司，
        "company": tab.ele('x://*[@id="main"]/div[3]/div/div[2]/div[1]/div[last()]/div[2]').text,
        # 城市
        "city": tab.ele('x://*[@id="main"]/div[1]/div/div/div[1]/p/a').text,
        # 活跃度
        "activity": activity,

        "url": url
    }

    tab.close()
    with lock:  # 使用线程锁确保数据操作的同步

        condition_dict = {'url': url, }
        condition_rules = {'url': '=', }

        a = database.query_data(table_name="job_opportunities", condition_dict=condition_dict,
                                condition_rules=condition_rules, )

        if a:
            database.update_data(
                table_name="job_opportunities",
                update_dict=data,
                condition_column="url",
                condition_value=url,
            )

            return

        database.insert_dict_into_mysql(data=data, table_name="job_opportunities")


if __name__ == '__main__':
    # 数据库连接配置
    conn = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '111111',
        'database': 'datas'
    }

    database = DatabaseProcessor(config=conn)
    database.connect()

    co = ChromiumOptions().use_system_user_path()
    page = ChromiumPage(co)

    page.listen.start('wapi/zpgeek/search/joblist.json')  # 开始监听，指定获取包含该文本的数据包
    page.get('https://www.zhipin.com/web/geek/job?query=python&city=101270100')  # 访问网址

    for _ in range(1, 10):
        res_jsons = None
        for packet in page.listen.steps(count=1):
            res_jsons = packet.response.body  # 打印数据包url

        for i in res_jsons["zpData"]["jobList"]:
            url = f'https://www.zhipin.com/job_detail/{i["encryptJobId"]}.html?lid={i["lid"]}&securityId={i["securityId"]}&sessionId='

            # 创建线程处理数据
            threading.Thread(target=main, args=(page, url)).start()

            time.sleep(random.randint(1, 3))

        try:
            page.ele('x://*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/div/div/div/a[last()]').click(by_js=True)
        except Exception as e:
            page.ele('x://*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/div/div/div/a[last()]').click(by_js=True)

    page.quit()
