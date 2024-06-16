import csv
import json
import time
import uuid

from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

from common.aes_operate import cipher
from common.ip_operate import getip
from common.session_operate import session
from dao.background_dao import background_dao
from dao.device_dao import device_dao
from dao.sentence_dao import sentence_dao
from dao.user_dao import user_dao

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
        extension = request.json.get("extension", {})  # 扩展字段
        if not application_id:
            return jsonify({"code": 400, "message": "param applicationId illegal"})

        """根据deviceId 进行查询，如果存在直接返回，不存在则新增"""
        data = device_dao.select_by_deviceid(deviceid)
        print("获取 {} 设备信息 == >> {}".format(deviceid, data))
        if not data:
            """创建新纪录"""
            now = int(time.time_ns() // 1_000_000)
            device_dao.add(deviceid, system, branch, system_version, name, json.dumps(extension), now)

        application = device_dao.select_device_app_by_deviceid(deviceid)
        if not application:
            now = int(time.time_ns() // 1_000_000)
            device_dao.add_device_app(deviceid, application_id, app_version, now)
        elif app_version and application[0][3] != app_version:
            now = int(time.time_ns() // 1_000_000)
            device_dao.update_device_app_info(deviceid, application_id, app_version, now)

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
        data = user_dao.select_by_login_account(deviceid)
        print("获取 {} 登录帐号绑定信息 == >> {}".format(deviceid, data))
        if data:
            userid = data[0].get(1)
            user_dao.select_by_userid(userid)
        else:
            """创建新纪录"""
            userid = user_dao.add_user(deviceid)
            user_dao.add_user_login_account(userid, deviceid, 1)

        appid = devObj["applicationId"]
        '''更新设备登录记录'''
        userDevice = user_dao.select_device_by_userid_deviceid_appid(userid, deviceid, appid)
        clientIp = getip(request)
        if userDevice:
            user_dao.update_user_device(clientIp, userDevice[0].get(0))
        else:
            user_dao.create_user_device(userid, deviceid, appid, clientIp, 1)

        sess = session.generate(userid, deviceid, appid, clientIp)
        result = {"sess": sess, "uid": userid}
        return jsonify({"code": 200, "result": result})
    except BadRequest as e:
        # 如果 get_json() 引发 BadRequest 异常，则捕获并处理它
        return jsonify({"code": 400, "message": "参数异常"}), 400
    except Exception as e:
        print("操作出现错误：{}".format(e))
        app.logger.exception("捕获到异常")
        return jsonify({"code": 500, "message": "系统异常"}), 500


@app.route('/internal/sentence/import', methods=["POST"])
def sentence_import():
    try:
        clientIp = getip(request)
        if clientIp != '192.168.50.57':
            return jsonify({"code": 403, "message": "no auth"})
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({"code": 400, "message": "file error"})
        file = request.files['file']

        # 如果用户没有选择文件，浏览器也会提交一个空文件部分，没有文件名
        if file.filename == '':
            return jsonify({"code": 400, "message": "file name error"})

        if file:
            # 使用 with 语句确保文件在处理后被正确关闭
            with file.stream as f:
                now = int(time.time_ns() // 1_000_000)
                for row in f:
                    fields = row.decode('utf-8').strip().split(',')
                    sentence_dao.add(fields[0], fields[1], fields[2], fields[3], now)

        return jsonify({"code": 200})
    except BadRequest as e:
        # 如果 get_json() 引发 BadRequest 异常，则捕获并处理它
        return jsonify({"code": 400, "message": "参数异常"}), 400
    except Exception as e:
        print("操作出现错误：{}".format(e))
        app.logger.exception("捕获到异常")
        return jsonify({"code": 500, "message": "系统异常"}), 500


@app.route('/internal/background/import', methods=["POST"])
def background_import():
    try:
        clientIp = getip(request)
        if clientIp != '192.168.50.57':
            return jsonify({"code": 403, "message": "no auth"})
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({"code": 400, "message": "file error"})
        file = request.files['file']

        # 如果用户没有选择文件，浏览器也会提交一个空文件部分，没有文件名
        if file.filename == '':
            return jsonify({"code": 400, "message": "file name error"})

        if file:
            # 使用 with 语句确保文件在处理后被正确关闭
            with open(file.filename, 'r') as f:
                reader = csv.DictReader(f)
                now = int(time.time_ns() // 1_000_000)
                for row in reader:
                    fields = row.strip().split(',')
                    background_dao.add(fields[0], fields[1], fields[2], fields[3], now)

        return jsonify({"code": 200})
    except BadRequest as e:
        # 如果 get_json() 引发 BadRequest 异常，则捕获并处理它
        return jsonify({"code": 400, "message": "参数异常"}), 400
    except Exception as e:
        print("操作出现错误：{}".format(e))
        app.logger.exception("捕获到异常")
        return jsonify({"code": 500, "message": "系统异常"}), 500


@app.route('/sentence', methods=["GET"])
def sentence():
    try:
        header_sess = request.headers["sess"]
        if not session.check(header_sess):
            return jsonify({"code": 401, "message": "login first please"})
        uid = session.get_uid(request.headers["sess"])
        lastId = request.args.get("lastId", 0)
        length = request.args.get("length", 20)
        if length > 1000:
            length = 1000

        data = sentence_dao.list_by_begin_id(lastId, length)
        result = [{'id': obj[0], 'name': obj[1], 'content': obj[2]} for obj in data]
        return jsonify({"code": 200, "result": result})
    except BadRequest as e:
        # 如果 get_json() 引发 BadRequest 异常，则捕获并处理它
        return jsonify({"code": 400, "message": "参数异常"}), 400
    except Exception as e:
        print("操作出现错误：{}".format(e))
        app.logger.exception("捕获到异常")
        return jsonify({"code": 500, "message": "系统异常"}), 500


@app.route('/background', methods=["GET"])
def background():
    try:
        header_sess = request.headers["sess"]
        if not session.check(header_sess):
            return jsonify({"code": 401, "message": "login first please"})
        uid = session.get_uid(request.headers["sess"])
        lastId = request.args.get("lastId", 0)
        length = request.args.get("length", 20)
        if length > 1000:
            length = 1000

        data = background_dao.list_by_begin_id(lastId, length)
        result = [{'name': obj[1], 'src': obj[2]} for obj in data]
        return jsonify({"code": 200, "result": result})
    except BadRequest as e:
        # 如果 get_json() 引发 BadRequest 异常，则捕获并处理它
        return jsonify({"code": 400, "message": "参数异常"}), 400
    except Exception as e:
        print("操作出现错误：{}".format(e))
        app.logger.exception("捕获到异常")
        return jsonify({"code": 500, "message": "系统异常"}), 500


