#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sensor_msg
import reply_msg
import request_msg
from tinyos.message import *
from tinyos.message.Message import *
from tinyos.message.SerialPacket import *
from tinyos.packet.Serial import Serial

from head import *
from task_manager import *
from db_operator import *
from thread_manager import thread_manager

class serial_operator(object):
    thread_mag = thread_manager()
    def __init__(self, motestring):
        self.mif = MoteIF.MoteIF()
        self.tos_source = self.mif.addSource(motestring)
        self.mif.addListener(self, sensor_msg.sensor_msg)
        self.mif.addListener(self, reply_msg.reply_msg)

    def receive(self, src, msg):
        if msg.get_amType() == sensor_msg.AM_TYPE:
            insert_data = t_insert_data()
            insert_data.node_id    = int(msg.get_node_id())
            insert_data.sensor_id  = int(msg.get_sensor_type())
            insert_data.data       = int(msg.get_sensor_value())

            #if insert_data.sensor_id == d_sensor_set["THERMISTOR"]:
                #insert_data.data = float("%.2f" % Celsius(insert_data.data))
            #print msg
            print "###### GET ONE SENSE MESSAGE #######"
            print "# node_id   = %d" % insert_data.node_id
            print "# sensor_id = %s" % d_sensor_num_to_name[str(insert_data.sensor_id)]
            print "# data      = %d" % insert_data.data
            print "####################################"
            #try:
            if 1:
                db_op = db_operator()
                db_op.db_connect()
                db_op.db_insert_data(insert_data)
                db_op.db_close()
                print "DB <<<<<<<<< ONE DATA INSERTED"
            #except sqlite3.OperationalError, e:
                #print e

        elif msg.get_amType() == reply_msg.AM_TYPE:
            print msg
            task_finished = t_update_task()
            task_finished.transaction_number = int(msg.get_transaction_number())
            task_finished.status             = int(msg.get_status())

            task_finished.node_id            = int(msg.get_node_id())
            task_finished.sensor_id          = int(msg.get_request_device())
            task_finished.request_code       = int(msg.get_request_code())
            task_finished.request_data       = int(msg.get_request_data())

            print "****** GET ON REPLY MESSAGE ********"
            print "* transaction_number = %d" % int(msg.get_transaction_number())
            print "* node_id            = %d" % int(msg.get_node_id())
            print "* status             = %d" % int(msg.get_status())
            print "* remark             = %d" % int(msg.get_remark())
            print "************************************"

            self.thread_mag.upword(task_finished)

        sys.stdout.flush()

    def send(self, task_to_commit):
        smsg = request_msg.request_msg()
        smsg.set_transaction_number(int(task_to_commit["transaction_number"]))
        smsg.set_node_id(int(task_to_commit["node_id"]))
        smsg.set_request_device(int(task_to_commit["sensor_id"]))
        smsg.set_request_code(int(task_to_commit["operation_code"]))
        smsg.set_request_data(int(task_to_commit["operation_data"]))

        self.mif.sendMsg(self.tos_source, 0xFFFF, smsg.get_amType(), 0, smsg)
        print "SENT ONE REQUEST >>>>>>>> HARDWARE"

    def main_loop(self):
        self.thread_mag.downword(self.send)

def main():
    if '-h' in sys.argv or len(sys.argv) < 1:
        print "Usage:", sys.argv[0], "[ serial | sf ]@[ dev | IP ]:[ micaz | PORT ]"
        sys.exit()

    dl = serial_operator(sys.argv[1])
    dl.main_loop()  # don't expect this to return...

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass


##############################
#serial_op = serial_operator()
##############################