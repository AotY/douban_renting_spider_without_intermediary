# 说明
用于爬取`豆瓣住房小组`信息，同时过滤中介。<br/>
该项目Fork自https://github.com/kaito-kidd/douban-group-spider ，修改或添加了几个地方：
- 添加了通过关键词筛选去除中介帖子的功能
- 修改了正文页面content的xpath路径
- 修改了App.py中begin_page和end_page存在float类型问题
- 更新了requirements.txt

# 依赖
- `gevent`
- `pymongo`
- `requests`
- `lxml`
- `Flask`
<br/>

具体版本参见`requirements.txt`<br/>

# 特别说明
- 由于豆瓣有防抓机制，故此爬虫使用了代理爬取，防止被封IP。<br/>
- 可从网上收集代理IP，放在项目路径下`proxy_list.txt`。
- 每个一行，程序会自动加载，且可以自动定时加载新代理。<br/>
- 如果程序运行发现总是出现超时或者403，请更换`proxy_list.txt`下的代理。
- 可以从以下仓库中获取proxy （供参考）:
	- https://github.com/clarketm/proxy-list
	- https://github.com/a2u/free-proxy-list

# 使用
- 安装`MongoDB`，具体参考安装文档。
- 建议使用`virtualenv`环境<br/>
	`virtualenv douban_group`
	`source douban-group/bin/activate`
    `pip install -r requirements.txt`
- 启动MongoDB
	`mongo douban_group`
- 启动爬虫<br/>
    `nohup python spider.py >> douban_spider.log &`
- 启动web服务<br/>
    `nohup python app.py >> app.log &`
- 查看页面<br/>
    `http://localhost:5000`

# 配置
参数配置见`config.py`，例如`MongoDB地址`、`并发数`、`爬取页数`等。
