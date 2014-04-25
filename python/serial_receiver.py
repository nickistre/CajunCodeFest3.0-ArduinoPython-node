__author__ = 'nick'
"""Code to manage receiving data from the arduino reciever via serial"""

import logging
from device.serial import DeviceSerial
import buffer
import device_data

logger = logging.getLogger(__name__)

device = None
"""
@type device: DeviceSerial
"""

def init(device_id, serial_port):
    global device
    device = DeviceSerial(device_id, serial_port)
    logger.debug('Pinging device to check if ready')
    device.send_message('ready?', 'device')

def loop_process(node_id):
    if device.message_waiting():
        message = device.receive_message()
        logger.debug('Received message')

        if message.type == 'log':
            device_logger = logging.getLogger('device-%d' % message.device_id)
            device_logger.debug(message.data)

        elif message.type == 'data':
            logger.info('Recieved data from device: %d' % message.device_id)
            message = device_data.convert_data(message)
            buffer.append(message)
        elif message.type == 'device':
            logger.info('Message from device %d: %s' % ( message.device_id, message.data))

        else:
            logger.warning('Unhandled message: %s' % vars(message))