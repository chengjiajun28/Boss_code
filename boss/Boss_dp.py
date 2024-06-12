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

    data = {
        "title": tab.ele('x://*[@id="main"]/div[1]/div/div/div/div[2]/h1').text,
        "details": escape_string(details_text),
        "name": tab.ele('x://*[@id="main"]/div[3]/div/div[2]/div[1]/div[last()]/h2').text,
        "company": tab.ele('x://*[@id="main"]/div[3]/div/div[2]/div[1]/div[last()]/div[2]').text,
        "url": url
    }

    tab.close()
    with lock:  # 使用线程锁确保数据操作的同步
        database.insert_dict_into_mysql(data=data, table_name="job_opportunities")
        print(data)

    return data


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

    tab = page.new_tab("https://www.zhipin.com/web/geek/job?query=python&city=101270100&page=1")

    for _ in range(1, 10):
        for html_class in tab.eles('x://*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li'):
            #                  //*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li[1]/div[1]/a

            url1 = html_class.ele('x:.//div[1]/a').attr("href")

            # 创建线程处理数据
            threading.Thread(target=main, args=(page, url1)).start()

            time.sleep(random.randint(1, 3))

        tab.ele('x://*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/div/div/div/a[last()]').click()
