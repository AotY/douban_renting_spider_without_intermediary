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

declare -a proxies=("https://cdn.jsdelivr.net/gh/mmpx12/proxy-list@master/https.txt" "https://cdn.jsdelivr.net/gh/clarketm/proxy-list@master/proxy-list-raw.txt" "https://cdn.jsdelivr.net/gh/clarketm/proxy-list@master/proxy-list-raw.txt" "https://cdn.jsdelivr.net/gh/TheSpeedX/PROXY-List@master/http.txt" "https://cdn.jsdelivr.net/gh/ShiftyTR/Proxy-List@master/proxy.txt" "https://cdn.jsdelivr.net/gh/hookzof/socks5_list@master/proxy.txt")

echo "127.0.0.1:4780" > ./data/tmp_local.txt
for proxy in "${proxies[@]}"
do
  echo "proxy: $proxy";
  tmp_name=$(echo $proxy | awk -F "/" '{print $5;}');
  echo "$tmp_name"
  # wget -c $proxy -O ./data/tmp_${tmp_name}.txt;
  wget -O ./data/tmp_${tmp_name}.txt $proxy
done

rm -rf ./data/updated_proxies.txt

less ./data/tmp_*.txt > ./data/updated_proxies.txt

export http_proxy=""; 
export https_proxy="";

echo "Proxies ready!"

