#!/bin/bash
# File              : start.sh
# Author            : Qing Tao <qingtao12138@163.com>
# Date              : 22.04.2022
# Last Modified Date: 26.04.2022
# Last Modified By  : Qing Tao <qingtao12138@163.com>

sh ./update_proxies.sh

python spider.py
