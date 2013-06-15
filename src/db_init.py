from head import *

handler = None
cursor = None

drop_db = '''
    drop database if exists irrigating_system;
    '''
create_db = '''
    create database irrigating_system;
    '''
grant_priv = "grant all privileges on %s.* to %s identified by %s" \
        %(db_name, user + "@" + "'%'", "'" + user_password + "'")

create_table_user = '''
    create table %s.%s(
    uid             bigint      auto_increment primary key,
    name            varchar(20) ,
    password        varchar(50) ,
    email           varchar(100),
    registe_time    timestamp   DEFAULT CURRENT_TIMESTAMP,
    last_log_time   datetime    ,
    last_log_ip     char(20)
    )ENGINE = INNODB CHARACTER SET utf8 COLLATE utf8_general_ci
    ''' %(db_name, tb_name)

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
