from head import *

db_name             = 'hehe'
tb_sensor_state     = 'tb_sensor_state'
tb_history_data     = 'tb_history_data'
tb_realtime_data    = 'tb_realtime_data'
tb_task             = 'tb_task'

user = 'guest'
user_password = 'guest'

handler = None
cursor = None

str_sql_drop_db = "drop database if exists %s;" % db_name
str_sql_create_db = " create database %s;" % db_name
str_sql_grant_priv = "grant all privileges on %s.* to %s identified by %s" \
        %(db_name, user + "@" + "'%'", "'" + user_password + "'")

str_sql_use_db = "use %s" % db_name

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

str_sql_drop_trg_task_insert_sensor_state = "drop trigger if exists trg_task_insert_sensor_state;;"
str_sql_create_trg_task_insert_sensor_state = '''
CREATE TRIGGER trg_task_insert_sensor_state
       BEFORE INSERT ON tb_task
       FOR EACH ROW
BEGIN
    declare amount int;
    set amount = 0;
    select count(node_id) from tb_sensor_state
        where node_id = new.node_id and sensor_id = new.sensor_id
        into amount;
    if amount = 0 then
        INSERT INTO tb_sensor_state (
            node_id,
            sensor_id,
            insert_time
        )
        VALUES (
            new.node_id,
            new.sensor_id,
            new.insert_time
        );
    end if;
END;;
'''

str_sql_drop_trg_history_insert_realtime = " drop trigger if exists trg_history_insert_realtime;;"

str_sql_create_trg_history_insert_realtime = '''
CREATE TRIGGER trg_history_insert_realtime
       BEFORE INSERT ON tb_history_data
       FOR EACH ROW
BEGIN
    declare amount int;
    set amount = 0;
    select count(node_id) from tb_realtime_data
        where node_id = new.node_id and sensor_id = new.sensor_id
        into amount;

    if amount = 1 then
        update tb_realtime_data
        set data = new.data,
            insert_time = new.insert_time
        where node_id = new.node_id and sensor_id = new.sensor_id;
    else
        INSERT INTO tb_realtime_data VALUES (
            new.node_id,
            new.sensor_id,
            new.data,
            new.insert_time
        );
    end if;
END;;
'''

def connect_db():
    try:
        global handler
        global cursor
        handler = MySQLdb.connect('localhost', 'root','johnchain')
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
    connect_db()
    global handler
    global cursor
    try:
        cursor.execute(str_sql_drop_db)
        cursor.execute(str_sql_create_db)
        cursor.execute(str_sql_grant_priv)
        cursor.execute(str_sql_use_db)
        cursor.execute(str_sql_create_tb_sensor_state)
        cursor.execute(str_sql_create_tb_history_data)
        cursor.execute(str_sql_create_tb_realtime_data)
        cursor.execute(str_sql_create_tb_task)
        cursor.execute(str_sql_creater_idx_tb_task_status)
        cursor.execute(str_sql_creater_idx_tb_history_data)
        cursor.execute(str_sql_creater_idx_tb_task_trans_num)
        cursor.execute(str_sql_drop_trg_task_insert_sensor_state)
        cursor.execute(str_sql_create_trg_task_insert_sensor_state)
        cursor.execute(str_sql_drop_trg_history_insert_realtime)
        cursor.execute(str_sql_create_trg_history_insert_realtime)

        handler.commit()
        print "Databases initiated!"
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        return -1

if __name__ == '__main__':
    init_db()
