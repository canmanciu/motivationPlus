import json
import time

from common.aes_operate import cipher


class Session:
    def __init__(self, cipher):
        self.cipher = cipher

    def generate(self, uid, deviceid, appid, ip):
        now = int(time.time_ns() // 1_000_000)
        sessObj = {"t": now, "uid": uid, "deviceid": deviceid, "appid": appid, "ip": ip}
        return cipher.encrypt(json.dumps(sessObj))

    def check(self, session):
        try:
            json.loads(cipher.decrypt(session))
            return True
        except:
            return False

    def get_uid(self, session):
        return json.loads(cipher.decrypt(session))["uid"]


session = Session(cipher)

