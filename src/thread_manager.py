#!/usr/bin/env python
# -*- coding: utf-8 -*-

from head import *
from task_manager import *
from db_operator import *

class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def getResult(self):
        return self.res

    def run(self):
        print 'STARTING', self.name, 'AT:',
        self.res = apply(self.func, self.args)
        print self.name, 'FINISHED AT:', datetime.now()

class thread_manager(object):
    thread_list = []
    def downword(self, f_send = None):
        print "############ NOW WE ARE IN DOWNWORD THREAD ################"
        db_op = db_operator()
        try:
            while True:
                db_op.db_connect()
                task_mag.build_task_list(db_op)
                task_mag.commit_task(db_op, f_send)
                db_op.db_close()
                sleep(0.5)
        #except Exception, e:
            #print e
        finally:
            print "DOWNWORD THREAD FINISHED"
            #db_op.db_close()

    def upword(self, task_finished):
        print "############ NOW WE ARE IN UPWORD THREAD ################"
        db_op = db_operator()
        #try:
        if 1:
            #while True:
            if 1:
                db_op.db_connect()
                #print "TASK_DICT: ", str(task_mag.task_dict)
                #transaction_number = raw_input("Please input the transaction_number:")
                task_mag.finish_task(db_op, task_finished)
                task_mag.update_tb_sensor_state(db_op, task_finished)
                db_op.db_close()
        #finally:
            #print "Upword thread finished"
            #db_op.db_close()

    def init_thread_list(self):
        self.thread_list.append( MyThread(self.downword,(),self.downword.__name__) )
        self.thread_list.append( MyThread(self.upword,(),self.upword.__name__) )

    def start_thread(self):
        thread_num = len(self.thread_list)
        for i in range(thread_num):
            self.thread_list[i].start()

def test_thread_manager():
    thread_mag = thread_manager()
    thread_mag.init_thread_list()
    thread_mag.start_thread()
    thread_mag.thread_list[0].join()
    thread_mag.thread_list[1].join()
if __name__ =='__main__':
    test_thread_manager()

