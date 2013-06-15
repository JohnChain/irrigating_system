#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from head import *
from db_operator import db_operator

db_op = db_operator()
db_op.db_connect()
insert_sensor_state = t_insert_sensor_state()

for i in range(6) :
    for j in range(1, 6) :
        insert_sensor_state.node_id = i
        insert_sensor_state.sensor_id = j
        if j == d_sensor_set["SOLENOIDVALVES"]:
            insert_sensor_state.switcher = d_default_data["DEFAULT_SWITCH"]
        elif j == d_sensor_set["YL69"]:
            insert_sensor_state.capture_frequency = d_default_data["DEFAULT_YL69_PERIOD"]
            insert_sensor_state.threshold = d_default_data["DEFAULT_YL69_THRESHOLD"]
        elif j == d_sensor_set["LIGHT"]:
            insert_sensor_state.capture_frequency = d_default_data["DEFAULT_LIGHT_PERIOD"]
            insert_sensor_state.threshold = d_default_data["DEFAULT_LIGHT_THRESHOLD"]
        elif j == d_sensor_set["THERMISTOR"]:
            insert_sensor_state.capture_frequency = d_default_data["DEFAULT_TEMP_PERIOD"]
            insert_sensor_state.threshold = d_default_data["DEFAULT_TEMP_THRESHOLD"]
        elif j == d_sensor_set["DS18B20"]:
            insert_sensor_state.capture_frequency = d_default_data["DEFAULT_DS18B20_PERIOD"]
            insert_sensor_state.threshold = d_default_data["DEFAULT_DS18B20_THRESHOLD"]
        try:
            db_op.db_insert_sensor_state(insert_sensor_state)
        except Exception, e:
            print e

db_op.db_close()

