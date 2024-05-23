import time
import json
import uuid

from flask import Flask, jsonify, request

from common.aes_operate import cipher
from common.psycopy2_operate import db
from common.ip_operate import getip
from dao.device_dao import device_dao
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示


@app.route('/')
def hello_world():
    return '404'


@app.route('/device/init', methods=["POST"])
def device_init():
    try:
        deviceid = request.json.get("deviceId", str(uuid.uuid4())).strip()  # 设备id
        system = request.json.get("system", "").strip()  # 系统
        branch = request.json.get("branch", "").strip()  # 品牌
        system_version = request.json.get("systemVersion", "").strip()  # 系统版本
        app_version = request.json.get("applicationVersion", "").strip()  # 应用版本
        name = request.json.get("name", "").strip()  # 名称
        application_id = request.json.get("applicationId", "").strip()  # 应用id
        extension = request.json.get("extension", "{}").strip()  # 扩展字段
        if not application_id:
            return jsonify({"code": 400, "message": "param applicationId illegal"})

        """根据deviceId 进行查询，如果存在直接返回，不存在则新增"""
        data = device_dao.select_by_deviceid(deviceid)
        print("获取 {} 设备信息 == >> {}".format(deviceid, data))
        if not data:
            """创建新纪录"""
            now = int(time.time_ns() // 1_1000_000)
            device_dao.add(deviceid, system, branch, system_version, name, extension, now)

        sqlQueryApp = "select * from common_device_app where device_id = '{}' and appid = '{}'" \
            .format(deviceid, application_id)
        application = db.select_db(sqlQueryApp)
        if not application:
            now = int(time.time_ns() // 1_1000_000)
            sqlInsertDevApp = "INSERT INTO " \
                              "common_device_app(device_id, appid, version, create_time, update_time) " \
                              "VALUES('{}', '{}', '{}', '{}', '{}')" \
                .format(deviceid, application_id, app_version, now, now)
            db.execute_db(sqlInsertDevApp)

        request.json['deviceId'] = deviceid
        fp = cipher.encrypt(json.dumps(request.json))
        result = {"deviceId": deviceid, "devFp": fp}
        return jsonify({"code": 200, "result": result})
    except BadRequest as e:
        # 如果 get_json() 引发 BadRequest 异常，则捕获并处理它
        return jsonify({"code": 400, "message": "参数异常"}), 400
    except Exception as e:
        print("操作出现错误：{}".format(e))
        app.logger.exception("捕获到异常")
        return jsonify({"code": 500, "message": "系统异常"}), 500


@app.route('/user/login', methods=["POST"])
def user_login():
    try:
        deviceid = request.json.get("deviceId", "").strip()  # 设备id
        devFp = request.json.get("devFp", "").strip()  # 设备指纹
        devObj = json.loads(cipher.decrypt(devFp))
        if devObj.get("deviceId") != deviceid:
            return jsonify({"code": 400, "message": "params illegal"})

        """根据设备进行帐号生成"""
        sqlSelectUserLogin = "select * from common_user_login_account where login_account = '{}' and status = 1"\
            .format(deviceid)
        data = db.select_db(sqlSelectUserLogin)
        now = int(time.time_ns() // 1_1000_000)
        print("获取 {} 登录帐号绑定信息 == >> {}".format(deviceid, data))
        if data:
            userid = data[0].get(1)
            sqlSelectUser = "select * from common_user where id = '{}'".format(userid)
            db.select_db(sqlSelectUser)
        else:
            """创建新纪录"""
            sqlInsertUserLogin = "INSERT INTO " \
                                 "common_user(" \
                                 "nickname, email, mobile, create_time, update_time" \
                                 ") " \
                                 "VALUES('{}', '{}', '{}', '{}', '{}') RETURNING id" \
                .format(deviceid, '', '', now, now)
            userid = db.execute_db(sqlInsertUserLogin)

            sqlInsertUserLogin = "INSERT INTO " \
                                 "common_user_login_account(" \
                                 "userid, login_account, status, create_time, update_time" \
                                 ") " \
                                 "VALUES('{}', '{}', '{}', '{}', '{}') " \
                .format(userid, deviceid, 1, now, now)
            db.execute_db(sqlInsertUserLogin)

        appid = devObj["applicationId"]
        '''更新设备登录记录'''
        sqlQueryUserDevice = "select * from common_user_device where userid = '{}' and device_id = '{}' " \
                             "and appid = '{}'"\
            .format(userid, deviceid, appid)
        userDevice = db.select_db(sqlQueryUserDevice)
        clientIp = getip(request)
        if userDevice:
            sqlUpdateUserDevice = "UPDATE common_user_device set status = 1, ip = '{}', update_time = '{}' " \
                                  "where id = '{}'" \
                .format(deviceid, clientIp, now, userDevice[0].get(0))
            db.execute_db(sqlUpdateUserDevice)
        else:
            addUpdateUserDevice = "INSERT INTO common_user_device(" \
                                  "userid, appid, device_id, ip, status, create_time, update_time" \
                                  ") values('{}', '{}', '{}', '{}', '{}', '{}', '{}') " \
                .format(userid, appid, deviceid, clientIp, 1, now, 0)
            db.execute_db(addUpdateUserDevice)

        sessObj = {"t": now, "userid": userid, "deviceid": deviceid, "appid": appid, "ip": clientIp}
        sess = cipher.encrypt(json.dumps(sessObj))
        result = {"sess": sess, "uid": userid}
        return jsonify({"code": 200, "result": result})
    except BadRequest as e:
        # 如果 get_json() 引发 BadRequest 异常，则捕获并处理它
        return jsonify({"code": 400, "message": "参数异常"}), 400
    except Exception as e:
        print("操作出现错误：{}".format(e))
        app.logger.exception("捕获到异常")
        return jsonify({"code": 500, "message": "系统异常"}), 500


