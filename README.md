SSDB monitor plugin for Open-Falcon
------------------------------------
------------------------------------
功能支持
------------------

采集SSDB基础状态信息 支持单机多实例;


环境需求
-----------------
操作系统: Linux

Python > 2.6

PyYAML > 3.10

ssdb = *

python-requests > 0.11

ssdbmon部署
--------------------------
1 目录解压到/path/to/ssdbmon

2 配置当前服务器的SSDB多实例信息,/path/to/ssdbmon/conf/ssdbmon.conf 每行记录一个实例: 集群名，密码，端口

- {cluster_name: cluster_1, password: '', port: 8888}

3 配置crontab, 修改ssdbmon_cron文件中ssdbmon安装path; cp ssdbmon_cron /etc/cron.d/

4 查看日志文件/path/to/ssdbmon/log/ssdbmon.log, 如无异常信息，表示采集正常；几分钟后，可从open-falcon的dashboard中查看ssdb metric

5 endpoint默认是hostname

采集的SSDB指标
----------------------------------------

--------------------------------
| Counters | Type | Notes|
|-----|------|------|
|binlogs_capacity  |GAUGE|binlog 队列的最大长度|
|binlogs_min_seq                   |GAUGE|当前队列中的最小 binlog 序号|
|links     |GAUGE|当前服务器的连接数|
|total_calls     |GAUGE|从服务器启动至今处理的请求数|
|ssdb_alive         |GAUGE|是否存活|
|dbsize       |GAUGE|数据库大小|
|binlogs_max_seq         |GAUGE|当前队列中的最大 binlog 序号|


-----------------------------
说明:系统级监控项由falcon agent提供；监控触发条件根据场景自行设置
--------------------------------
Contributors
------------------------------------------
- : Blog: http://www.zzhub.cn
