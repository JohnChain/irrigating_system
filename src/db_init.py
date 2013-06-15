from head import *

handler = None
cursor = None

drop_db = "drop database if exists irrigating_system;"
create_db = " create database irrigating_system;"
grant_priv = "grant all privileges on %s.* to %s identified by %s" \
        %(db_name, user + "@" + "'%'", "'" + user_password + "'")

str_sql_use_db = "use irrigating_system"

str_sql_drop_tb_sensor_state = " drop table if exists %s.%s " %(db_name, tb_sensor_state)
str_sql_create_tb_sensor_state = '''
CREATE TABLE if not exists %s.%s (
    node_id             INTEGER  NOT NULL,
    sensor_id           INTEGER  NOT NULL,
    switcher            INTEGER  DEFAULT  1 ,
    capture_frequency   INTEGER  DEFAULT  -1 ,
    threshold           DOUBLE   DEFAULT  -1 ,
    insert_time         DATETIME NOT NULL,
    PRIMARY KEY ( node_id, sensor_id )
    )ENGINE = INNODB CHARACTER SET utf8 COLLATE utf8_general_ci
    ''' %(db_name, tb_sensor_state)

str_sql_drop_tb_history_data = " drop table if exists %s.%s " %(db_name, tb_history_data)
str_sql_create_tb_history_data = '''
CREATE TABLE if not exists %s.%s (
    record_id   INTEGER  PRIMARY KEY AUTO_INCREMENT NOT NULL UNIQUE,
    insert_time DATETIME NOT NULL,
    node_id     INTEGER  NOT NULL,
    sensor_id   INTEGER  NOT NULL,
    data        REAL     NOT NULL DEFAULT  -1000
    )ENGINE = INNODB CHARACTER SET utf8 COLLATE utf8_general_ci
    ''' %(db_name, tb_history_data)

str_sql_drop_tb_realtime_data = " drop table if exists %s.%s " %(db_name, tb_realtime_data)
str_sql_create_tb_realtime_data = '''
CREATE TABLE if not exists %s.%s (
    node_id     INTEGER  NOT NULL,
    sensor_id   INTEGER  NOT NULL,
    data        REAL     NOT NULL DEFAULT  -1000 ,
    insert_time DATETIME NOT NULL,
    PRIMARY KEY ( node_id, sensor_id )
    )ENGINE = INNODB CHARACTER SET utf8 COLLATE utf8_general_ci
    ''' %(db_name, tb_realtime_data)

str_sql_drop_tb_task = " drop table if exists %s.%s " %(db_name, tb_task)
str_sql_create_tb_task = '''
CREATE TABLE if not exists %s.%s (
    transaction_number VARCHAR(50)      NOT NULL ,
    node_id            INTEGER          NOT NULL,
    sensor_id          INTEGER          NOT NULL,
    operation_code     INTEGER          NOT NULL,
    operation_data     INTEGER,
    status             INTEGER   DEFAULT  3 ,
    remark             VARCHAR(20),
    reversed           INTEGER,
    insert_time        DATETIME,
    PRIMARY KEY ( transaction_number )
    )ENGINE = INNODB CHARACTER SET utf8 COLLATE utf8_general_ci
    ''' %(db_name, tb_task)

str_sql_creater_idx_tb_task_status = '''CREATE INDEX idx_tb_task_status ON tb_task ( status ); '''
str_sql_creater_idx_tb_task_trans_num = '''CREATE UNIQUE INDEX idx_tb_task_trans_num ON tb_task ( transaction_number );'''
str_sql_creater_idx_tb_history_data = ''' CREATE INDEX idx_tb_history_data ON tb_history_data ( insert_time, node_id ); '''

def connect_db():
    try:
        global handler
        global cursor
        handler = MySQLdb.connect(host, admin, admin_password)
        cursor = handler.cursor()
        cursor.execute("select version()")
        vers = cursor.fetchone()
        print "database version is: %s" %vers
        return 0
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        return -2
    #finally:
        #if handler:
            #handler.close()

def init_db():
    try:
        cursor.execute(drop_db)
        cursor.execute(create_db)
        cursor.execute(grant_priv)
        cursor.execute(create_table_user)
        handler.commit()
        print "Databases initiated!"
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        return -1

if __name__ == '__main__':
    init_db()
