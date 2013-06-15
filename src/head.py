#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import struct
import sqlite3
import MySQLdb
import threading
from time import sleep
from datetime import datetime

MAX_TASK_ID     = 65535
DB_PATH         = "../db/irrigating_system.db"
MYSQL_SQL_PATH  = "../db/mysql_creater.sql"
SQL_PATH        = "../db/sqlite_creater.sql"

d_db_conn_local = {
    "HOST"      : "localhost",
    "USER"      : "johnchain",
    "PASSWORD"  : "johnchain",
    #"DATABASE"  : "irrigating_system",
    "DATABASE"  : "test",
    }

d_db_conn_remote = {
    "HOST"      : "10.18.50.10",
    "USER"      : "smartwin",
    "PASSWORD"  : "smartwin",
    "DATABASE"  : "irrigating_system",
    }

d_task_status = {
    "SUCCEED"     : 0,
    "FAILED"      : 1,
    "DEALING"     : 2,
    "SUBMITTING"  : 3,
    }

d_switcher = {
    "OFF"         : 0,
    "ON"          : 1,
    }

d_sensor_set = {
    "PUMP"           : 0, #水泵
    "SOLENOIDVALVES" : 1, # 电磁阀门
    "YL69"           : 2, # 土壤湿度传感器
    "LIGHT"          : 3, # 光照
    "THERMISTOR"     : 4, # 空气中的温度
    "DS18B20"        : 5, # 土壤中的温度
    }

d_sensor_num_to_name = {
    "0" : "PUMP"          , #水泵
    "1" : "SOLENOIDVALVES", # 电磁阀门
    "2" : "YL69"          , # 土壤湿度传感器
    "3" : "LIGHT"         , # 光照
    "4" : "THERMISTOR"    , # 空气中的温度
    "5" : "DS18B20"       , # 土壤中的温度
    }

d_request_code = {
    "SET_SWITCH_STATUS_REQUEST"     : 1, # 设置传感器开关
    "GET_SWITCH_STATUS_REQUEST"     : 2, # 获取开关状态
    "GET_READING_REQUEST      "     : 3, # 获取传感器采集的数据
    "SET_READING_PERIOD_REQUEST"    : 4, # 设置采集的周期
    "GET_READING_PERIOD_REQUEST"    : 5, # 获取采集的周期
    "SET_READING_THRESHOLD_REQUEST" : 6, # 设置阈值
    "GET_READING_THRESHOLD_REQUEST" : 7, # 获取阈值
    }

d_request_code_to_name = {
    "1" : "SET_SWITCH_STATUS_REQUEST"    , # 设置传感器开关
    "2" : "GET_SWITCH_STATUS_REQUEST"    , # 获取开关状态
    "3" : "GET_READING_REQUEST      "    , # 获取传感器采集的数据
    "4" : "SET_READING_PERIOD_REQUEST"   , # 设置采集的周期
    "5" : "GET_READING_PERIOD_REQUEST"   , # 获取采集的周期
    "6" : "SET_READING_THRESHOLD_REQUEST", # 设置阈值
    "7" : "GET_READING_THRESHOLD_REQUEST", # 获取阈值
    }

d_default_data = {
    "DEFAULT_SWITCH"            : 0,
    "DEFAULT_DS18B20_PERIOD"    : 3000,
    "DEFAULT_YL69_PERIOD"       : 3000,
    "DEFAULT_LIGHT_PERIOD"      : 3000,
    "DEFAULT_TEMP_PERIOD"       : 3000,
    "DEFAULT_MIC_PERIOD"        : 1,

    "DEFAULT_DS18B20_THRESHOLD" : 30,
    "DEFAULT_YL69_THRESHOLD"    : 0,
    "DEFAULT_LIGHT_THRESHOLD"   : 50,
    "DEFAULT_TEMP_THRESHOLD"    : 800,
    "DEFAULT_MIC_THRESHOLD"     : 900,
    }

class t_insert_data():
        node_id = 0
        sensor_id = 0
        data = 0

class t_select_sensor_state():
    node_id = 0

class t_update_sensor_state():
        node_id = 0
        sensor_id = 0
        switcher = 0
        capture_frequency = 0
        threshold = 0

class t_select_history_data():
    node_id = 0
    start_time = ''
    end_time = ''

class t_insert_task():
    transaction_number = ''
    node_id = 0
    sensor_id = 0
    operation_code = 0
    operation_data = 0
    status = 0

class t_select_task_status():
    transaction_number = ''

class t_select_task():
    status = 0


class t_update_task():
    transaction_number = ''
    node_id = 0
    sensor_id = 0
    operation_code = 0
    operation_data = 0
    status = 0

def Celsius(ADC):
    from math import log, pow
    ADC    = float(ADC)
    ADC_FS = 1023
    R1     = 10000
    A      = 0.00130705
    B      = 0.000214381
    C      = 0.000000093
    Rthr   = R1 * (ADC_FS - ADC) / ADC
    result = float((1 / (A + B * log(Rthr) + C * pow(log(Rthr), 3))) - 273.15)
    return result

