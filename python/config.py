__author__ = 'nick'

from message_convert_functions import *

serial_ports = [
    "/dev/ttyUSB0",
    "/dev/ttyACM1"
    ]

node_id = 1

devices = {
#  device_id: convert function
    1: timer_random,
    2: timer_random,
    51: motion_sensor,
    4: trash_scanner,
    5: pill_box
}

send_interval = 300;
error_send_interval = 15;

service_url = "http://codefest.winwithteamwork.com/index.php?option=com_jumi&view=application&fileid=5&Itemid=123"
#service_url = "http://localhost:8000/"

bulk_transfer_mode = False