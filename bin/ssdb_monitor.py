#! /bin/env python
# -*- coding:utf8 -*
# Author  : peilun2050@gmail.com
import json
import socket
import requests
import yaml
import time
from logging.config import logging
from ssdb import SSDB

from ssdb_server import SSDBServer

falcon_client = "http://127.0.0.1:1988/v1/push"
upload_ts = int(time.time())


class SSDBFalconMonitor(object):
    """
    ssdb monitor
    """

    def __init__(self, addr, port, password, cluster_name):
        self.addr = addr
        self.port = port
        self.password = password
        self.tags = "ssdb=" + str(port) + "_" + cluster_name
        self.cluster_name = cluster_name
        logging.config.fileConfig("../conf/logging.ini")
        self.logger = logging.getLogger(__name__)

    def ping_ssdb(self):
        ssdb_is_alive = 0
        try:
            ssdb_cli = SSDB(host=self.addr, port=self.port)
            ping_res = ssdb_cli.execute_command("ping")
            if ping_res:
                ssdb_is_alive = 1
        except Exception as e:
            self.logger.error(e)
        if ssdb_is_alive == 0:  # If ssdb is dead, update the alive metrice here.
            ssdb_alive_data = [
                {"endpoint": self.addr, "metric": "ssdb_alive", "tags": self.tags, "timestamp": upload_ts,
                 "value": ssdb_is_alive, "step": 60, "counterType": "GAUGE"}]

            r = requests.post(falcon_client,data=json.dumps(ssdb_alive_data))
            self.logger.debug(r.text)
        return ssdb_is_alive

    def send_data(self):
        # 创建实例
        ssdb_server_info = SSDBServer(self.addr, self.port)
        # 处理后的info dict
        ssdb_server_info_dict = ssdb_server_info.ssdb_info()
        ssdb_server_info_dict["ssdb_alive"] = 1
        ssdb_update_list = []  # The upload info list
        for info_key in ssdb_server_info_dict.keys():
            # 采用COUNTER
            key_item_dict = {"endpoint": self.addr, "metric": info_key, "tags": self.tags, "timestamp": upload_ts,
                             "value": ssdb_server_info_dict[info_key], "step": 60, "counterType": "GAUGE"}
            ssdb_update_list.append(key_item_dict)
        print(ssdb_update_list)
        r = requests.post(falcon_client, data=json.dumps(ssdb_update_list))
        self.logger.debug(r.text)


def main():
    ssdb_hostname = socket.gethostname()
    f = open("../conf/ssdbmon.conf")
    y = yaml.load(f)
    f.close()
    ssdb_items = y["items"]
    for ssdb_ins in ssdb_items:
        ssdb_clusterName = ssdb_ins["cluster_name"]
        ssdb_port = ssdb_ins["port"]
        ssdb_password = ssdb_ins["password"]
        ssdb_falcon_monitor = SSDBFalconMonitor(ssdb_hostname, ssdb_port, ssdb_password, ssdb_clusterName)
        ssdb_is_alive = ssdb_falcon_monitor.ping_ssdb()
        if (ssdb_is_alive == 0):
            continue
        ssdb_falcon_monitor.send_data()


if __name__ == '__main__':
    main()
