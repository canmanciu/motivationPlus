create database iquateone;
use iquateone;

CREATE TABLE `iqua_device` (
  `id` bigint(20) unsigned NOT NULL,
  `device_id` varchar(128) NOT NULL DEFAULT '' COMMENT '设备id',
  `system` varchar(64) NOT NULL DEFAULT '' COMMENT '系统名称',
  `branch` varchar(64) NOT NULL DEFAULT '' COMMENT '品牌名称',
  `system_version` varchar(64) NOT NULL DEFAULT '' COMMENT '系统版本号',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '设备名称',
  `ext` JSON ,

  `create_time` bigint(20) unsigned NOT NULL COMMENT '创建时间',
  `update_time` bigint(20) unsigned NOT NULL COMMENT '更新时间',

  PRIMARY KEY (`id`),
  KEY `IDX_DEVICE_ID` (`device_id`),
  KEY `IDX_UPDATE_TIME` (`update_time`),
  KEY `IDX_CREATE_TIME` (`create_time`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `iqua_device_app` (
  `id` bigint(20) unsigned NOT NULL,
  `device_id` varchar(128) NOT NULL DEFAULT '' COMMENT '设备id',
  `appid` varchar(64) NOT NULL DEFAULT '' COMMENT '应用id',
  `version` varchar(64) NOT NULL DEFAULT '' COMMENT '应用版本号',

  `create_time` bigint(20) unsigned NOT NULL COMMENT '创建时间',
  `update_time` bigint(20) unsigned NOT NULL COMMENT '更新时间',

  PRIMARY KEY (`id`),
  KEY `IDX_DEVICE_ID` (`device_id`),
  KEY `IDX_UPDATE_TIME` (`update_time`),
  KEY `IDX_CREATE_TIME` (`create_time`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `iqua_user_device` (
  `id` bigint(20) unsigned NOT NULL,
  `userid` bigint(20) unsigned NOT NULL COMMENT '帐号id',
  `appid` bigint(20) unsigned NOT NULL COMMENT '应用id',
  `did` int(20) unsigned NOT NULL DEFAULT 0 COMMENT '设备主键id',
  `ip` varchar(128) NOT NULL DEFAULT '' COMMENT 'ip',
  `status` smallint(8) NOT NULL DEFAULT 1 COMMENT '状态，1 表示在线，2 表示离线',

  `create_time` bigint(20) unsigned NOT NULL COMMENT '创建时间',
  `update_time` bigint(20) unsigned NOT NULL COMMENT '更新时间',

  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_DEVICE` (`userid`, `did`, `appid`),
  KEY `IDX_DEVICE` (`did`, `appid`),
  KEY `IDX_STATUS` (`status`),
  KEY `IDX_UPDATE_TIME` (`update_time`),
  KEY `IDX_CREATE_TIME` (`create_time`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `iqua_user` (
  `id` bigint(20) unsigned NOT NULL,
  `nickname` varchar(128) NOT NULL DEFAULT '' COMMENT '昵称',
  `email` varchar(128) NOT NULL DEFAULT '' COMMENT '邮箱',
  `mobile` varchar(64) NOT NULL DEFAULT '' COMMENT '手机号码',

  `create_time` bigint(20) unsigned NOT NULL COMMENT '创建时间',
  `update_time` bigint(20) unsigned NOT NULL COMMENT '更新时间',

  PRIMARY KEY (`id`),
  KEY `IDX_EMAIL` (`email`),
  KEY `IDX_MOBILE` (`mobile`),
  KEY `IDX_UPDATE_TIME` (`update_time`),
  KEY `IDX_CREATE_TIME` (`create_time`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

