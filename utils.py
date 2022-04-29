#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : utils.py
# Author            : Qing Tao <qingtao12138@163.com>
# Date              : 15.03.2021
# Last Modified Date: 20.04.2022
# Last Modified By  : Qing Tao <qingtao12138@163.com>
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import logging
import random
import subprocess
import re

# from config import PROXY_LIST_URLS


class Timer(object):
    """定时器，定时执行指定的函数

    """

    def __init__(self, start, interval):
        """
        @start, int, 延迟执行的秒数
        @interval, int, 每次执行的间隔秒数
        """
        self.start = start
        self.interval = interval

    def run(self, func, *args, **kwargs):
        """运行定时器

        @func, callable, 要执行的函数
        *args, 需要执行函数的参数
        **kwary, 参数字典
        """
        time.sleep(self.start)
        while True:
            func(*args, **kwargs)
            time.sleep(self.interval)


class ProxyManager(object):
    """代理管理器
    """

    def __init__(self, interval_per_ip=0, is_single=False):
        '''
        @interval_per_ip, int, 每个ip调用最小间隔, s
        @is_single, bool, 是否启用单点代理,例如使用 squid
        '''
        self.host_time_map = {}
        self.interval = interval_per_ip
        self.is_single = is_single

    def init_proxies(self, proxies_or_path):
        '''初始化代理列表
        @proxies_or_path, str or list, 代理path或列表
        @proxies_or_path, list or str
        '''
        self.proxies_or_path = proxies_or_path
        if isinstance(proxies_or_path, str):
            if self.is_single:
                if not proxies_or_path:
                    return False
                self.proxies = proxies_or_path
            else:
                if not os.path.exists(proxies_or_path):
                    return False
                with open(proxies_or_path) as f:
                    self.proxies = list(
                        set([p.strip().split()[0] for p in f.readlines() if p.strip()]))
        else:
            self.proxies = proxies_or_path

        if isinstance(self.proxies, list) and len(self.proxies) == 0:
            return False

        return True

    def reload_proxies(self):
        '''重新加载代理，proxies_or_path必须是文件路径 '''
        if not isinstance(self.proxies_or_path, str):
            raise TypeError("proxies_or_path type is invalid!")
        if self.is_single:
            raise TypeError("is_single must be False!")
        with open(self.proxies_or_path) as f:
            # self.proxies = f.readlines()
            # self.proxies = [p.strip().split()[0] for p in f.readlines()]
            self.proxies = list(
                set([p.strip().split()[0] for p in f.readlines() if p.strip()]))
        logging.info("reload %s proxies ...", len(self.proxies))

    def get_proxy(self):
        '''获取一个可用代理

        如果代理使用过于频繁会阻塞，以防止服务器屏蔽
        '''
        # 如果使用单点代理,直接返回
        if self.is_single:
            return self.proxies
        proxy = self.proxies[random.randint(0, len(self.proxies) - 1)].strip()
        host, _ = proxy.split(':')
        latest_time = self.host_time_map.get(host, 0)
        interval = time.time() - latest_time
        if interval < self.interval:
            logging.info("%s waiting", proxy)
            time.sleep(self.interval)
        self.host_time_map[host] = time.time()
        # return "http://%s" % proxy.strip()
        return proxy.strip()

    def remove(self, proxy):
        print('remove proxy: ', proxy)
        if self.is_single:
            print("exit! has no more proxy.")
            exit(0)
        else:
            if len(self.proxies) == 0:
                print("exit! has no more proxy.")
                exit(0)
            if proxy in self.proxies:
                self.proxies.remove(proxy)

    # def download_proxy_list(self, proxies_or_path):
    #     proxy_re = re.compile(r"^\d+\.\d+\.\d+\.\d+:\d+$")

    #     proxy_list_file = open(proxies_or_path, 'w', encoding='utf-8')
    #     # proxy_list_file.write('127.0.0.1:1087\n')

    #     for i, proxy_list_url in enumerate(PROXY_LIST_URLS):
    #         # download_command = 'wget -O tmp_proxy_list_%s.txt %s' % (proxy_list_url, i)
    #         subprocess.call(['wget', '-O', 'tmp_proxy_list_%s.txt' % i, proxy_list_url])
    #         with open('tmp_proxy_list_%s.txt' % i, 'r', encoding='utf-8') as tmp_f:
    #             for line in tmp_f:
    #                 line = line.rstrip()
    #                 if proxy_re.match(line) is not None:
    #                     proxy_list_file.write(line)

    #     proxy_list_file.close()
    #     self.proxies_or_path = proxies_or_path
    #     self.init_proxies(proxies_or_path)

