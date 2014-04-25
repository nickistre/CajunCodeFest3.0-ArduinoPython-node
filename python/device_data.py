__author__ = 'nick'

from message_convert_functions import *

devices = {}

def convert_data(message):
    device_type_func = devices.get(message.device_id, none)
    return device_type_func(message)
