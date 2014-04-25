__author__ = 'nick'

import buffer
import logging
import time
import urllib.request
import urllib.parse
import json

logger = logging.getLogger(__name__)

# TODO: Store on drive
last_send_time = None;

# Number of seconds to wait between sends
send_interval = 5

#service_url = "http://localhost/quantum"
service_url = "http://codefest.winwithteamwork.com/components/com_jumi/files/node-service.php"


def loop_process(node_id):
    check_important(node_id)
    check_time(node_id)
    pass


def check_important(node_id):
    if buffer.important_count() > 0:
        logger.info('%d important messages in buffer, starting send now'%buffer.important_count())
        messages = buffer.important_get_all()
        send_messages(messages)

def check_time(node_id):
    if last_send_time == None:
        logger.debug('No last_send_time set, sending all messages currenltly in buffer')
        messages = buffer.get_all()
        send_messages(messages, node_id)
        update_last_send_time()
    else:
        if (time.time() - last_send_time > send_interval):
            logger.debug('More than %d seconds since last send, sending now')
            messages=buffer.get_all()
            send_messages(messages, node_id)
            update_last_send_time()



def send_messages(messages, node_id):
    if len(messages) > 0:
        logger.info('Sending %d messages to server'%len(messages))

        data_messages = []


        for message in messages:
            data_message = {
                'device_id': message.device_id,
                'node_id': node_id,
                'message': json.dumps(message.data),
                'recorded_ts': message.recorded_ts
            };

        data=urllib.parse.urlencode({"messages": data_messages}).encode('utf-8')

        logger.debug('Connecting to service url: %s'%service_url)
        service_request = urllib.request.Request(
            service_url,
        )
        service_request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
        response_stream = urllib.request.urlopen(service_request, data)

def update_last_send_time():
    global last_send_time
    last_send_time = time.time()
    logger.debug('Updated last_send_time to: %d'%last_send_time)