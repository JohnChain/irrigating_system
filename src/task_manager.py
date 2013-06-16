#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from head import *
from db_operator import *

class task_manager():
    flag = 0
    task_dict = {}

    task_to_commit = {}
    def commit_task(self, db_op, f_send = None):
        for key in self.task_dict.keys():
            try:
                if self.task_dict[key]["status"] == d_task_status["SUBMITTING"]:
                    self.task_dict[key]["status"] = d_task_status["DEALING"]

                    self.task_to_commit["node_id"] = self.task_dict[key]["node_id"]
                    self.task_to_commit["sensor_id"] = self.task_dict[key]["sensor_id"]
                    self.task_to_commit["operation_code"] = self.task_dict[key]["operation_code"]

                    data = self.task_dict[key]["operation_data"]
                    if self.task_to_commit["sensor_id"] == d_sensor_set["THERMISTOR"] and \
                        self.task_to_commit["operation_code"] == d_request_code["SET_READING_THRESHOLD_REQUEST"]:
                        data = d_temp_to_ADC[str(data)]
                    self.task_to_commit["operation_data"] = data
                    self.task_to_commit["transaction_number"] = int(key)
                    print "Next step will send task: number = %s" % (self.task_to_commit["transaction_number"])

                    if f_send != None:
                        f_send(self.task_to_commit)
                        sleep(0.1)
            except KeyError, e:
                pass

    def build_task_list(self, db_op):
        select_task = t_select_task()
        select_task.status = d_task_status["SUBMITTING"]
        #try:
        if 1:
            undone_tasks = db_op.db_select_task(select_task)
        #except Exception, e:
        #except sqlite3.OperationalError, e:
            #print "IN BUILD_TASK CATCHED ERROR: ", e
            #return -1

        task_list = undone_tasks.fetchall()
        len_task_list = len(task_list)
        for n in range(len_task_list):
            if self.flag < MAX_TASK_ID:
                self.flag += 1
            else:
                if len(self.task_dict) == 0:
                    self.flag = 1
                else:
                    break
            print "[%d] TASK_LIST <<< ADDING ONE TASK TO TASK LIST" % n
            one_task = list(task_list[n])
            #print one_task
            flag = str(self.flag)
            temp_task_dict = {}
            temp_task_dict["transaction_number"]  = one_task[0]
            temp_task_dict["node_id"]             = one_task[1]
            temp_task_dict["sensor_id"]           = one_task[2]
            temp_task_dict["operation_code"]      = one_task[3]
            temp_task_dict["operation_data"]      = one_task[4]
            temp_task_dict["status"]              = one_task[5]
            self.task_dict[flag] = temp_task_dict

            update_task = t_update_task()
            update_task.status = int(d_task_status["DEALING"])
            #try:
            if 1:
                update_task.transaction_number = temp_task_dict["transaction_number"]
                #print "before update, update_task tran_num = %s, status = %d" %(update_task.transaction_number, update_task.status)
                db_op.db_update_task(update_task)
                print "DB <<< ONE TASK HAS BEEN UPDATE TO DEALING..."
            #except sqlite3.OperationalError, e:
                #print "While update task in build task: ", e
                #db_op.db_update_task(update_task)
        return 0

    def exchange_task_id(self, key):
        task_id = self.task_dict.pop(key)
        return task_id["transaction_number"]

    def update_tb_sensor_state(self, db_op, task_finished):
        request_code = task_finished.operation_code
        if request_code == d_request_code["SET_SWITCH_STATUS_REQUEST"]:
            db_op.db_update_certain_sensor_state('switcher', task_finished)
        elif request_code == d_request_code["SET_READING_THRESHOLD_REQUEST"]:
            db_op.db_update_certain_sensor_state('threshold', task_finished)
        elif request_code == d_request_code["SET_READING_PERIOD_REQUEST"]:
            db_op.db_update_certain_sensor_state('capture_frequency', task_finished)
        print "DB <<< UPDATED ON SENSOR_STATE"

    def finish_task(self, db_op, task_finished):
        try:
            task_finished.transaction_number = self.exchange_task_id(str(task_finished.transaction_number))
        except KeyError, e:
            return -1
        #try:
        if 1:
            db_op.db_update_task(task_finished)
            print "DB <<< Exchange one and update one"
        #except sqlite3.OperationalError, e:
            #print "IN FINISH_TASK CATCHED ERROR: ", e
            #db_op.db_update_task(task_finished)

#########################
task_mag = task_manager()
#########################


def main():
 db_op = db_operator()
 db_op.db_connect()
 task_mag = task_manager()
 task_finished = t_update_task()
 task_finished.node_id = 1
 task_finished.sensor_id = 3
 task_finished.operation_code = 4
 task_finished.operation_data = 3001
 task_mag.update_tb_sensor_state(db_op, task_finished)

if __name__ == '__main__':
    main()
