#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : config.py
# Author            : Qing Tao <qingtao12138@163.com>
# Date              : 16.03.2021
# Last Modified Date: 28.04.2022
# Last Modified By  : Qing Tao <qingtao12138@163.com>
# coding: utf8

"""配置
"""
import re
from requests.cookies import RequestsCookieJar


# User-Agent
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ",
    "Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ",
    "Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
    "Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 ",
    "Mozilla/5.0 (Windows NT 6.3; WOW64)",
    "AppleWebKit/537.36 (KHTML, like Gecko)",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
]

# cookies
"""
Cookie:
    gr_user_id=183cd2f9-0f18-4ab5-899b-4e1aebac2753;
    douban-profile-remind=1;
    bid=P85BvlsLhgY;
    __yadk_uid=lhMWBVwKjPzTqzt5wvoReZxl0ow8Al9t;
    push_noty_num=0;
    push_doumail_num=0;
    ll="118281";
    ap_v=0,6.0;
    dbcl2="135598293:urhKYy7ADqQ"
"""
jar = RequestsCookieJar()
jar.set("gr_user_id", "183cd2f9-0f18-4ab5-899b-4e1aebac2752")
jar.set("douban-profile-remind", "1")
jar.set("bid", "P85BvlsLhgY")
jar.set("push_noty_num", "0")
jar.set("push_doumail_num", "0")
jar.set("ll", "118281")
# jar.set("ct", "y")
jar.set("ap_v", "0,6.0")
jar.set("__yadk_uid", "lhMWBVwKjPzTqzt5wvoReZxl0ow8Al9t")
jar.set("dbcl2", "135598293:urhKYy7ADqQ")

jar2 = jar.copy()
jar2.set("gr_user_id", "182cd1f8-0f18-4ab4-899b-4e1aebac2753")

jar3 = jar.copy()
# jar3.set("__yadk_uid", "lhMWBVwKjPzTazt5wvoReZxl0ow8Al9e")
jar3.set("gr_user_id", "183ce2f8-0f18-4ab4-899b-5e1aebac2753")

jar4 = jar.copy()
jar4.set("gr_user_id", "183cd2f9-0f18-4ab5-897b-4e1aebac2753")

jar5 = jar.copy()
# jar5.set("__yadk_uid", "lhMWVvwKjPzTazt5wvoReZxl0ow8Al9e")
jar5.set("gr_user_id", "183cd2f8-0e18-4ab4-899b-4e1abbac2753")

JARS = [jar, jar2, jar3, jar4, jar5]


# mongo config
DB_URI = "mongodb://localhost:27017"
# DB_URI = "mongodb://192.168.6.7:27017"
DB_NAME = "douban_group"
DB_TLS_CA_FILE = "/Users/LeonTao/mongodb-macos-x86_64-4.2.12/ssl/ca.pem"
DB_TLS_CERTIFICATE_KEY_FILE = "/Users/LeonTao/mongodb-macos-x86_64-4.2.12/ssl/client.pem"

# 并发数
# POOL_SIZE = 20
POOL_SIZE = 5
# POOL_SIZE = 1

# 监控周期(秒),默认10分钟
WATCH_INTERVAL = 10 * 60

# 重载代理周期
PROXY_INTERVAL = 30 * 60

# 抓取前多少页
# MAX_PAGE = 5
MAX_PAGE = 2

# 每页多少条记录
PAGE_SIZE = 25
# PAGE_SIZE = 10

# 睡眠时间
SLEEP_TIME = 2.0
# SLEEP_TIME = 4.0

# PROXY_LIST_URLS = [
#     'https://github.com/clarketm/proxy-list/blob/master/proxy-list-raw.txt',
#     'https://github.com/ShiftyTR/Proxy-List/blob/master/proxy.txt',
#     'https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt'
# ]
UPDATED_PROXY = "127.0.0.1:4780"
UPDATED_PROXIES_PATH = "./data/updated_proxies.txt"
UPDATED_PROXIES = [
]


# 小组列表后缀
GROUP_SUFFIX = "discussion?start=%d"

# 豆瓣小组URL
GROUP_LIST = [
    # 深圳租房团
    'https://www.douban.com/group/106955/',
    # 初来咋到（深圳租房）
    'https://www.douban.com/group/116930/',
    # 深圳租房
    'https://www.douban.com/group/551176/',
	'https://www.douban.com/group/637628/',
	'https://www.douban.com/group/SZhouse/',
    # 福田租房
    'https://www.douban.com/group/futianzufang/',
    # 南山租房
    'https://www.douban.com/group/nanshanzufang/',
	'https://www.douban.com/group/637638/',
    'https://www.douban.com/group/591624/',
    # 深圳南山租房团
    'https://www.douban.com/group/498004/',
	# 罗湖租房
	'https://www.douban.com/group/592828/',
	# 宝安租房
	'https://www.douban.com/group/baoanzufang/',
    'https://www.douban.com/group/637700/',
    'https://www.douban.com/group/luobao1haoxian/',
	# 龙华租房
	'https://www.douban.com/group/longhuazufang/',
	#  整租
	'https://www.douban.com/group/537027/',
    # 落户租房
    'https://www.douban.com/group/592828/',
    # 福田租房|深圳福田租房
    'https://www.douban.com/group/luohuzufang/',
    # 深圳租房/ 福田/龙岗
    'https://www.douban.com/group/592144/',
    # 深圳转租
    'https://www.douban.com/group/609271/'
]

# 豆瓣名称没有改，直接是豆友后面加一串数字的
# 只有标题，正文不写字的

# 匹配规则
RULES = {
    # 列表元素
    "topic_item": "//table[@class='olt']/tr",
    # url列表
    "url_list": "//table[@class='olt']/tr/td[@class='title']/a/@href",
    # title 列表
    "title_list": "//table[@class='olt']/tr/td[@class='title']/a/@title",
    # TODO created_time
    "created_time": "td[@class='time']/text()",
    # TODO title
    "title": "td[@class='title']/a/@title",
    # "author": "td[@nowrap='nowrap'][1]/a/text()",
    # "reply": "td[@nowrap='nowrap'][2]/text()",
    "replied_count": "td[contains(@class, 'r-count')]/text()",
    # "last_replied_time": "td[@class='time']/text()", # 列表页面上的最后更新时间没有根据最后回复时间进行更新
    "url": "td[@class='title']/a/@href",

    # "detail_title_sm": "//td[@class='tablecc']/text()",
    # "detail_title_lg": "//div[@id='article']/h1/text()",

    # 正文
	"content": "//*[@id='link-report']/div/div/p/text()",
    # 正文标题
    "content_title": "//div[@class='article']/h1/text()",
    # 创建时间
    "content_created_time": "//div[@class='article']/div[contains(@class, 'topic-content')]/div[@class='topic-doc']/h3/span[contains(@class, 'create-time')]/text()",
    # 发布作者
    "content_author": "//span[@class='from']/a/text()",
    # 回复列表
    "content_replied_list": "//ul[@class='topic-reply']/li[contains(@class, 'reply-item')]/div[contains(@class, 'reply-doc')]/p/text()",
    # 回复时间列表
    "content_replied_time_list": "//ul[@class='topic-reply']/li[contains(@class, 'reply-item')]/div[contains(@class, 'reply-doc')]/div[@class='bg-img-green']/h4/span[@class='pubtime']/text()",
}

# 过滤的正文最小字数
FILTERED_CONTENT_MIN_LEN = 5
FILTERED_CONTENT_MAX_LEN = 500
FILTERED_THRILL_MAX_COUNT = 4

# 过滤正则列表

FILTERED_RES = [
    re.compile(r"求[^\s]{0,2}租|可[^\s]{0,5}短租"),
    re.compile(r"包[^\s]{0,2}入[^\s]{0,2}住|(?:家[电私具]|配套)齐全|拎[\^s]{0,2}包[^\s]{0,2}入|"
               r"拎包住|可拎包入"),
    re.compile(r"[无免][^\s]{0,2}[管中][^\s]{0,2}[介理][^\s]{0,2}费|"
               r"[无没][^\s]{0,3}任何[^\s]{0,3}费用|[都均]免费|无中介"),
    re.compile(r"[vV][xX][^\s]{0,2}同|[加+][vV微]|[vV微]同|[vV微]信同|同[vV微]"),
    re.compile(r"限女[生性]|小[姐妹][姐妹]|网红|白领|女[生性]合租|公务员|"
               r"[找只全][^\s]{0,3}女[性生]"),
    re.compile(r"[阳采]光[^\s]{0,2}[特超][^\s]{0,2}好|光好大|光通风|"
               r"大(?:阳台|房间)|电梯房|可做饭|吃喝玩乐|素质好|"
               r"(?:空中|[大小])花园|(?:采光|户型|通风)[佳好]"),
    re.compile(r"急！|！急|秒杀|特价|🔥|降价|性价比[^\s]{0,3}[超很非]|[0-9]{3,4}[!！]|"
               r"✨|🈴️|白菜价|价格美丽|值得你|大主卧|大单间|阳光[^\s]{0,2}卧|车位充足"),
    re.compile(r"(?:拒绝|没有|无)[^\s]{0,2}(?:潮湿|握手|合租|隔断|蟑螂)|非(?:城中村|农民房)"),
    re.compile(r"[hH][tT][tT][pP]|[见原][链连]接"),
    re.compile(r"真实房源|(?:业主|房东|个人)直租|一手房东|中介勿扰"),
    re.compile(
        r"精装|一流|豪华|(?:图|那么|非常)[^\s]{0,2}漂亮|超棒|愉悦|很棒|超大|高档|宽大|"
        r"洼地|豪宅|温馨|精致|梦[！幻]|品质|高端|大气|一流|无敌|黄金|"
        r"忍痛|依山|傍水|香港|非常好|相当好|均有|如题|酒店|舒适|诗和|远方|"
        r"贵族|来吧|实拍|仅需|很喜欢|不等人|俱全|巨全|好房子|低至|低到|全包|"
        r"超高|杂物|心情|来袭|都市|骚扰|急转|视野|捡漏|优雅|辐射|一体化|一级棒|"
        r"热闹|都懂|靓房|大型|慵懒|独门|超好|大飘窗|免佣|急租|珍稀|高要求|手慢无|"
        r"绝美|绝佳"
    ),
    re.compile(r"(?:视频|[vV微]信|预约)看房|(?:提前|需)预约|"
               r"(?:看房|价格)(?:私聊|方便|联系)|(?:微信|电话|详情)咨询|"
               r"咨询[^\s]{0,2}加[vV微]|速度[^\s]{0,2}联系|随时(?:看房|入住)"),
    re.compile(r"回[家乡去]发展|[实真][房图][实真]价|尊重(?:他人|室友)|从来不用|"
               r"(?:不限|可养)宠物|优惠多多|跳转原文"
               r"应有尽有|随你(?:实现|安排)|零距离|拍照技术|如果不是|低于市场价|"
               r"(?:走路|步行)上班|多[个种](?:价位|选择)|弄虚作假|地铁周边"),
    re.compile(r"(?:24|二十四)(?:小时|h)"),
    re.compile(r"备注[^\s]{0,2}豆瓣租房"),
]

# 过滤关键词
# FILTERED_KEYWORDS = [
#     '拎包入住',
#     '精装',
# 	'一流',
#     '精装公寓',
# 	'豪华',
#     '直租',
#     '无中介费',
#     '免中介费',
#     '图很漂亮',
#     '没什么杂物',
#     '价格比市场价低',
#     '价格私聊',
#     '朝向南',
#     '超高性价比',
#     '多种选择',
#     '多个价位',
#     '真实房源',
#     '实图实价',
#     '弄虚作假',
#     '那么漂亮',
#     '超棒的',
#     '这很棒',
#     '心情愉悦',
#     '微信同步',
# 	'微信同',
#     '家私齐全',
#     '房东直租',
#     '全包',
#     '好房来袭',
#     '低至',
#     '超大',
#     '精装修',
# 	'微同步',
#     '无.中.介.费',
#     '真房真价',
#     '高档小区',
#     '宽大',
#     '洼地',
#     '配套齐全',
# 	'低于市场价',
# 	'好房子不等人',
# 	'走路上班',
# 	'备注一下豆瓣租房',
# 	'备注豆瓣租房',
# 	'中介费用！',
# 	'一应俱全',
# 	'见链接',
# 	'原链接',
# 	'前定下',
# 	'如果不是',
# 	'豪宅',
# 	'不等人',
# 	'拍照技术',
# 	'我很喜欢',
# 	'我喜欢',
# 	'无任何中介费用',
#     '空中花园',
#     '零距离',
#     '小花园',
#     '仅需',
#     '温馨',
#     '24小时',
#     '24h',
#     '实拍',
#     '随你实现',
#     '分享',
#     '来吧',
#     '贵族',
#     '应有尽有',
#     '电梯房',
#     'http'
#     '精致',
#     '诗和远方',
#     '优惠多多',
#     '速度联系',
#     '梦！',
#     '温馨舒适！',
#     '限女生',
#     '限女性',
#     '白领',
#     '酒店',
#     'VX同步',
#     'VX',
#     'vx',
#     'Ⅴ同',
#     'v同',
#     '微同',
#     "！急",
#     "秒杀",
#     "特价",
#     "温馨",
#     "女生合租",
#     "求租",
#     "品质",
#     "可短租",
#     "咨询加微信",
#     "大阳台",
#     "可做饭",
#     "微信看房",
#     "高端",
#     "一流",
#     "中介勿扰",
#     "拒绝潮湿",
#     "拒绝握手楼",
#     "拒绝合租",
#     "看房方便",
#     "阳光特好",
#     "看房联系",
#     "采光精装",
#     "黄金",
#     "加微",
#     "无隔断",
#     "预约看房",
#     "精装家电",
#     "需预约",
#     "可养宠物",
#     "无敌",
#     "从来不用",
#     "尊重他人",
#     "详情咨询",
#     "同微",
#     "回家发展",
#     "采光通风好",
#     "非城中村",
#     "非农民房",
#     "降价",
#     "光好大",
#     "详情",
#     "提前预约",
#     "微信咨询",
#     "均有",
#     "拎包可入",
#     "如题",
#     "网红",
#     "均免费",
#     "+v",
#     "+V",
#     "求短租",
#     "小姐姐",
#     "真图实价",
#     "忍痛转租",
#     "没有任何费用",
#     "没任何费用",
#     "依山傍水",
#     "面向香港",
#     "看房私聊"
#     "非常好",
#     "电梯房",
#     "视频看房",
#     "公务员"
# ]
