__author__ = 'nick'

import logging
import serial_receiver
import server_push
import device_data
import config


# TODO: Set this and service url, etc. in a config file




# From the perspective of the arduino unit, the host is alwasy device 0
device_id = 0

# Setup logging levels to show to cli
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

logger.info('Starting application')

serial_receiver.init(config.node_id, config.serial_ports)

server_push.send_interval = config.send_interval

server_push.error_send_interval = config.error_send_interval

server_push.service_url = config.service_url

server_push.bulk_transfer_mode = config.bulk_transfer_mode


# Update device_data module
device_data.devices = config.devices

# Main app loop
logger.info('Starting main loop')
exit_app = False
while not exit_app:
    serial_receiver.loop_process(config.node_id)
    server_push.loop_process(config.node_id)

logger.info('Exiting application')
exit()