# coding: utf8

"""配置
"""

# User-Agent
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 6.3; WOW64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/40.0.2214.93 Safari/537.36"
)

# mongo config
DB_URI = "mongodb://127.0.0.1:27017"
# DB_URI = "mongodb://192.168.6.7:27017"
DB_NAME = "douban_group"

# 豆瓣小组URL
GROUP_LIST = [
    # 深圳租房团
    'https://www.douban.com/group/106955/',
    # 初来咋到（深圳租房）
    'https://www.douban.com/group/116930/',
    # 深圳租房
    'https://www.douban.com/group/551176/',
    # 深圳南山租房（个人房源免费推广）
    'https://www.douban.com/group/nanshanzufang/',
    # 深圳1号罗宝地铁沿线租房
    'https://www.douban.com/group/luobao1haoxian/',
    # 深圳租房★（个人房源免费推广）
    'https://www.douban.com/group/szsh/',
    # 深圳租房
    'https://www.douban.com/group/SZhouse/',
    # 深圳南山租房团
    'https://www.douban.com/group/498004/',
    # 深圳租房@南山/宝安租房
    'https://www.douban.com/group/637638/',
    # 深圳福田租房（个人房源免费推广）
    'https://www.douban.com/group/futianzufang/',
    # 深圳宝安租房（个人房源免费推广）
    'https://www.douban.com/group/baoanzufang/',
    # 深圳租房@福田租房
    'https://www.douban.com/group/637700/',
    # 深圳5号环中地铁沿线租房
    'https://www.douban.com/group/huanzhongxian/',
    # 深圳2号蛇口地铁沿线租房
    'https://www.douban.com/group/591624/',
    # 深圳7号地铁沿线租房
    'https://www.douban.com/group/615403/',
]

# 后缀
GROUP_SUFFIX = "discussion?start=%d"

# 抓取前多少页
MAX_PAGE = 5

# 匹配规则
RULES = {
    # 每个帖子项
    "topic_item": "//table[@class='olt']/tr",
    "url_list": "//table[@class='olt']/tr/td[@class='title']/a/@href",

    # 列表元素
    "title": "td[@class='title']/a/@title",
    "author": "td[@nowrap='nowrap'][1]/a/text()",
    "reply": "td[@nowrap='nowrap'][2]/text()",
    "last_reply_time": "td[@class='time']/text()",
    "url": "td[@class='title']/a/@href",

    # 帖子详情
    "detail_title_sm": "//td[@class='tablecc']/text()",

    # 完整标题
    "detail_title_lg": "//div[@id='content']/h1/text()",

    "create_time": "//span[@class='color-green']/text()",
    "detail_author": "//span[@class='from']/a/text()",
    # "content": "//div[@class='topic-content']/p/text()",
	"content": "//div[@class='topic-richtext']/p/text()",
}

INTERMEDIARY_KEYWORDS = [
    '拎包入住',
    '精装',
	'一流',
    '精装公寓',
	'豪华',
    '直租',
    '无中介费',
    '免中介费',
    '图很漂亮',
    '没什么杂物',
    '价格比市场价低',
    '价格私聊',
    '朝向南',
    '超高性价比',
    '多种选择',
    '多个价位',
    '真实房源',
    '实图实价',
    '弄虚作假',
    '那么漂亮',
    '超棒的',
    '这很棒',
    '心情愉悦',
    '微信同步',
    '家私齐全',
    '房东直租',
    '全包',
    '好房来袭',
    '低至',
    '超大',
    '精装修',
    '微信同号',
	'微信同',
	'微同步',
    '无.中.介.费',
    '真房真价',
    '高档小区',
    '宽大',
    '洼地',
    '配套齐全',
	'低于市场价',
	'好房子不等人',
	'走路上班',
	'备注一下豆瓣租房',
	'中介费用！',
	'一应俱全',
	'见链接',
	'原链接',
	'前定下',
	'如果不是',
	'豪宅',
	'不等人',
	'拍照技术',
	'我很喜欢',
	'我喜欢',
	'无任何中介费用',
    '空中花园',
    '零距离',
    '小花园',
    '仅需',
    '温馨',
    '24小时',
    '24h',
    '实拍',
    '随你实现',
    '分享',
    '来吧',
    '贵族',
    '应有尽有',
    '电梯房',
    'http'
    '精致',
    '诗和远方',
    '优惠多多',
    '速度联系',
    '梦！',
    '温馨舒适！',
    '仅限女生',
    '仅限女性',
]
# 豆瓣名称没有改，直接是豆友后面加一串数字的
# 只有标题，正文不写字的

PROXY_LIST_URLS = [
    'https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt',
    'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt'
]

# 并发数
POOL_SIZE = 20

# 监控周期(秒),默认10分钟
WATCH_INTERVAL = 10 * 60

# 重载代理周期
PROXY_INTERVAL = 30 * 60
