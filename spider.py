# usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : spider.py
# Author            : Qing Tao <qingtao12138@163.com>
# Date              : 17.03.2021
# Last Modified Date: 29.04.2022
# Last Modified By  : Qing Tao <qingtao12138@163.com>
# coding: utf8

"""
豆瓣小组爬虫
"""

from gevent import monkey
monkey.patch_all()

import time
import random
import logging
import subprocess
from datetime import datetime

import gevent
import requests
from gevent.pool import Pool
from gevent.queue import Queue
from lxml import etree
from db_client import DBClient

from config import (
    GROUP_LIST, GROUP_SUFFIX, USER_AGENTS,
    POOL_SIZE, RULES, MAX_PAGE, WATCH_INTERVAL,
    PROXY_INTERVAL, SLEEP_TIME, PAGE_SIZE,
    FILTERED_CONTENT_MAX_LEN, FILTERED_CONTENT_MIN_LEN,
    FILTERED_THRILL_MAX_COUNT, FILTERED_RES, JARS,
    UPDATED_PROXIES_PATH, UPDATED_PROXIES, UPDATED_PROXY,
    MONEY_RE, MAX_MONEY, MIN_MONEY
)

from utils import Timer, ProxyManager

"""
1. 爬取列表页面
 - 获取页面标题，根据标题进行一定的过滤
 - 得到满足过滤条件的url
 - 这里感觉需要根据列表item的回应数据来判断是否有更新（因为发现在帖子
   里面的回复时间有更新，但是列表页面上的时间没有更新），有点奇怪

2. 爬取详情页面
 - 获取文本正文，同样，进行关键词过滤
 - 更新正文内容
"""


def get_logger(name):
    """logger
    """
    default_logger = logging.getLogger(name)
    default_logger.setLevel(logging.DEBUG)
    stream = logging.StreamHandler()
    stream.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
    stream.setFormatter(formatter)
    default_logger.addHandler(stream)
    return default_logger


logger = get_logger("douban_spider")


class HTTPError(Exception):

    """ HTTP状态码不是200异常 """

    def __init__(self, status_code, url):
        self.status_code = status_code
        self.url = url

    def __str__(self):
        return "%s HTTP %s" % (self.url, self.status_code)


class URLFetchError(Exception):

    """ HTTP请求结果为空异常 """

    def __init__(self, url):
        self.url = url

    def __str__(self):
        return "%s fetch failed! Cannot get a invalid proxy in most case." % self.self.url


class DoubanSpider(DBClient):

    """" 豆瓣爬虫 """

    def __init__(self, proxy_manager=None):
        # self.result_page = self.db.result_page
        # self.result_topic = self.db.result_topic
        # self.cache = self.db.cache_page
        # logger.info(self.result_page)
        # logger.info(self.result_topic)
        # logger.info(self.cache)

        # 用于存储结果的mongodb表
        self.result_all = self.db.result_all
        self.cache = self.db.cache_all

        # 由于大量的无效代理
        self.cache.delete_many({})

        self.group_list = GROUP_LIST
        self.rules = RULES
        self.interval = WATCH_INTERVAL

        self.pool = Pool(size=POOL_SIZE)

        # 列表队列
        self.page_queue = Queue()

        # 页面详情队列
        self.topic_queue = Queue()

        self.proxy_manager = proxy_manager
        # self.proxy_manager = None

    def _fetech(self, url, timeout=10, retury_num=10):
        """发起HTTP请求

        @url, str, URL
        @timeout, int, 超时时间
        @retury_num, int, 重试次数
        """
        kwargs = {
            "headers": {
                "User-Agent": USER_AGENTS[random.randint(0, len(USER_AGENTS) - 1)],
                "Referer": "https://www.douban.com/group/explore",
                "Host": "www.douban.com"
            },
        }
        kwargs["timeout"] = timeout
        resp = None
        proxy = None
        for i in range(retury_num):
            try:
                # 是否启动代理
                if self.proxy_manager is not None:
                    proxy = self.proxy_manager.get_proxy()
                    kwargs["proxies"] = {
                        "http": 'http://%s' % proxy,
                        "https": 'http://%s' % proxy
                        # "https": 'https://%s' % proxy
                    }
                # resp = requests.get(url, **kwargs)
                resp = requests.get(url, cookies=JARS[random.randint(0, 4)], **kwargs)
                if resp.status_code != 200:
                    raise HTTPError(resp.status_code, url)
                break
            except Exception as exc:
                logger.warning("%s %s %d failed!\n%s", proxy, url, i, str(exc))
                if self.proxy_manager is not None:
                    self.proxy_manager.remove(proxy)
                time.sleep(SLEEP_TIME)
                continue

        if resp is None:
            logger.error("cannot get a valid proxy in most case.")
            # raise URLFetchError(url)
            return None

        # bytes to str
        return resp.content.decode('utf-8')

    def _extract(self, regx, body, multi=False):
        """解析元素,xpath语法

        @regx, str, 解析表达式
        @body, str or element, 网页源码或元素
        @multi, bool, 是否取多个
        """
        if isinstance(body, str):
            body = etree.HTML(body)

        res = body.xpath(regx)
        if res is None:
            return None
        # 如果返回的是列表
        if multi:
            return res
        else:
            if len(res) == 0:
                return None
            else:
                return res[0]
        # return res[0] if res else None

    def run(self):
        """run
        """
        all_greenlet = []

        # 定时爬取，小组列表
        for group_url in self.group_list:
            # timer = Timer(random.randint(0, self.interval), self.interval)
            timer = Timer(random.randint(0, 3), self.interval)
            greenlet = gevent.spawn(
                timer.run, self._init_page_tasks, group_url)
            all_greenlet.append(greenlet)

        # 生产 & 消费
        # 帖子列表
        all_greenlet.append(gevent.spawn(self._page_loop))

        # 帖子详情
        all_greenlet.append(gevent.spawn(self._topic_loop))

        # 重载代理，10分
        proxy_timer = Timer(PROXY_INTERVAL, PROXY_INTERVAL)
        all_greenlet.append(
            gevent.spawn(proxy_timer.run(self.reload_proxies)))

        gevent.joinall(all_greenlet)

    def reload_proxies(self):
        """重新加载代理
        """
        # 由于大量的无效代理
        # self.cache.delete_many({})
        # 重新执行拉去代理列表脚本
        # subprocess.call(['sh', './update_proxies.sh'])
        subprocess.run("sh ./update_proxies.sh", shell=True, check=True)
        self.proxy_manager.reload_proxies()

    def _init_page_tasks(self, group_url):
        """初始化页面任务

        @group_url, str, 小组URL
        """
        for i in range(MAX_PAGE):
            url_suffix = GROUP_SUFFIX % (i * PAGE_SIZE)
            url = "%s%s" % (group_url, url_suffix)
            self.page_queue.put(url)
            logger.info("page queue adding: %s" % url)

    def _page_loop(self):
        """page loop 循环列表页面
        """
        while True:
            # Remove and return an item from the queue
            page_url = self.page_queue.get(block=True)
            self.pool.spawn(self._crawl_page, page_url)
            gevent.sleep(SLEEP_TIME)

    def _topic_loop(self):
        """topic loop
        """
        while 1:
            # Remove and return an item from the queue
            # block if necessary until an item is available.
            topic_url = self.topic_queue.get(block=True)
            self.pool.spawn(self._crawl_topic_detail, topic_url)

    def _crawl_page(self, url):
        """爬取帖子列表

        @url, str, 当前页面URL
        """
        logger.info("processing page url: %s" % url)
        html = self._fetech(url)
        if html is None:
            self.page_queue.put(url)
            return
        body = etree.HTML(html)
        titles = self._extract(self.rules["title_list"], body, multi=True)
        titles = [t.strip() for t in titles]
        # first one is column names
        topics = self._extract(self.rules["topic_item"], body, multi=True)[1:]
        assert(len(titles) == len(topics)), "titles and items are not equal in size."
        # topic_urls = self._extract(self.rules["url_list"], body, multi=True)
        logger.info("%s has %d topics.", url, len(topics))
        # logger.info("titles: {}".format(titles))
        # filtered_topics = [(titles[i], topics[i]) for i in range(len(titles)) \
        #                    if not self._filter_by_keywords(titles[i])]
        filtered_topics = [topics[i] for i in range(len(titles)) \
                           if not self._filter_by_keywords(titles[i])]
        logger.info("got %d topics after filtered.", len(filtered_topics))

        filtered_titles, filtered_topic_urls, \
            filtered_replied_count, filtered_created_times = \
            list(), list(), list(), list()
        for topic in filtered_topics:
            topic_url = self._extract(self.rules["url"], topic, multi=False)
            if topic_url is None:
                logger.error("filtered_topic has empty topic url: %s" % url)
                continue
            replied_count = self._extract(self.rules["replied_count"], topic, multi=False)
            if replied_count is None:
                replied_count = 0
            else:
                if not replied_count.isnumeric():
                    logger.error("replied count is not numeric: %s" % replied_count)
                    continue
                replied_count = int(replied_count)

            created_time = self._extract(self.rules["created_time"], topic, multi=False)
            if created_time is None:
                logger.error("filtered_topic has empty topic created_time: %s" % url)
                continue
            created_time = str(datetime.now().year) + "-" + created_time

            title = self._extract(self.rules["title"], topic, multi=False)
            if title is None:
                logger.error("filtered_topic has empty topic title: %s" % url)
                continue

            logger.info("url: %s, replied_count: %d, created_time: %s, title: %s", \
                        topic_url, replied_count, created_time, title)

            # 添加到过滤后的列表
            filtered_topic_urls.append(topic_url)
            filtered_replied_count.append(replied_count)
            filtered_created_times.append(created_time)
            filtered_titles.append(title)

        # updated_urls = self._diff_urls(topic_urls)
        # 找出新增的帖子，根据url和帖子回复个数，包含url和回复个数
        updated_topics = self._diff_topics(
            filtered_topic_urls,
            filtered_replied_count,
            filtered_created_times,
            filtered_titles
        )

        if len(updated_topics) == 0:
            logger.info("%s no update ...", url)
            return

        logger.info("%s new add : %d", url, len(updated_topics))

        # topic_list = self._extract(self.rules["topic_item"], html, multi=True)

        # 获取每个topic的简要的信息
        # topics = self._get_page_info(topic_list)
        # 过滤,找到新增的和之前的帖子
        # new_topics, old_topics = self._filter_topics(topics, updated_urls)

        # 保存每页的信息
        # self.result_page.insert(new_topics)

        # 更新老帖子的时间和回复数
        # self._update_old_topics(old_topics)

        # 初始化帖子任务
        updated_urls = [url for (url, _, _, _) in updated_topics]

        self._init_topic_tasks(updated_urls)

        # 将更新的列表也加入到数据库
        self._update_topics(updated_topics)

        # 更新缓存
        self._update_cache(updated_topics)
        # self._update_cache(updated_urls)

    # def _get_page_info(self, topic_list):
    #     """获取每一页的帖子基本信息

    #     @topic_list, list, 当前页的帖子项
    #     """
    #     topics = []
    #     # 第一行是标题头,舍掉
    #     for topic_item in topic_list[1:]:
    #         topic = {}
    #         topic["title"] = self._extract(self.rules["title"], topic_item)
    #         topic["author"] = self._extract(self.rules["author"], topic_item)
    #         topic["reply"] = self._extract(self.rules["reply"], topic_item) or 0
    #         topic["last_reply_time"] = self._extract(
    #             self.rules["last_reply_time"], topic_item)

    #         topic["url"] = self._extract(self.rules["url"], topic_item)
    #         now = time.time()
    #         topic["got_time"] = now
    #         topic["last_update_time"] = now
    #         # print('page info topic: {}'.format(topic))
    #         if not self._filter_by_keywords(topic['author'], topic['title'], None):
    #             topics.append(topic)
    #     return topics

    @staticmethod
    def _filter_topics(topics, updated_urls):
        """过滤帖子,找出新增的和老的帖子

        @topics, list, 当前页所有帖子信息
        @updated_urls, list, 新增的帖子URL
        """
        new_topics, old_topics = [], []
        for topic in topics:
            if topic["url"] in updated_urls:
                new_topics.append(topic)
            else:
                old_topics.append(topic)
        return new_topics, old_topics

    def _diff_topics(self,
                     topic_urls,
                     replied_counts,
                     created_times,
                     titles):
        """过滤重复帖子URL

        @topic_urls, list, 当前页URL列表
        @replied_counts, list, 当前帖子回复数列表
        @created_times, list, 帖子时间列表
        @titles, list, 帖子标题列表
        """
        logger.info("topic_urls size: %d"  % len(topic_urls))
        # 与缓存比较
        cached_dict = {}
        cursor = self.cache.find()
        for item in cursor:
            cached_url = item["url"]
            cached_replied_count = item["replied_count"]
            cached_dict[cached_url] = cached_replied_count

        logger.info("cached url size: %d" % len(cached_dict))
        # 找出新增的URL，通过对比新增的url和帖子回复个数
        updated_topics = [
            (url, count, ct, title) for (url, count, ct, title) in \
            zip(topic_urls, replied_counts, created_times, titles) \
            if url not in cached_dict or count != cached_dict[url]
        ]
        logger.info("updated topic size: %d" % len(updated_topics))
        return updated_topics

    def _diff_urls(self, topic_urls):
        """过滤重复帖子URL

        @topic_urls, list, 当前页所有帖子URL
        """
        print("topic_urls: ", len(topic_urls))
        # 与缓存比较
        cache_urls = []
        cursor = self.cache.find()
        for item in cursor:
            cache_urls.extend(item["urls"])
        print("cache_urls: ", len(cache_urls))
        # 找出新增的URL
        updated_urls = list(set(topic_urls) - set(cache_urls))
        return updated_urls

    # def _update_old_topics(self, old_topics):
    #     """更新老帖子的信息,标题,回应时间和回复数量

    #     @old_topics, list, 老帖子列表
    #     """
    #     for topic in old_topics:
    #         new_info = {
    #             "title": topic["title"],
    #             "reply": topic["reply"],
    #             "last_reply_time": topic["last_reply_time"],
    #             "last_update_time": time.time()
    #         }
    #         self.result_page.update(
    #             {"url": topic["url"]},
    #             {"$set": new_info}
    #         )
    #         logger.info("%s updated ...", topic["url"])

    def _init_topic_tasks(self, topic_urls):
        """初始化帖子任务

        @topic_urls, list, 当前页面帖子的URL
        """
        for url in topic_urls:
            self.topic_queue.put(url)

    def _update_topics(self, updated_topics):
        """更新缓存

        @updated_topics, list, 新增的帖子信息
        """
        for (url, count, ct, title) in updated_topics:
            info = {
                "url": url,
                "replied_count": count,
                "created_time": ct,
                "title": title,
                "content": title,
                "last_replied_time": ct,
                "got_time": time.time(),
            }
            self.result_all.update_one(
                {"url": info["url"]}, # filter
                {"$set": info}, # update
                upsert=True # upsert
            )
    def _update_cache(self, updated_urls):
        """更新缓存

        @updated_urls, list, 新增的帖子URL
        """
        # self.cache.insert(
        #     {"got_time": time.time(), "urls": updated_urls})
        for (url, count, _, _) in updated_urls:
            info = {
                "url": url,
                "replied_count": count,
                "got_time": time.time()
            }
            # self.cache.update(
            self.cache.update_one(
                {"url": info["url"]}, # filter
                {"$set": info}, # update
                upsert=True # upsert
            )

    def _crawl_topic_detail(self, url):
        """爬取每个帖子的详情

        @url, str, 每个帖子的URL
        """
        logger.info("processing topic: %s", url)
        html = self._fetech(url)
        if html is None:
            self.topic_queue.put(url)
            return
        body = etree.HTML(html)
        if body is None:
            logger.error("got empty body: %s" % url)
            return

        # 获取每一页的信息
        topic = self._get_topic_info(body, url)

        if not topic:
            return

        topic["url"] = url
        topic["got_time"] = time.time()

        # 不存在 & 保存帖子的信息
        # if self.result_topic.find_one({"url": url}):
        #     return

        # self.result_topic.insert(topic)
        # self.result_all.update(
        self.result_all.update_one(
            {"url": topic["url"]}, # filter
            {"$set": topic}, # update
            upsert=True # upsert
        )

    def _get_topic_info(self, body, url):
        """获取帖子详情

        @html, str, 页面
        """
        # if "机器人" in html:
        #    logger.warn("%s 403.html", url)
        #    return None

        topic = {}
        # title = self._extract(self.rules["detail_title_sm"], html) \
        #     or self._extract(self.rules["detail_title_lg"], html)
        title = self._extract(self.rules["content_title"], body, multi=False)
        author = self._extract(self.rules["content_author"], body, multi=False)
        created_time = self._extract(self.rules["content_created_time"], body, multi=False)
        if title is None or author is None or created_time is None:
            logger.error("got empty title or author or created_time: %s" % url)
            return None

        content = self._extract(self.rules["content"], body, multi=True)
        content = ' '.join([c.strip() for c in content])
        if self._filter_by_keywords(content):
            return None

        #  回复时间列表
        replied_times = self._extract(self.rules["content_replied_time_list"], body, multi=True)
        replied_count = len(replied_times)

        topic["content"] = content
        topic["title"] = title.strip()
        topic["author"] = author.strip()
        topic["created_time"] = created_time.strip()
        topic["replied_count"] = replied_count
        topic["last_replied_time"] = replied_times[-1] if replied_count > 0 else topic["created_time"]

        return topic

    def _filter_by_keywords(self, content):
        """根据文本内容判断是否要进行过滤，加上一些启发式规则"""
        # logger.info("content: %s", content)

        if content is None:
            return True

        # is_filtered = False
        content_len = len(content)
        if content_len < FILTERED_CONTENT_MIN_LEN or content_len > FILTERED_CONTENT_MAX_LEN:
            logger.info("%s filtered by length.", content)
            return True

        # 感叹号个数，激动次数
        num_thrills = content.count("!") + content.count("！")
        if num_thrills > FILTERED_THRILL_MAX_COUNT:
            logger.info("%s filtered by thrill count.", content)
            return True

        # 金额过滤
        money_matchs = MONEY_RE.findall(content)
        if len(money_matchs) > 0 and len(money_matchs[0]) > 0:
            for money_ma in money_matchs:
                money = int(money_ma)
                if money < MIN_MONEY or money > MAX_MONEY:
                    logger.info("%s filtered by money range.", content)
                    return True

        # 关键词过滤
        for reg in FILTERED_RES:
            matches = reg.findall(content)
            if len(matches) != 0 and len(matches[0]) > 0:
                logger.info("%s filtered by keywords.", content)
                return True
        logger.info("content: %s", content)
        return False

    # def _filter_by_keywords(self, author, title, content=None):
    #     """根据关键词, 内容和豆瓣用户名等判断是否为中介"""
    #     full_text = title
    #     if content is not None:
    #         if len(content) < 20 or len(content) > 500 or content == title:
    #              return True
    #         full_text += content

    #     if author.startswith('豆友') or author.find('直租') != -1:
    #         return True

    #     exclamation_count = full_text.count('!') + full_text.count('！')
    #     if exclamation_count >= 3:
    #          return True

    #     for kw in FILTERED_KEYWORDS:
    #         if full_text.find(kw) != -1:
    #             return True
    #     return False


""" main """
def main():
    # proxy_manager = ProxyManager(interval_per_ip=30, is_single=True)
    # is_init_success = proxy_manager.init_proxies(UPDATED_PROXY)

    proxy_manager = ProxyManager(interval_per_ip=30, is_single=False)
    is_init_success = proxy_manager.init_proxies(UPDATED_PROXIES_PATH)

    # is_init_success = proxy_manager.init_proxies(UPDATED_PROXIES)
    if not is_init_success:
        logger.error("Init proxies failed, got a invalid proxies, please running `sh ./update_proxies.sh`.")
        # logger.error("Init proxies failed, got a invalid proxies.")
        exit(0)
    spider = DoubanSpider(proxy_manager)
    spider.run()


if __name__ == "__main__":
    main()
