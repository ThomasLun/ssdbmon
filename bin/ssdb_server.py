#! /bin/env python
# -*- coding:utf8 -*
# Author  : peilun2050@gmail.com
import logging
from logging.config import logging
from ssdb import SSDB


class SSDBServer(object):
    """Fetches the SSDB info and info commandstats metrics.

    Attributes:
        addr: SSDB server hostname,as well as the Endpoint.
        port: SSDB tcp port number.
        password: SSDB require password, if not empty string.

    """

    def __init__(self, addr, port):
        self.addr = addr
        self.port = port

        logging.config.fileConfig("../conf/logging.ini")
        self.logger = logging.getLogger(__name__)

    def ssdb_info(self):
        try:
            ssdb_cli = SSDB(host=self.addr, port=self.port)
            ssdb_info_list = ssdb_cli.execute_command("info")[2:-2]
            ssdb_info = self.process_ssdb_info_simple(ssdb_info_list)
        except Exception as e:
            self.logger.error(e)
            ssdb_info = {}
        return ssdb_info

    def process_ssdb_info_simple(self, ssdb_info_list):
        """SSDB  simple information"""
        keys = [x for x in ssdb_info_list[::2]]
        values = [x for x in ssdb_info_list[1::2]]
        ssdb_info = dict(zip(keys, values))
        ssdb_info.pop("serv_key_range")
        ssdb_info.pop("data_key_range")
        ssdb_info.pop("version")
        ssdb_info["binlogs"] = dict(map(lambda x: x.replace(" ", "").split(":"), ssdb_info["binlogs"].split("\n")))
        binlogs = ssdb_info.pop("binlogs")
        ssdb_info["binlogs_max_seq"] = binlogs["max_seq"]
        ssdb_info["binlogs_capacity"] = binlogs["capacity"]
        ssdb_info["binlogs_min_seq"] = binlogs["min_seq"]
        return ssdb_info

    def process_ssdb_info(self, ssdb_info_list):
        """SSDB  complete information"""
        keys = [x for x in ssdb_info_list[::2]]
        values = [x for x in ssdb_info_list[1::2]]
        ssdb_info = dict(zip(keys, values))
        ssdb_info["binlogs"] = dict(map(lambda x: x.replace(" ", "").split(":"), ssdb_info["binlogs"].split("\n")))
        ssdb_info["serv_key_range"] = dict(
            map(lambda x: x.replace(" ", "").replace('"', '').split(":"), ssdb_info["serv_key_range"].split("\n")))
        ssdb_info["data_key_range"] = dict(
            map(lambda x: x.replace(" ", "").replace('"', '').split(":"), ssdb_info["data_key_range"].split("\n")))
        return ssdb_info
