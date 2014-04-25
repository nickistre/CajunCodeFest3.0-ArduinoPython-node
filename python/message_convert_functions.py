__author__ = 'nick'

import logging
import json
import math

logger = logging.getLogger(__name__)

def timer_random(message):
    logger.info('convert data to long int')
    old_data = json.loads(message.data)

    data_number = int.from_bytes(old_data, byteorder='little', signed=False)


    logger.debug('Final value is %d'%(data_number))
    message.data = data_number

    return message;

def motion_sensor(message):
    logger.info('convert data to longs, mean & standard deviation');

    old_data = json.loads(message.data)
    mean_data = old_data[0:4]
    std_dev_data = old_data[4:8];

    mean = int.from_bytes(mean_data, byteorder='little', signed=True)
    std_dev = int.from_bytes(std_dev_data, byteorder='little', signed=True)

    data = json.dumps({'mean': mean, 'std_dev': std_dev})
    logger.debug('Converted values: %s'%data);

    message.data = data

    return message;

def trash_scale(message):
    # TODO: Stub
    return message;

def pill_scale(message):
    # TODO: Stub
    return message

def pill_box(message):
    logger.info('convert data to a string')
    old_data = json.loads(message.data)

    logger.debug('old data: %s'%repr(old_data))

    value = ''.join(chr(i) for i in old_data);

    logger.debug('value from data: %s'%value)

    message.data = value;
    return message

def grocery_scanner(message):
    logger.info('Grocery RFID scanner, no change to message')
    return message

def trash_scanner(message):
    logger.info('Trash RFID scanner, no change to message')
    return message

def none(message):
    logger.info('No change to message')
    return message;