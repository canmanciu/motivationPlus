import datetime
import socket

# twitter's snowflake parameters
twepoch = 1288834974657
datacenter_id_bits = 5
worker_id_bits = 5
sequence_id_bits = 12
max_datacenter_id = 1 << datacenter_id_bits
max_worker_id = 1 << worker_id_bits
max_sequence_id = 1 << sequence_id_bits
max_timestamp = 1 << (64 - datacenter_id_bits - worker_id_bits - sequence_id_bits)

def make_snowflake(timestamp_ms, datacenter_id, worker_id, sequence_id, twepoch=twepoch):
    """generate a twitter-snowflake id, based on
    https://github.com/twitter/snowflake/blob/master/src/main/scala/com/twitter/service/snowflake/IdWorker.scala
    :param: timestamp_ms time since UNIX epoch in milliseconds"""

    sid = ((int(timestamp_ms) - twepoch) % max_timestamp) << datacenter_id_bits << worker_id_bits << sequence_id_bits
    sid += (datacenter_id % max_datacenter_id) << worker_id_bits << sequence_id_bits
    sid += (worker_id % max_worker_id) << sequence_id_bits
    sid += sequence_id % max_sequence_id

    return sid

def melt(snowflake_id, twepoch=twepoch):
    """inversely transform a snowflake id back to its parts."""
    sequence_id = snowflake_id & (max_sequence_id - 1)
    worker_id = (snowflake_id >> sequence_id_bits) & (max_worker_id - 1)
    datacenter_id = (snowflake_id >> sequence_id_bits >> worker_id_bits) & (max_datacenter_id - 1)
    timestamp_ms = snowflake_id >> sequence_id_bits >> worker_id_bits >> datacenter_id_bits
    timestamp_ms += twepoch

    return (timestamp_ms, int(datacenter_id), int(worker_id), int(sequence_id))

def local_datetime(timestamp_ms):
    """convert millisecond timestamp to local datetime object."""
    return datetime.datetime.fromtimestamp(timestamp_ms / 1000.)

def get_local_ip():
    # 创建一个 socket 对象
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 不需要连接，只是获取本地主机的名称
        host_name = socket.gethostname()
        # 获取主机名对应的所有IP地址
        address_list = socket.getaddrinfo(host_name, None)
        for item in address_list:
            if item[0] == socket.AF_INET:
                # 返回 IPv4 地址
                return item[4][0]
    except socket.error:
        pass
    finally:
        s.close()
    return None

if __name__ == '__main__':
    # import time
    # t0 = int(time.time() * 1000)
    # print(local_datetime(t0))
    # time.sleep(0.001)
    # print(make_snowflake(int(time.time_ns() // 1_000_000), 0, 0, 0))
    # time.sleep(0.001)
    # print(make_snowflake(int(time.time_ns() // 1_000_000), 0, 0, 0))
    # time.sleep(0.001)
    # print(make_snowflake(int(time.time_ns()), 0, 0, 0))
    # print(make_snowflake(int(time.time_ns()), 0, 0, 0))
    # print(get_local_ip())
    # assert(melt(make_snowflake(t0, 0, 0, 0))[0] == t0)
    import json
    print(json.dumps({"a":"aaa"}))

