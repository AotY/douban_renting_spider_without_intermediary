#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : db_client.py
# Author            : Qing Tao <qingtao12138@163.com>
# Date              : 16.03.2021
# Last Modified Date: 27.03.2022
# Last Modified By  : Qing Tao <qingtao12138@163.com>
# coding: utf8

""" 单例mongo客户端 """

from pymongo import MongoClient

from config import (
    DB_URI, DB_NAME,
    DB_TLS_CA_FILE,
    DB_TLS_CERTIFICATE_KEY_FILE
)



class DBClient(object):

    """ mongodb客户端 """

    _client = None

    @property
    def client(self):
        if not self._client:
            #self._client = MongoClient(DB_URI)
            self._client = MongoClient(
                DB_URI,
                tls=True,
                # tlsCAFile='/Users/LeonTao/mongodb-macos-x86_64-4.2.12/ssl/ca.pem',
                # tlsCertificateKeyFile='/Users/LeonTao/mongodb-macos-x86_64-4.2.12/ssl/client.pem'
                tlsCAFile=DB_TLS_CA_FILE,
                tlsCertificateKeyFile=DB_TLS_CERTIFICATE_KEY_FILE
            )
        return self._client

    @property
    def db(self):
        """Return DB_NAME client"""
        return self.client[DB_NAME]


if __name__ == '__main__':
    db_client = DBClient()
    print("db: {}".format(db_client.db))
    cursor = db_client.db.test.find() # test
    for item in cursor:
        print(item)
