CREATE DATABASE iquateone;
\c iquateone


CREATE TABLE common_device (  
    id BIGSERIAL PRIMARY KEY,
    device_id VARCHAR(128) NOT NULL DEFAULT ''::character varying, -- 在 PostgreSQL 中，需要指定默认值的数据类型  
    system VARCHAR(64) NOT NULL DEFAULT ''::character varying, -- 同上  
    branch VARCHAR(64) NOT NULL DEFAULT ''::character varying, -- 同上  
    system_version VARCHAR(64) NOT NULL DEFAULT ''::character varying, -- 同上  
    name VARCHAR(128) NOT NULL DEFAULT ''::character varying, -- 
    ext JSONB, -- PostgreSQL 使用 JSONB 类型来存储可二进制格式的 JSON 数据，支持索引  
    create_time BIGINT NOT NULL,  
    update_time BIGINT NOT NULL
);  
  
-- 创建索引  
CREATE INDEX IDX_DEVICE_DEVICE_ID ON common_device (device_id);
CREATE INDEX IDX_DEVICE_UPDATE_TIME ON common_device (update_time);
CREATE INDEX IDX_DEVICE_CREATE_TIME ON common_device (create_time);

COMMENT ON COLUMN common_device.device_id IS '设备id';
COMMENT ON COLUMN common_device.system IS '系统名称';
COMMENT ON COLUMN common_device.branch IS '品牌名称';
COMMENT ON COLUMN common_device.system_version IS '系统版本号';
COMMENT ON COLUMN common_device.name IS '设备名称';
COMMENT ON COLUMN common_device.ext IS '扩展信息';
COMMENT ON COLUMN common_device.create_time IS '创建时间';
COMMENT ON COLUMN common_device.update_time IS '更新时间';


CREATE TABLE common_device_app (  
    id BIGSERIAL PRIMARY KEY, -- 使用 BIGSERIAL 替代 bigint(20) unsigned，自动增长  
    device_id VARCHAR(128) NOT NULL DEFAULT ''::character varying ,
    appid VARCHAR(64) NOT NULL DEFAULT ''::character varying ,
    version VARCHAR(64) NOT NULL DEFAULT ''::character varying ,
    create_time BIGINT NOT NULL ,
    update_time BIGINT NOT NULL
);  
  
-- 实际上，我们应该创建普通的索引，而不是 UNIQUE 约束，除非确实需要唯一性  
CREATE INDEX idx_devapp_device_id_idx ON common_device_app (device_id);
CREATE INDEX idx_devapp_update_time_idx ON common_device_app (update_time);
CREATE INDEX idx_devapp_create_time_idx ON common_device_app (create_time);

COMMENT ON COLUMN common_device_app.device_id IS '设备id';
COMMENT ON COLUMN common_device_app.appid IS '应用id';
COMMENT ON COLUMN common_device_app.version IS '应用版本号';
COMMENT ON COLUMN common_device_app.create_time IS '创建时间';
COMMENT ON COLUMN common_device_app.update_time IS '更新时间';


CREATE TABLE common_user_device (  
    id BIGSERIAL PRIMARY KEY, -- 使用 BIGSERIAL 替代 bigint(20) unsigned，自动增长  
    userid BIGINT NOT NULL ,
    appid VARCHAR(128) NOT NULL DEFAULT ''::character varying ,
    device_id VARCHAR(128) NOT NULL DEFAULT ''::character varying ,
    ip VARCHAR(128) NOT NULL DEFAULT ''::character varying ,
    status SMALLINT NOT NULL DEFAULT 1 ,
    create_time BIGINT NOT NULL ,
    update_time BIGINT NOT NULL ,
      
    -- 创建索引和约束  
    CONSTRAINT uk_userdev_device UNIQUE (userid, device_id, appid) -- 联合唯一键
      
); 

-- 实际上，我们应该创建普通的索引  
CREATE INDEX idx_userdev_device_idx ON common_user_device (device_id, appid);
CREATE INDEX idx_userdev_status_idx ON common_user_device (status);
CREATE INDEX idx_userdev_update_time_idx ON common_user_device (update_time);
CREATE INDEX idx_userdev_create_time_idx ON common_user_device (create_time);

COMMENT ON COLUMN common_user_device.userid IS '帐号id';
COMMENT ON COLUMN common_user_device.appid IS '应用id';
COMMENT ON COLUMN common_user_device.device_id IS '设备id';
COMMENT ON COLUMN common_user_device.ip IS 'ip';
COMMENT ON COLUMN common_user_device.status IS '状态，1 表示在线，2 表示离线';
COMMENT ON COLUMN common_user_device.create_time IS '创建时间';
COMMENT ON COLUMN common_user_device.update_time IS '更新时间';


CREATE TABLE common_user_login_account (
    id BIGSERIAL PRIMARY KEY, -- 使用 BIGSERIAL 替代 bigint(20) unsigned，自动增长
    userid BIGINT NOT NULL ,
    login_account VARCHAR(128) NOT NULL DEFAULT ''::character varying ,
    status SMALLINT NOT NULL DEFAULT 1 ,
    create_time BIGINT NOT NULL ,
    update_time BIGINT NOT NULL ,

    -- 创建索引和约束
    CONSTRAINT uk_userlogin_loginaccount UNIQUE (login_account) -- 联合唯一键

);

-- 实际上，我们应该创建普通的索引
CREATE INDEX idx_userlogin_user_idx ON common_user_login_account (userid);

COMMENT ON COLUMN common_user_login_account.userid IS '帐号id';
COMMENT ON COLUMN common_user_login_account.login_account IS '登录帐号';
COMMENT ON COLUMN common_user_login_account.status IS '状态，1 表示绑定中，2 表示已接触绑定';
COMMENT ON COLUMN common_user_login_account.create_time IS '创建时间';
COMMENT ON COLUMN common_user_login_account.update_time IS '更新时间';


CREATE TABLE common_user (  
    id BIGSERIAL PRIMARY KEY, -- PostgreSQL 使用 BIGSERIAL 作为自增的 BIGINT 类型  
    nickname VARCHAR(128) NOT NULL DEFAULT ''::character varying, -- 昵称  
    email VARCHAR(128) NOT NULL DEFAULT ''::character varying, -- 邮箱  
    mobile VARCHAR(64) NOT NULL DEFAULT ''::character varying, -- 手机号码  
    create_time BIGINT NOT NULL, -- 创建时间  
    update_time BIGINT NOT NULL -- 更新时间  
);  
  
-- PostgreSQL 使用 CREATE INDEX 语句来创建索引  
CREATE INDEX idx_email ON common_user (email);  
CREATE INDEX idx_mobile ON common_user (mobile);  
CREATE INDEX idx_update_time ON common_user (update_time);  
CREATE INDEX idx_create_time ON common_user (create_time);  
  
COMMENT ON TABLE common_user IS 'User table';  
COMMENT ON COLUMN common_user.nickname IS '昵称';  
COMMENT ON COLUMN common_user.email IS '邮箱';  
COMMENT ON COLUMN common_user.mobile IS '手机号码';  
COMMENT ON COLUMN common_user.create_time IS '创建时间';  
COMMENT ON COLUMN common_user.update_time IS '更新时间';


