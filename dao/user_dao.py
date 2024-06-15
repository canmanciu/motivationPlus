import time

from common.psycopy2_operate import db


class UserDao:

    def __init__(self, db):
        self.db = db

    def add_user(self, deviceid):
        now = int(time.time_ns() // 1_000_000)
        sqlInsertUserLogin = "INSERT INTO " \
                             "common_user(" \
                             "nickname, email, mobile, create_time, update_time" \
                             ") " \
                             "VALUES('{}', '{}', '{}', '{}', '{}') RETURNING id" \
            .format(deviceid, '', '', now, now)
        return db.execute_db(sqlInsertUserLogin)

    def add_user_login_account(self, userid, login_account, status):
        now = int(time.time_ns() // 1_000_000)
        sqlInsertUserLogin = "INSERT INTO " \
                             "common_user_login_account(" \
                             "userid, login_account, status, create_time, update_time" \
                             ") " \
                             "VALUES('{}', '{}', '{}', '{}', '{}')" \
            .format(userid, login_account, status, now, now)
        db.execute_db(sqlInsertUserLogin)

    def select_device_by_userid_deviceid_appid(self, userid, deviceid, appid):
        sql = "select * from common_user_device where userid = '{}' and device_id = '{}' and appid = '{}'"\
            .format(userid, deviceid, appid)
        return db.select_db(sql)

    def update_user_device(self, ip, id):
        now = int(time.time_ns() // 1_000_000)
        sqlUpdateUserDevice = "UPDATE common_user_device set status = 1, ip = '{}', update_time = '{}' " \
                              "where id = '{}'" \
            .format(ip, now, id)
        db.execute_db(sqlUpdateUserDevice)

    def create_user_device(self, userid, deviceid, appid, ip, status):
        now = int(time.time_ns() // 1_000_000)
        sqlInsertUserDevice = "INSERT INTO " \
                              "common_user_device(" \
                              "userid, device_id, appid, ip, status, create_time, update_time" \
                              ") " \
                              "VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')" \
            .format(userid, deviceid, appid, ip, status, now, now)
        db.execute_db(sqlInsertUserDevice)

    def select_by_login_account(self, login_account):
        sqlSelectUserLogin = "select * from common_user_login_account where login_account = '{}' and status = 1" \
            .format(login_account)
        return db.select_db(sqlSelectUserLogin)

    def select_by_userid(self, userid):
        sqlSelectUser = "select * from common_user where id = '{}'".format(userid)
        return db.select_db(sqlSelectUser)


user_dao = UserDao(db)

