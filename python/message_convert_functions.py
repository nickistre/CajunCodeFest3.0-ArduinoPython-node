__author__ = 'nick'

import logging
import json
import math

logger = logging.getLogger(__name__)

def timer_random(message):
    logger.info('convert data to long int')
    old_data = json.loads(message.data)

    current_shift = 0;
    data_number = 0;

    for x in old_data:
        value = x * pow(2, current_shift)
        logger.debug('%d * pow(%d, %d) = %d'%(value, 2, current_shift, value));
        data_number = data_number + value
        current_shift = current_shift + 8

    logger.debug('Final value is %d'%(data_number))
    message.data = data_number

    return message;

def motion_sensor(message):
    # TODO: Stub
    return message;

def trash_scale(message):
    # TODO: Stub
    return message;

def pill_scale(message):
    # TODO: Stub
    return message

def grocery_scanner(message):
    logger.info('Grocery RFID scanner, no change to message')
    return message

def none(message):
    logger.info('No change to message')
    return message;