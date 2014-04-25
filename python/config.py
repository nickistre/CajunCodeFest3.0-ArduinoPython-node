__author__ = 'nick'

from message_convert_functions import *

serial_ports = [
    "/dev/ttyUSB1",
    "/dev/ttyACM1"
    ]

node_id = 0

devices = {
#  device_id: convert function
    1: timer_random,
    2: timer_random,
    3: motion_sensor,
    4: grocery_scanner
}

send_interval = 600;
error_send_interval = 30;

service_url = "http://codefest.winwithteamwork.com/index.php?option=com_jumi&view=application&fileid=5&Itemid=123"
#service_url = "http://localhost:8000/"

bulk_transfer_mode = False