__author__ = 'nick'

import logging
import serial_receiver
import server_push

# TODO: Set this and service url, etc. in a config file
serial_port = "/dev/ttyUSB1"
node_id = 0

# From the perspective of the arduino unit, the host is alwasy device 0
device_id = 0

# Setup logging levels to show to cli
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

logger.info('Starting application')

serial_receiver.init(node_id, serial_port)



# Main app loop
logger.info('Starting main loop')
exit_app = False
while not exit_app:
    serial_receiver.loop_process(node_id)
    server_push.loop_process(node_id)

logger.info('Exiting application')
exit()