import psycopg2
import psycopg2.extras

from config.setting import POSTGRES_HOST, POSTGRES_DB, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWD


class PostgresDb:

    def __init__(self, host, port, user, passwd, db):
        # 建立数据库连接
        self.conn = psycopg2.connect(
            host=host,
            database=db,
            user=user,
            password=passwd,
            port=port
        )
        # 通过 cursor() 创建游标对象，并让查询结果以字典格式输出
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def __del__(self): # 对象资源被释放时触发，在对象即将被删除时的最后操作
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def select_db(self, sql):
        """查询"""
        # 检查连接是否断开，如果断开就进行重连
        # self.conn.ping(reconnect=True)
        # 使用 execute() 执行sql
        self.cur.execute(sql)
        # 使用 fetchall() 获取查询结果
        data = self.cur.fetchall()
        return data

    def execute_db(self, sql):
        """更新/新增/删除"""
        try:
            # 检查连接是否断开，如果断开就进行重连
            # self.conn.ping(reconnect=True)
            # 使用 execute() 执行sql
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
            if sql.endswith("RETURNING id"):
                return self.cur.fetchone()[0]
        except Exception as e:
            print("操作出现错误：{}".format(e))
            # 回滚所有更改
            self.conn.rollback()
            raise e


db = PostgresDb(POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWD, POSTGRES_DB)

