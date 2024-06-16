from common.psycopy2_operate import db


class DeviceDao:

    def __init__(self, db):
        self.db = db

    def add(self, deviceid, system, branch, system_version, name, extension, now):
        sqlInsertDevice = "INSERT INTO " \
                          "common_device(" \
                          "device_id, system, branch, system_version, name, ext, create_time, update_time" \
                          ") " \
                          "VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')" \
            .format(deviceid, system, branch, system_version, name, extension, now, now)
        db.execute_db(sqlInsertDevice)

    def select_by_deviceid(self, deviceid):
        sql = "select * from common_device where device_id = '{}'".format(deviceid)
        return db.select_db(sql)

    def select_device_app_by_deviceid(self, deviceid):
        sql = "select * from common_device_app where device_id = '{}'".format(deviceid)
        return db.select_db(sql)

    def add_device_app(self, deviceid, appid, version, now):
        sqlInsertDevApp = "INSERT INTO " \
                          "common_device_app(device_id, appid, version, create_time, update_time) " \
                          "VALUES('{}', '{}', '{}', '{}', '{}')" \
            .format(deviceid, appid, version, now, now)
        db.execute_db(sqlInsertDevApp)

    def update_device_app_info(self, deviceid, appid, version, now):
        sqlUpdateDevApp = ("UPDATE common_device_app "
                           "set version='{}', update_time={} where device_id = '{}' and appid = '{}'") \
            .format(version, now, deviceid, appid)
        db.execute_db(sqlUpdateDevApp)


device_dao = DeviceDao(db)

