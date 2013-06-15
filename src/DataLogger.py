import os
import sys
import time
import struct

#tos stuff
import sensor_msg
import reply_msg
import request_msg
from tinyos.message import *
from tinyos.message.Message import *
from tinyos.message.SerialPacket import *
from tinyos.packet.Serial import Serial

class DataLogger():
    def __init__(self, motestring):
        self.mif = MoteIF.MoteIF()
        self.tos_source = self.mif.addSource(motestring)
        self.mif.addListener(self, sensor_msg.sensor_msg)
        self.mif.addListener(self, reply_msg.reply_msg)

    def receive(self, src, msg):
        if msg.get_amType() == sensor_msg.AM_TYPE:
            #print msg
            print "###### GET ONE SENSE MESSAGE #######"
            print "# node_id   = %d" % int(msg.get_node_id())
            print "# sensor_id = %d" % int(msg.get_sensor_type())
            print "# data      = %d" % int(msg.get_sensor_value())
            print "####################################"

        elif msg.get_amType() == reply_msg.AM_TYPE:
            print "****** GET ON REPLY MESSAGE ********"
            print "* transaction_number = %d" % int(msg.get_transaction_number())
            print "* node_id            = %d" % int(msg.get_node_id())
            print "* status             = %d" % int(msg.get_status())
            print "* remark             = %d" % int(msg.get_remark())
            print "************************************"

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
        task_to_commit = {}
        task_to_commit["transaction_number"] = 1
        task_to_commit["node_id"] = 1
        task_to_commit["sensor_id"] = 1
        task_to_commit["operation_code"] = 1
        while 1:
            #task_to_commit["operation_data"] = 0
            #self.send(task_to_commit)
            #time.sleep(5)
            #task_to_commit["operation_data"] = 1
            #self.send(task_to_commit)
            time.sleep(5)
            #task_to_commit["operation_data"] = 2
            #self.send(task_to_commit)
            #time.sleep(3)
arg = 'serial@/dev/ttyUSB1:micaz'
def main():
    if '-h' in sys.argv or len(sys.argv) < 1:
        print "Usage:", sys.argv[0], "sf@localhost:micaz"
        sys.exit()

    #dl = DataLogger(sys.argv[1])
    dl = DataLogger(arg)
    dl.main_loop()  # don't expect this to return...

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
