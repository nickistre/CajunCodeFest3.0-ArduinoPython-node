__author__ = 'nick'

from message_convert_functions import *

serial_port = "/dev/ttyUSB1"

node_id = 0

devices = {
    1: timer_random,
    2: timer_random,
}

send_interval = 5;

#service_url = "http://codefest.winwithteamwork.com/index.php?option=com_jumi&view=application&fileid=5&Itemid=123"
service_url = "http://localhost:8000/"

bulk_transfer_mode = True