from common.psycopy2_operate import db


class SentenceDao:

    def __init__(self, db):
        self.db = db

    def add(self, name, content, source, extension, now):
        sqlInsertDevice = "INSERT INTO " \
                          "iquate_sentence(" \
                          "name, content, source, extension, create_time, update_time" \
                          ") " \
                          "VALUES('{}', '{}', '{}', '{}', '{}', '{}')" \
            .format(name, content, source, extension, now, now)
        db.execute_db(sqlInsertDevice)

    def list_by_begin_id(self, lastid, length):
        sql = "select * from iquate_sentence where id > '{}' limit '{}'"\
            .format(lastid, length)
        return db.select_db(sql)


sentence_dao = SentenceDao(db)

