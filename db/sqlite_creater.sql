
-- Table: tb_sensor_state
CREATE TABLE tb_sensor_state ( 
    node_id           INTEGER          NOT NULL,
    sensor_id         INTEGER          NOT NULL,
    switcher          INTEGER( 0, 1 )  DEFAULT ( 1 ),
    capture_frequency INTEGER          DEFAULT ( -1 ),
    threshold         REAL             DEFAULT ( -1 ),
    insert_time       DATETIME         NOT NULL,
    PRIMARY KEY ( node_id, sensor_id )  ON CONFLICT IGNORE 
);


-- Table: tb_history_data
CREATE TABLE tb_history_data ( 
    record_id   INTEGER  PRIMARY KEY AUTOINCREMENT
                         NOT NULL
                         UNIQUE,
    insert_time DATETIME NOT NULL,
    node_id     INTEGER  NOT NULL,
    sensor_id   INTEGER  NOT NULL,
    data        REAL     NOT NULL
                         DEFAULT ( -1000 ) 
);


-- Table: tb_realtime_data
CREATE TABLE tb_realtime_data ( 
    node_id     INTEGER  NOT NULL,
    sensor_id   INTEGER  NOT NULL,
    data        REAL     NOT NULL
                         DEFAULT ( -1000 ),
    insert_time DATETIME NOT NULL,
    PRIMARY KEY ( node_id, sensor_id )  ON CONFLICT REPLACE 
);


-- Table: tb_task
CREATE TABLE tb_task ( 
    transaction_number VARCHAR          NOT NULL
                                        UNIQUE,
    node_id            INTEGER          NOT NULL,
    sensor_id          INTEGER          NOT NULL,
    operation_code     INTEGER          NOT NULL,
    operation_data     INTEGER,
    status             INTEGER( 0, 3 )  CHECK ( 0 <= status 
                                            AND
                                        status <= 3 ) 
                                        DEFAULT ( 3 ),
    remark             VARCHAR,
    reversed           INTEGER,
    insert_time        DATETIME,
    PRIMARY KEY ( transaction_number ) 
);


-- Index: idx_tb_task_status
CREATE INDEX idx_tb_task_status ON tb_task ( 
    status 
);


-- Index: idx_tb_task_trans_num
CREATE UNIQUE INDEX idx_tb_task_trans_num ON tb_task ( 
    transaction_number 
);


-- Index: idx_tb_history_data
CREATE INDEX idx_tb_history_data ON tb_history_data ( 
    insert_time,
    node_id 
);


-- Trigger: trg_record_insert_sensor_state
CREATE TRIGGER trg_record_insert_sensor_state
       BEFORE INSERT ON tb_history_data
       FOR EACH ROW
BEGIN
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
END;
;


-- Trigger: trg_record_insert_realtime
CREATE TRIGGER trg_record_insert_realtime
       AFTER INSERT ON tb_history_data
       FOR EACH ROW
BEGIN
    INSERT INTO tb_realtime_data VALUES ( 
        new.node_id,
        new.sensor_id,
        new.data,
        new.insert_time 
    );
END;
;

