import os, sys
import logging
from config.setting import SERVER_PORT
from api.controller import app
from logging.handlers import RotatingFileHandler


# 项目根路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_PATH)  # 将项目根路径临时加入环境变量，程序退出后失效

if __name__ == '__main__':
    app.logger.setLevel(logging.ERROR)  # 设置日志级别为 ERROR
    # 创建一个 handler，用于写入日志文件
    file_handler = RotatingFileHandler('flask.log',
                                       maxBytes=1024 * 1024 * 100, backupCount=10)
    file_handler.setLevel(logging.ERROR)
    # 定义 handler 的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    # 给 app.logger 添加 handler
    app.logger.addHandler(file_handler)
    # host为主机ip地址，port指定访问端口号，debug=True设置调试模式打开
    app.run(host="0.0.0.0", port=SERVER_PORT, debug=True)

