
from DrissionPage import ChromiumOptions, ChromiumPage

co = ChromiumOptions().use_system_user_path()
page = ChromiumPage(co)

tab = page.new_tab("https://www.zhipin.com/web/geek/job?query=python&city=101270100&page=1")

for _ in range(1, 10):
    for html_class in tab.eles('x://*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li'):
        #                  //*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li[1]/div[1]/a

        html_class.ele("x:.//div[1]/a")
        url1 = html_class.ele('x:.//div[1]/a').attr("href")

        print(url1)