# usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : update_proxies.sh
# Author            : Qing Tao <qingtao12138@163.com>
# Date              : 17.03.2021
# Last Modified Date: 29.04.2022
# Last Modified By  : Qing Tao <qingtao12138@163.com>
# coding: utf8

export http_proxy="127.0.0.1:4780";
export https_proxy="127.0.0.1:4780";

declare -a proxies=("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt" "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt")

echo "127.0.0.1:4780" > ./data/tmp_local.txt
for proxy in "${proxies[@]}"
do
  echo "proxy: $proxy";
  tmp_name=$(echo $proxy | awk -F "/" '{print $5;}');
  echo "$tmp_name"
  # wget -c $proxy -O ./data/tmp_${tmp_name}.txt;
  wget -O ./data/tmp_${tmp_name}.txt $proxy --timeout=5 -o ./data/wget_tmp_${tmp_name}.log
done

echo "" > ./data/raw_proxies.txt
less ./data/tmp_*.txt > ./data/raw_proxies.txt

rm -rf ./data/tmp_*.txt
rm -rf ./data/wget-log*

export http_proxy=""; 
export https_proxy="";

echo "Proxies ready!"

