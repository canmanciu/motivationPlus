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


device_dao = DeviceDao(db)

