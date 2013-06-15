#ifndef SMART_IRRIGATION_H
#define SMART_IRRIGATION_H
 
#define RESERVED_LEN 1
 
// list of operation -> request_code
#define SET_SWITCH_STATUS_REQUEST  0x01// 设置传感器开关
#define GET_SWITCH_STATUS_REQUEST  0x02// 获取开关状态
#define GET_READING_REQUEST        0x03// 获取传感器采集的数据
#define SET_READING_PERIOD_REQUEST 0x04// 设置采集的周期
#define GET_READING_PERIOD_REQUEST 0x05// 获取采集的周期
#define SET_READING_THRESHOLD_REQUEST  0x06// 设置阈值
#define GET_READING_THRESHOLD_REQUEST  0x07// 获取阈值
 
 
// list of device number -> request_device
#define SOLENOIDVALVES 0x01 // 电磁阀门
#define YL69           0x02 // 土壤湿度传感器
#define LIGHT          0x03 // 光照
#define THERMISTOR     0x04 // 空气中的温度
#define DS18B20        0x05 // 土壤中的温度
 
#define SUCCESS   0
#define FAIL 1
 
#define OFF 0
#define ON  1
 
 
typedef struct sensor_msg {
    nx_uint16_t node_id;
    nx_uint8_t sensor_type;
    nx_uint16_t sensor_value;
    nx_uint16_t reserved[RESERVED_LEN];
} sensor_msg_t;
 
typedef struct request_msg {
    nx_uint16_t node_id;
    nx_uint16_t transaction_number;
    nx_uint8_t request_code;
    nx_uint8_t request_device;
    nx_uint16_t request_data;
    nx_uint16_t reserved[RESERVED_LEN];
} request_msg_t;
 
typedef struct reply_msg {
    nx_uint16_t node_id;
    nx_uint16_t trasaction_number;
    nx_uint8_t status;
    nx_uint16_t remark; // 备注, 出现错误， 给出更具体的提示, 备用
    nx_uint16_t reserved[RESERVED_LEN];
} reply_msg_t;
