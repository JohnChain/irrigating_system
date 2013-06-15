#!/usr/bin/env python
# -*- coding: utf-8 -*-

from head import *

class db_operator(object):
    def db_connect(self):
        #self.handler = sqlite3.connect(DB_PATH, check_same_thread = False)
        #self.handler = sqlite3.connect('/home/johnchain/Templates/icecream/irrigation.db', check_same_thread = False)
        d_db_conn = d_db_conn_local
        self.handler = MySQLdb.connect(d_db_conn["HOST"], d_db_conn["USER"], d_db_conn["PASSWORD"], d_db_conn["DATABASE"])

        self.select_cur = self.handler.cursor()
        self.update_cur = self.handler.cursor()
        self.insert_cur = self.handler.cursor()
        return self.handler, self.select_cur, self.update_cur, self.insert_cur

    def db_init(self):
        #try:
        if 1:
            for line in open(MYSQL_SQL_PATH):
                #self.update_cur.execute(line)
            #self.handler.commit()
                print "^^^^^^^^^^^^^^^^^"
                print line
        #except sqlite3.OperationalError, e:
            #print e

    ###################################################################
    def db_insert_data(self, data):
        ''' data:
                node_id
                sensor_id
                data
        '''
                    #values(?, ?, ?, ?)
        #now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now_time = datetime.now().strftime("%Y%m%d%H%M%S")
        sql_str = r'''
                    insert into tb_history_data( insert_time, node_id, sensor_id, data) values('%s', %d, %d, %f)
                ''' % (now_time, data.node_id, data.sensor_id, data.data)
        self.insert_cur.execute( sql_str)
        self.handler.commit()

    def db_insert_task(self, task):
        ''' task:
                transaction_number
                node_id
                sensor_id
                operation_code
                operation_data
                status
        '''
        operating_time = datetime.now().strftime("%Y%m%d%H%M%S")
        str_sql = r'''
                    insert into tb_task(
                                                transaction_number,
                                                insert_time,
                                                node_id,
                                                sensor_id,
                                                operation_code,
                                                operation_data,
                                                status)
                    values('%s', '%s', %d, %d, %d, %d, %d)
                ''' % (task.transaction_number, \
                                   operating_time, \
                                   task.node_id, \
                                   task.sensor_id, \
                                   task.operation_code, \
                                   task.operation_data, \
                                   task.status)
        self.insert_cur.execute(str_sql)
        self.handler.commit()

    def db_insert_sensor_state(self, condition):
        '''condition:
                node_id
                sensor_id
                switcher
                capture_frequency
                threshold
        '''
        str_sql = r'''
                    insert into tb_sensor_state(
                            node_id,
                            sensor_id,
                            switcher,
                            capture_frequency,
                            threshold)
                    values(%d, %d, %d, %d, %d)
                '''%(condition.node_id, condition.sensor_id, condition.switcher, condition.capture_frequency, condition.threshold)
        result = self.update_cur.execute(str_sql )
        self.handler.commit()
        return result


    ###################################################################
    def db_select_task_status(self, task):
        ''' task:
                transaction_number
        '''
        str_sql = r'''
                    select  node_id, status from tb_task
                        where transaction_number = '%s'
                '''%(task.transaction_number)
        result = self.select_cur.execute(str_sql)
        return self.select_cur

    def db_select_task(self, task):
        ''' task:
                status
        '''
        str_sql = r'''
                    select  transaction_number,
                            node_id,
                            sensor_id,
                            operation_code,
                            operation_data,
                            status,
                            insert_time
                    from tb_task
                        where status = %d
                '''%(task.status)
        result = self.select_cur.execute(str_sql )
        return self.select_cur

    def db_select_realtime_data(self, data):
        ''' data:
                node_id
        '''
        str_sql = r'''
                    select node_id, sensor_id, data, insert_time from tb_realtime_data
                        where node_id = %d
                '''%(data.node_id)
        result = self.select_cur.execute(str_sql)
        return self.select_cur

    def db_select_history_data(self, data):
        ''' data:
                 node_id
                 start_time
                 end_time
         '''
        str_sql = r'''
                     select node_id, sensor_id, data, insert_time from tb_history_data
                     where node_id = %d and insert_time >= '%s' and insert_time <= '%s'
                 ''' % (data.node_id, data.start_time, data.end_time)
        result = self.select_cur.execute(str_sql)
        return self.select_cur

    def db_select_history_data_sensor(self, data):
        ''' data:
                 node_id
                 sensor_id
                 start_time
                 end_time
         '''
        str_sql = r'''
                     select node_id, sensor_id, data, insert_time from tb_history_data
                     where node_id = %d and sensor_id = %d and insert_time >= '%s' and insert_time <= '%s'
                 ''' % (data.node_id,data.sensor_id, data.start_time, data.end_time)
        result = self.select_cur.execute(str_sql)
        return self.select_cur

    def db_select_all_history_data(self, condition):
        ''' condition:
                node_id
        '''
        str_sql = r'''
                     select node_id, sensor_id, data, insert_time from tb_history_data
                         where node_id = %d
                         order by insert_time
                 '''% (condition.node_id)
        result = self.select_cur.execute(str_sql )
        return self.select_cur

    def db_select_sensor_state(self, condition):
        '''condition:
                node_id
        '''
        str_sql = r'''
                     select node_id ,sensor_id, switcher, capture_frequency, threshold from tb_sensor_state
                     where node_id = %d
                 '''%(condition.node_id)
        result = self.select_cur.execute(str_sql)
        return self.select_cur

    def db_select_node_sensor(self, node_id):
        str_sql = r'''
                    select sensor_id from tb_realtime_data
                    where node_id = %d
                    '''
        result = self.select_cur.execute(str_sql, [node_id])
        return self.select_cur

    def db_select_node(self):
        str_sql = r'''
                    select distinct(node_id) from tb_realtime_data
                    '''
        result = self.select_cur.execute(str_sql)
        return self.select_cur

    ###################################################################
    def db_update_task(self, condition):
        '''condition:
                transaction_number
                status
        '''
        str_sql = r'''
                    update tb_task
                    set status = %d
                    where transaction_number = '%s'
                ''' % (condition.status, condition.transaction_number)
        result = self.update_cur.execute(str_sql)
        self.handler.commit()
        return result

    def db_update_certain_sensor_state(self, sensor_name, condition):
        '''condition:
                node_id
                sensor_id
                state
        '''
        str_sql = r'''
                    update tb_sensor_state
                    set %s = %d
                    where  node_id = %d and sensor_id = %d
                ''' %(sensor_name, condition.operation_data, condition.node_id, condition.sensor_id)
        result = self.update_cur.execute(str_sql)
        self.handler.commit()
        return result

    ###################################################################
    def db_close(self):
        if self.handler:
            self.select_cur.close()
            self.insert_cur.close()
            self.update_cur.close()
            self.handler.close()

    ###################################################################
#######################
#db_op = db_operator()
#######################

def main():
    ############################ Testing Data #######################################
    #command_time = datetime.now().strftime("%Y%m%d%H%M%S")

    #insert_data = t_insert_data()
    #insert_data.node_id     = 3
    #insert_data.sensor_id   = d_sensor_set["LIGHT"]
    #insert_data.data        = 3

    #select_sensor_state = t_select_sensor_state()
    #select_sensor_state.node_id             = 3

    #update_sensor_state                     = t_update_sensor_state()
    #update_sensor_state.node_id             = 1
    #update_sensor_state.sensor_id           = d_sensor_set["YL69"]
    #update_sensor_state.switcher            = d_switcher["ON"]
    #update_sensor_state.capture_frequency   = 2
    #update_sensor_state.threshold           = 4

    #select_history_data = t_select_history_data()
    #select_history_data.node_id     = 3
    #select_history_data.start_time  = '20130605102821'
    #select_history_data.end_time    = command_time

    #insert_task = t_insert_task()
    #insert_task.transaction_number  = r'90CE96FE-ACF7-404E-A68F-46531118E013'
    #insert_task.node_id             = 1
    #insert_task.sensor_id           = d_sensor_set["SOLENOIDVALVES"]
    #insert_task.operation_code      = 1
    #insert_task.operation_data      = 1
    #insert_task.status = d_task_status["SUBMITTING"]

    #select_task_status                      = t_select_task_status()
    #select_task_status.transaction_number   = command_time

    #select_task                             = t_select_task()
    #status                                  = d_task_status["SUBMITTING"]

    #select_all_history_data                 = select_sensor_state
    #select_all_history_data.node_id         = 3

    #update_task                             = t_update_task()
    #update_task.transaction_number          = command_time
    #update_task.status                      = d_task_status["SUCCEED"]
    ################################################################################


    db = db_operator()
    #db.db_connect()
    #db.select_cur.execute("select version()")
    #vers = db.select_cur.fetchone()
    #print "database version is: %s" %vers
    db.db_init()
    #try:
        #db.db_init()
    #except sqlite3.OperationalError, e:
        #print e
    #try:
        #db.db_insert_data(insert_data)
        #db.db_insert_task(insert_task)
        #db.db_insert_sensor_state(insert_sensor_state)
        #db.db_update_task(update_task)

        #result2 = db.db_select_realtime_data(select_sensor_state)
        #print 'realtime data: %r' % str(list(result2.fetchall()))

        #result3 = db.db_select_sensor_state(select_sensor_state)
        #print 'sensor  state: %r' % str(list(result3.fetchall()))

        #result1 = db.db_select_history_data(select_history_data)
        #print 'history  data: %r' % (list(result1.fetchall()))

        #result5 = db.db_select_task(select_task)
        #print 'task     data: %r' % str(list(result5.fetchall()))

        #result6 = db.db_select_task_status(select_task_status)
        #print 'task   status: %r' % str(list(result6.fetchall()))

        #result7 = db.db_select_all_history_data(select_all_history_data)
        #print 'all history data: %r' %str(list(result7.fetchall()))
        #result8 = db.db_select_node()
        #print "select all node: %r" % str(list(result8.fetchall()))

        #print '%r' %command_time
    #finally:
        #db.db_close()

if __name__ == '__main__':
    main()
