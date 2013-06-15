/*drop database if exists irrigating_system;*/
/*create database irrigating_system;*/
/*use irrigating_system;*/

drop database if exists test;
create database test;
use test;

drop table if exists tb_sensor_state;
CREATE TABLE if not exists tb_sensor_state ( 
    node_id             INTEGER  NOT NULL, 
    sensor_id           INTEGER  NOT NULL, 
    switcher            INTEGER  DEFAULT  1 , 
    capture_frequency   INTEGER  DEFAULT  -1 , 
    threshold           DOUBLE   DEFAULT  -1 , 
    insert_time         DATETIME NOT NULL, 
    PRIMARY KEY ( node_id, sensor_id )   
    );

drop table if exists tb_history_data;
CREATE TABLE if not exists tb_history_data ( 
    record_id   INTEGER  PRIMARY KEY AUTO_INCREMENT NOT NULL UNIQUE,
    insert_time DATETIME NOT NULL,
    node_id     INTEGER  NOT NULL,
    sensor_id   INTEGER  NOT NULL,
    data        REAL     NOT NULL DEFAULT  -1000  
    );

drop table if exists tb_realtime_data;
CREATE TABLE if not exists tb_realtime_data ( 
    node_id     INTEGER  NOT NULL,
    sensor_id   INTEGER  NOT NULL,
    data        REAL     NOT NULL DEFAULT  -1000 ,
    insert_time DATETIME NOT NULL,
    PRIMARY KEY ( node_id, sensor_id )   
    );

drop table if exists tb_task;
CREATE TABLE if not exists tb_task ( 
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
    );

CREATE INDEX idx_tb_task_status ON tb_task ( 
    status 
);

CREATE UNIQUE INDEX idx_tb_task_trans_num ON tb_task ( 
    transaction_number 
);

CREATE INDEX idx_tb_history_data ON tb_history_data ( 
    insert_time,
    node_id 
);

delimiter ;;

drop trigger if exists trg_task_insert_sensor_state;;
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

drop trigger if exists trg_history_insert_realtime;;
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

delimiter ;

