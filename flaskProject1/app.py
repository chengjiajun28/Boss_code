import html
import re

from bs4 import BeautifulSoup
from flask import Flask, render_template, request

from datetime import datetime
from markupsafe import Markup

from tools123.Database_Processor import DatabaseProcessor

app = Flask(__name__)

job_listings = [
    {
        'title': 'Python！开发（接受应届，线上面试）',
        'details': Markup(
            '<div class="job-sec-text">全程线上面试，薪资结构基础工资2~4个月年终奖+加班费:六险一金，全额基数缴纳社保公积金，合同四年起签<br>1、有嵌入式软件开发、通用软件开发、软件算法、媒体算法、音频算法、自动化控制制、精密装备开发与自动化等软件相关工作经验:<br>2、热爱编程，基础扎实，熟悉掌握但不限于JAVA/C++/C/Python/JS/HTML/GO等编程语言中的一种或数种，有良好的编程习惯;</div><div class="detail-section-item company-certification">\n                                <h3>认证资质<span class="company-certification-icon"></span></h3>\n                                <div class="certification-container">\n                                    <ul class="certification-tags">\n                                            <li>人力资源服务许可证</li>\n                                            <li>劳务派遣经营许可证</li>\n                                    </ul>\n                                </div>\n                                <div id="certification-content" class="certification-text" style="display: none;">\n                                    <h2 class="certification-title">资质说明</h2>\n                                    <ul class="certification-text">\n                                            <li>\n                                                <h2>人力资源服务许可证</h2>\n                                                <p>人力资源服务许可证是由国家人力资源与社会保障相关部门颁发，代表人才经纪人所在企业可以合法开展人力资源相关业务的资质证件。展示标签代表该企业已上传许可证并经由平台审核验证通过。</p>\n                                            </li>\n                                            <li>\n                                                <h2>劳务派遣经营许可证</h2>\n                                                <p>劳务派遣经营许可证是由国家人力资源与社会保障相关部门颁发，代表人才经纪人所在企业可以合法开展劳务派遣相关业务的资质证件。展示标签代表该企业已上传许可证并经由平台审核验证通过。</p>\n                                            </li>\n                                    </ul>\n                                </div>\n                            </div><div class="job-boss-info">\n                            <div class="detail-figure">\n                                    <img src="https://img.bosszhipin.com/beijin/upload/avatar/20220201/607f1f3d68754fd0203107643f9fe240fefd1b0f1a47515d4c3cbc9cc8c86736476cef340ba87362_s.png?x-oss-process=image/resize,w_100,limit_0" alt="">\n                            </div>\n                            <h2 class="name">肖先生<i class="icon-vip"></i>\n                            </h2>\n                            <div class="boss-info-attr">\n                                科锐国际<em class="vdot">·</em>猎头顾问\n                                \n                            </div>\n                        </div>'),
        'name': '肖先生',
        'company': '科锐国际·猎头顾问',
        'url': 'https://www.zhipin.com/job_detail/00171a87bfe82e9e1HR42N68EFZX.html?lid=9kkPueb6I1i.search.27&securityId=VIVvRiBTKxbcA-d1COUwVzxBRPM1-CUptHvz-MJFhJgXh69MDXOUQdxOI-NHJF0DZHgORkJZyxKU9h9miNdH30Z0C492S2SqnD8LZUmTQJ2R7C0~&sessionId=',
        'date_added': datetime(2024, 6, 10, 6, 29, 45),
        'city': '成都',
        'activity': None
    },
    {
        'title': 'Python！开发（接受应届，线上面试）',
        'details': Markup(
            '<div class="job-sec-text">全程线上面试，薪资结构基础工资2~4个月年终奖+加班费:六险一金，全额基数缴纳社保公积金，合同四年起签<br>1、有嵌入式软件开发、通用软件开发、软件算法、媒体算法、音频算法、自动化控制制、精密装备开发与自动化等软件相关工作经验:<br>2、热爱编程，基础扎实，熟悉掌握但不限于JAVA/C++/C/Python/JS/HTML/GO等编程语言中的一种或数种，有良好的编程习惯;</div><div class="detail-section-item company-certification">\n                                <h3>认证资质<span class="company-certification-icon"></span></h3>\n                                <div class="certification-container">\n                                    <ul class="certification-tags">\n                                            <li>人力资源服务许可证</li>\n                                            <li>劳务派遣经营许可证</li>\n                                    </ul>\n                                </div>\n                                <div id="certification-content" class="certification-text" style="display: none;">\n                                    <h2 class="certification-title">资质说明</h2>\n                                    <ul class="certification-text">\n                                            <li>\n                                                <h2>人力资源服务许可证</h2>\n                                                <p>人力资源服务许可证是由国家人力资源与社会保障相关部门颁发，代表人才经纪人所在企业可以合法开展人力资源相关业务的资质证件。展示标签代表该企业已上传许可证并经由平台审核验证通过。</p>\n                                            </li>\n                                            <li>\n                                                <h2>劳务派遣经营许可证</h2>\n                                                <p>劳务派遣经营许可证是由国家人力资源与社会保障相关部门颁发，代表人才经纪人所在企业可以合法开展劳务派遣相关业务的资质证件。展示标签代表该企业已上传许可证并经由平台审核验证通过。</p>\n                                            </li>\n                                    </ul>\n                                </div>\n                            </div><div class="job-boss-info">\n                            <div class="detail-figure">\n                                    <img src="https://img.bosszhipin.com/beijin/upload/avatar/20220201/607f1f3d68754fd0203107643f9fe240fefd1b0f1a47515d4c3cbc9cc8c86736476cef340ba87362_s.png?x-oss-process=image/resize,w_100,limit_0" alt="">\n                            </div>\n                            <h2 class="name">肖先生<i class="icon-vip"></i>\n                            </h2>\n                            <div class="boss-info-attr">\n                                科锐国际<em class="vdot">·</em>猎头顾问\n                                \n                            </div>\n                        </div>'),
        'name': '肖先生',
        'company': '科锐国际·猎头顾问',
        'url': 'https://www.zhipin.com/job_detail/00171a87bfe82e9e1HR42N68EFZX.html?lid=9kkPueb6I1i.search.27&securityId=VIVvRiBTKxbcA-d1COUwVzxBRPM1-CUptHvz-MJFhJgXh69MDXOUQdxOI-NHJF0DZHgORkJZyxKU9h9miNdH30Z0C492S2SqnD8LZUmTQJ2R7C0~&sessionId=',
        'date_added': datetime(2024, 6, 10, 6, 29, 45),
        'city': '成都',
        'activity': None
    },
    {
        'title': 'Python！开发（接受应届，线上面试）',
        'details': Markup(
            '<div class="job-sec-text">全程线上面试，薪资结构基础工资2~4个月年终奖+加班费:六险一金，全额基数缴纳社保公积金，合同四年起签<br>1、有嵌入式软件开发、通用软件开发、软件算法、媒体算法、音频算法、自动化控制制、精密装备开发与自动化等软件相关工作经验:<br>2、热爱编程，基础扎实，熟悉掌握但不限于JAVA/C++/C/Python/JS/HTML/GO等编程语言中的一种或数种，有良好的编程习惯;</div><div class="detail-section-item company-certification">\n                                <h3>认证资质<span class="company-certification-icon"></span></h3>\n                                <div class="certification-container">\n                                    <ul class="certification-tags">\n                                            <li>人力资源服务许可证</li>\n                                            <li>劳务派遣经营许可证</li>\n                                    </ul>\n                                </div>\n                                <div id="certification-content" class="certification-text" style="display: none;">\n                                    <h2 class="certification-title">资质说明</h2>\n                                    <ul class="certification-text">\n                                            <li>\n                                                <h2>人力资源服务许可证</h2>\n                                                <p>人力资源服务许可证是由国家人力资源与社会保障相关部门颁发，代表人才经纪人所在企业可以合法开展人力资源相关业务的资质证件。展示标签代表该企业已上传许可证并经由平台审核验证通过。</p>\n                                            </li>\n                                            <li>\n                                                <h2>劳务派遣经营许可证</h2>\n                                                <p>劳务派遣经营许可证是由国家人力资源与社会保障相关部门颁发，代表人才经纪人所在企业可以合法开展劳务派遣相关业务的资质证件。展示标签代表该企业已上传许可证并经由平台审核验证通过。</p>\n                                            </li>\n                                    </ul>\n                                </div>\n                            </div><div class="job-boss-info">\n                            <div class="detail-figure">\n                                    <img src="https://img.bosszhipin.com/beijin/upload/avatar/20220201/607f1f3d68754fd0203107643f9fe240fefd1b0f1a47515d4c3cbc9cc8c86736476cef340ba87362_s.png?x-oss-process=image/resize,w_100,limit_0" alt="">\n                            </div>\n                            <h2 class="name">肖先生<i class="icon-vip"></i>\n                            </h2>\n                            <div class="boss-info-attr">\n                                科锐国际<em class="vdot">·</em>猎头顾问\n                                \n                            </div>\n                        </div>'),
        'name': '肖先生',
        'company': '科锐国际·猎头顾问',
        'url': 'https://www.zhipin.com/job_detail/00171a87bfe82e9e1HR42N68EFZX.html?lid=9kkPueb6I1i.search.27&securityId=VIVvRiBTKxbcA-d1COUwVzxBRPM1-CUptHvz-MJFhJgXh69MDXOUQdxOI-NHJF0DZHgORkJZyxKU9h9miNdH30Z0C492S2SqnD8LZUmTQJ2R7C0~&sessionId=',
        'date_added': datetime(2024, 6, 10, 6, 29, 45),
        'city': '成都',
        'activity': None
    },
    {
        'title': 'Python！开发（接受应届，线上面试）',
        'details': Markup(
            '<div class="job-sec-text">全程线上面试，薪资结构基础工资2~4个月年终奖+加班费:六险一金，全额基数缴纳社保公积金，合同四年起签<br>1、有嵌入式软件开发、通用软件开发、软件算法、媒体算法、音频算法、自动化控制制、精密装备开发与自动化等软件相关工作经验:<br>2、热爱编程，基础扎实，熟悉掌握但不限于JAVA/C++/C/Python/JS/HTML/GO等编程语言中的一种或数种，有良好的编程习惯;</div><div class="detail-section-item company-certification">\n                                <h3>认证资质<span class="company-certification-icon"></span></h3>\n                                <div class="certification-container">\n                                    <ul class="certification-tags">\n                                            <li>人力资源服务许可证</li>\n                                            <li>劳务派遣经营许可证</li>\n                                    </ul>\n                                </div>\n                                <div id="certification-content" class="certification-text" style="display: none;">\n                                    <h2 class="certification-title">资质说明</h2>\n                                    <ul class="certification-text">\n                                            <li>\n                                                <h2>人力资源服务许可证</h2>\n                                                <p>人力资源服务许可证是由国家人力资源与社会保障相关部门颁发，代表人才经纪人所在企业可以合法开展人力资源相关业务的资质证件。展示标签代表该企业已上传许可证并经由平台审核验证通过。</p>\n                                            </li>\n                                            <li>\n                                                <h2>劳务派遣经营许可证</h2>\n                                                <p>劳务派遣经营许可证是由国家人力资源与社会保障相关部门颁发，代表人才经纪人所在企业可以合法开展劳务派遣相关业务的资质证件。展示标签代表该企业已上传许可证并经由平台审核验证通过。</p>\n                                            </li>\n                                    </ul>\n                                </div>\n                            </div><div class="job-boss-info">\n                            <div class="detail-figure">\n                                    <img src="https://img.bosszhipin.com/beijin/upload/avatar/20220201/607f1f3d68754fd0203107643f9fe240fefd1b0f1a47515d4c3cbc9cc8c86736476cef340ba87362_s.png?x-oss-process=image/resize,w_100,limit_0" alt="">\n                            </div>\n                            <h2 class="name">肖先生<i class="icon-vip"></i>\n                            </h2>\n                            <div class="boss-info-attr">\n                                科锐国际<em class="vdot">·</em>猎头顾问\n                                \n                            </div>\n                        </div>'),
        'name': '肖先生',
        'company': '科锐国际·猎头顾问',
        'url': 'https://www.zhipin.com/job_detail/00171a87bfe82e9e1HR42N68EFZX.html?lid=9kkPueb6I1i.search.27&securityId=VIVvRiBTKxbcA-d1COUwVzxBRPM1-CUptHvz-MJFhJgXh69MDXOUQdxOI-NHJF0DZHgORkJZyxKU9h9miNdH30Z0C492S2SqnD8LZUmTQJ2R7C0~&sessionId=',
        'date_added': datetime(2024, 6, 10, 6, 29, 45),
        'city': '成都',
        'activity': None
    },
    {
        'title': 'Python！开发（接受应届，线上面试）',
        'details': Markup(
            '<div class="job-sec-text">全程线上面试，薪资结构基础工资2~4个月年终奖+加班费:六险一金，全额基数缴纳社保公积金，合同四年起签<br>1、有嵌入式软件开发、通用软件开发、软件算法、媒体算法、音频算法、自动化控制制、精密装备开发与自动化等软件相关工作经验:<br>2、热爱编程，基础扎实，熟悉掌握但不限于JAVA/C++/C/Python/JS/HTML/GO等编程语言中的一种或数种，有良好的编程习惯;</div><div class="detail-section-item company-certification">\n                                <h3>认证资质<span class="company-certification-icon"></span></h3>\n                                <div class="certification-container">\n                                    <ul class="certification-tags">\n                                            <li>人力资源服务许可证</li>\n                                            <li>劳务派遣经营许可证</li>\n                                    </ul>\n                                </div>\n                                <div id="certification-content" class="certification-text" style="display: none;">\n                                    <h2 class="certification-title">资质说明</h2>\n                                    <ul class="certification-text">\n                                            <li>\n                                                <h2>人力资源服务许可证</h2>\n                                                <p>人力资源服务许可证是由国家人力资源与社会保障相关部门颁发，代表人才经纪人所在企业可以合法开展人力资源相关业务的资质证件。展示标签代表该企业已上传许可证并经由平台审核验证通过。</p>\n                                            </li>\n                                            <li>\n                                                <h2>劳务派遣经营许可证</h2>\n                                                <p>劳务派遣经营许可证是由国家人力资源与社会保障相关部门颁发，代表人才经纪人所在企业可以合法开展劳务派遣相关业务的资质证件。展示标签代表该企业已上传许可证并经由平台审核验证通过。</p>\n                                            </li>\n                                    </ul>\n                                </div>\n                            </div><div class="job-boss-info">\n                            <div class="detail-figure">\n                                    <img src="https://img.bosszhipin.com/beijin/upload/avatar/20220201/607f1f3d68754fd0203107643f9fe240fefd1b0f1a47515d4c3cbc9cc8c86736476cef340ba87362_s.png?x-oss-process=image/resize,w_100,limit_0" alt="">\n                            </div>\n                            <h2 class="name">肖先生<i class="icon-vip"></i>\n                            </h2>\n                            <div class="boss-info-attr">\n                                科锐国际<em class="vdot">·</em>猎头顾问\n                                \n                            </div>\n                        </div>'),
        'name': '肖先生',
        'company': '科锐国际·猎头顾问',
        'url': 'https://www.zhipin.com/job_detail/00171a87bfe82e9e1HR42N68EFZX.html?lid=9kkPueb6I1i.search.27&securityId=VIVvRiBTKxbcA-d1COUwVzxBRPM1-CUptHvz-MJFhJgXh69MDXOUQdxOI-NHJF0DZHgORkJZyxKU9h9miNdH30Z0C492S2SqnD8LZUmTQJ2R7C0~&sessionId=',
        'date_added': datetime(2024, 6, 10, 6, 29, 45),
        'city': '成都',
        'activity': None
    },
    {
        'title': 'Python！开发（接受应届，线上面试）',
        'details': Markup(
            '<div class="job-sec-text">全程线上面试，薪资结构基础工资2~4个月年终奖+加班费:六险一金，全额基数缴纳社保公积金，合同四年起签<br>1、有嵌入式软件开发、通用软件开发、软件算法、媒体算法、音频算法、自动化控制制、精密装备开发与自动化等软件相关工作经验:<br>2、热爱编程，基础扎实，熟悉掌握但不限于JAVA/C++/C/Python/JS/HTML/GO等编程语言中的一种或数种，有良好的编程习惯;</div><div class="detail-section-item company-certification">\n                                <h3>认证资质<span class="company-certification-icon"></span></h3>\n                                <div class="certification-container">\n                                    <ul class="certification-tags">\n                                            <li>人力资源服务许可证</li>\n                                            <li>劳务派遣经营许可证</li>\n                                    </ul>\n                                </div>\n                                <div id="certification-content" class="certification-text" style="display: none;">\n                                    <h2 class="certification-title">资质说明</h2>\n                                    <ul class="certification-text">\n                                            <li>\n                                                <h2>人力资源服务许可证</h2>\n                                                <p>人力资源服务许可证是由国家人力资源与社会保障相关部门颁发，代表人才经纪人所在企业可以合法开展人力资源相关业务的资质证件。展示标签代表该企业已上传许可证并经由平台审核验证通过。</p>\n                                            </li>\n                                            <li>\n                                                <h2>劳务派遣经营许可证</h2>\n                                                <p>劳务派遣经营许可证是由国家人力资源与社会保障相关部门颁发，代表人才经纪人所在企业可以合法开展劳务派遣相关业务的资质证件。展示标签代表该企业已上传许可证并经由平台审核验证通过。</p>\n                                            </li>\n                                    </ul>\n                                </div>\n                            </div><div class="job-boss-info">\n                            <div class="detail-figure">\n                                    <img src="https://img.bosszhipin.com/beijin/upload/avatar/20220201/607f1f3d68754fd0203107643f9fe240fefd1b0f1a47515d4c3cbc9cc8c86736476cef340ba87362_s.png?x-oss-process=image/resize,w_100,limit_0" alt="">\n                            </div>\n                            <h2 class="name">肖先生<i class="icon-vip"></i>\n                            </h2>\n                            <div class="boss-info-attr">\n                                科锐国际<em class="vdot">·</em>猎头顾问\n                                \n                            </div>\n                        </div>'),
        'name': '肖先生',
        'company': '科锐国际·猎头顾问',
        'url': 'https://www.zhipin.com/job_detail/00171a87bfe82e9e1HR42N68EFZX.html?lid=9kkPueb6I1i.search.27&securityId=VIVvRiBTKxbcA-d1COUwVzxBRPM1-CUptHvz-MJFhJgXh69MDXOUQdxOI-NHJF0DZHgORkJZyxKU9h9miNdH30Z0C492S2SqnD8LZUmTQJ2R7C0~&sessionId=',
        'date_added': datetime(2024, 6, 10, 6, 29, 45),
        'city': '成都',
        'activity': None
    },
    {
        'title': 'Python！开发（接受应届，线上面试）',
        'details': Markup(
            '<div class="job-sec-text">全程线上面试，薪资结构基础工资2~4个月年终奖+加班费:六险一金，全额基数缴纳社保公积金，合同四年起签<br>1、有嵌入式软件开发、通用软件开发、软件算法、媒体算法、音频算法、自动化控制制、精密装备开发与自动化等软件相关工作经验:<br>2、热爱编程，基础扎实，熟悉掌握但不限于JAVA/C++/C/Python/JS/HTML/GO等编程语言中的一种或数种，有良好的编程习惯;</div><div class="detail-section-item company-certification">\n                                <h3>认证资质<span class="company-certification-icon"></span></h3>\n                                <div class="certification-container">\n                                    <ul class="certification-tags">\n                                            <li>人力资源服务许可证</li>\n                                            <li>劳务派遣经营许可证</li>\n                                    </ul>\n                                </div>\n                                <div id="certification-content" class="certification-text" style="display: none;">\n                                    <h2 class="certification-title">资质说明</h2>\n                                    <ul class="certification-text">\n                                            <li>\n                                                <h2>人力资源服务许可证</h2>\n                                                <p>人力资源服务许可证是由国家人力资源与社会保障相关部门颁发，代表人才经纪人所在企业可以合法开展人力资源相关业务的资质证件。展示标签代表该企业已上传许可证并经由平台审核验证通过。</p>\n                                            </li>\n                                            <li>\n                                                <h2>劳务派遣经营许可证</h2>\n                                                <p>劳务派遣经营许可证是由国家人力资源与社会保障相关部门颁发，代表人才经纪人所在企业可以合法开展劳务派遣相关业务的资质证件。展示标签代表该企业已上传许可证并经由平台审核验证通过。</p>\n                                            </li>\n                                    </ul>\n                                </div>\n                            </div><div class="job-boss-info">\n                            <div class="detail-figure">\n                                    <img src="https://img.bosszhipin.com/beijin/upload/avatar/20220201/607f1f3d68754fd0203107643f9fe240fefd1b0f1a47515d4c3cbc9cc8c86736476cef340ba87362_s.png?x-oss-process=image/resize,w_100,limit_0" alt="">\n                            </div>\n                            <h2 class="name">肖先生<i class="icon-vip"></i>\n                            </h2>\n                            <div class="boss-info-attr">\n                                科锐国际<em class="vdot">·</em>猎头顾问\n                                \n                            </div>\n                        </div>'),
        'name': '肖先生',
        'company': '科锐国际·猎头顾问',
        'url': 'https://www.zhipin.com/job_detail/00171a87bfe82e9e1HR42N68EFZX.html?lid=9kkPueb6I1i.search.27&securityId=VIVvRiBTKxbcA-d1COUwVzxBRPM1-CUptHvz-MJFhJgXh69MDXOUQdxOI-NHJF0DZHgORkJZyxKU9h9miNdH30Z0C492S2SqnD8LZUmTQJ2R7C0~&sessionId=',
        'date_added': datetime(2024, 6, 10, 6, 29, 45),
        'city': '成都',
        'activity': None
    },

    # 其他职位数据...
]


@app.route('/', methods=['GET', 'POST'], )
def index():
    # conn = {
    #     'host': '127.0.0.1',
    #     'port': 3306,
    #     'user': 'root',
    #     'password': '111111',
    #     'database': 'datas'
    # }
    #
    # database = DatabaseProcessor(config=conn)
    # database.connect()
    #
    # filtered_listings = database.fetch_data_as_dict("job_opportunities")

    # keyword = None
    # if request.method == 'POST':
    #     keyword = request.form.get('keyword', '')
    #
    #     filtered_listings = [
    #         job for job in database.fetch_data_as_dict("job_opportunities") if
    #         keyword.lower() in job['title'].lower()
    #         or
    #         keyword.lower() in re.sub('<[^<]+?>', '',
    #                                   job['details']).lower()
    #     ]
    #
    # datas = []
    # for i in filtered_listings:
    #     modified_html = i["details"].replace('\\"', '"').replace('\n', '')
    #
    #     soup = BeautifulSoup(modified_html, 'html.parser')
    #     target_div = soup.find('div', class_='job-boss-info')
    #     if target_div:
    #         target_div.decompose()
    #
    #     modified_html = str(soup)
    #     i["details"] = modified_html
    #
    #     datas.append(i)

    return render_template('index.html', job_listings=job_listings, )


if __name__ == '__main__':
    app.run(debug=True)
