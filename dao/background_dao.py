from common.psycopy2_operate import db


class BackgroundDao:

    def __init__(self, db):
        self.db = db

    def add(self, name, src, source, extension, now):
        sqlInsertDevice = "INSERT INTO " \
                          "iquate_background(" \
                          "name, src, source, extension, create_time, update_time" \
                          ") " \
                          "VALUES('{}', '{}', '{}', '{}', '{}', '{}')" \
            .format(name, src, source, extension, now, now)
        db.execute_db(sqlInsertDevice)

    def select_all(self):
        sql = "select * from iquate_background"
        return db.select_db(sql)

    def list_by_begin_id(self, lastid, length):
        sql = "select * from iquate_background where id > '{}' limit '{}'"\
            .format(lastid, length)
        return db.select_db(sql)


background_dao = BackgroundDao(db)

