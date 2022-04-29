#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : app.py
# Author            : Qing Tao <qingtao12138@163.com>
# Date              : 20.03.2022
# Last Modified Date: 27.03.2022
# Last Modified By  : Qing Tao <qingtao12138@163.com>
# coding: utf8

import re
import math

from flask import Flask, request, render_template
from db_client import DBClient

app = Flask(__name__)
app.debug = True

# db & collection
db = DBClient().db
# topic_collection = db.result_topic # 详情页面
# page_collection = db.result_page # 列表页面，有最后更新时间

# 这里需要给他整合一下，
# 只保留一个collection，里面既有 create_time, 又有
# last_replied_time
result_collection = db.result_all

@app.route("/", methods=["GET", "POST"])
def index():
    """index
    """
    cpage = int(request.form.get("cpage", 1))
    psize = int(request.form.get("psize", 50))
    keyword = request.form.get("keyword", "")
    is_order_replied_time = int(request.form.get("is_order_replied_time", 0))

    # 按更新时间排序
    collection = result_collection
    if is_order_replied_time:
        orderby = "last_replied_time"
    else: # 按创建时间排序
        orderby = "created_time"

    where = {}
    if keyword:
        regx = re.compile(".*%s.*" % keyword, re.IGNORECASE)
        where["title"] = {"$regex": regx}
        where["content"] = {"$regex": regx}

    # count
    count = collection.find(where).count()

    # page
    page = Page(cpage, psize, count)

    # get data from db
    topics = collection.find(where).sort(
        [(orderby, -1)]).skip(page.start).limit(page.end)
    print('page: {}, {}, {}, {}, {}'.format(
        page.cpage, page.psize, page.count, page.begin_page, page.end_page))
    return render_template(
        "index.html",
        topics=topics,
        is_order_replied_time=is_order_replied_time,
        keyword=keyword,
        count=count,
        page=page
    )


class Page(object):

    """ page info"""

    def __init__(self, cpage, psize, count):
        self.cpage = cpage
        self.psize = psize
        self.count = count
        self.max_page = int((count + psize - 1) / psize)
        self.max_page = max(self.max_page, 1)
        self.cpage = min(self.cpage, self.max_page)

        self.start = (self.cpage - 1) * psize
        self.start = 0 if self.start < 0 else self.start
        self.end = psize

        # 初始化页码
        self.init_page_num(self.cpage, self.max_page)

    def init_page_num(self, cpage, max_page):
        '''初始化页面页码

        @cpage, int, 当前页码
        @max_page, int, 最大页数
        '''
        begin_page, end_page = 1, 1
        # 总页码小于15
        if max_page < 15:
            # 开始:1
            begin_page = 1
            # 结束:总页码
            end_page = max_page
        else:
            # 保证显示15个
            begin_page = cpage - 7
            end_page = cpage + 7
            if begin_page < 1:
                begin_page = 1
                end_page = 15
            elif end_page > max_page:
                end_page = max_page
                begin_page = max_page - 15

        self.begin_page = math.floor(begin_page)
        self.end_page = math.ceil(end_page)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
