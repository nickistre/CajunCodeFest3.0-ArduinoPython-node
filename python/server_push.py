from apport.crashdb import URLError

__author__ = 'nick'

import buffer
import logging
import time
import urllib.request
import urllib.parse
import urllib
from urllib.error import HTTPError
from urllib.error import URLError
import json

logger = logging.getLogger(__name__)

# TODO: Store on drive
next_send_time = None;

# Number of seconds to wait between sends
send_interval = 3600

error_send_interval = 30

service_url = "http://localhost/test"

bulk_transfer_mode = False

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
    if next_send_time == None:
        logger.debug('No last_send_time set, sending all messages currently in buffer')
        if (bulk_transfer_mode):
            messages = buffer.get_all()
            send_messages(messages, node_id)
            update_last_send_time(send_interval)
        else:
            if (buffer.count() > 0):
                message = buffer.get()
                send_message(message, node_id)
                if (buffer.count() == 0):
                    update_last_send_time(send_interval)
            else:
                update_last_send_time(send_interval)

    else:
        if (time.time() - next_send_time >= 0):
            logger.debug('Next planned time passed, sending now')
            if (bulk_transfer_mode):
                messages=buffer.get_all()
                send_messages(messages, node_id)
                update_last_send_time(send_interval)
            else:
                if (buffer.count() > 0):
                    message = buffer.get()
                    send_message(message, node_id)
                    if (buffer.count() == 0):
                        update_last_send_time(send_interval)
                else:
                    logger.debug('No messages in buffer to send')
                    update_last_send_time(send_interval)


def send_message(message, node_id):
    data_message = {
        'device_id': message.device_id,
        'node_id': node_id,
        'message': message.data,
        'recorded_ts': message.recorded_ts
    };
    #data_messages.append(data_message)

    logger.debug('data_message: %s'%repr(data_message))
    data = urllib.parse.urlencode(data_message,).encode('utf-8')
    logger.debug('Data stream: %s'%data);

    service_request = urllib.request.Request(service_url)
    #service_request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
    try:
        response_stream = urllib.request.urlopen(service_request, data, timeout=30)
    except HTTPError as err:
        logger.error('Error connecting to server: %s - %s'%(err.code, err.reason))
        logger.debug('Moving message back into front of buffer');
        buffer.prepend(message)
        update_last_send_time(error_send_interval)
    except URLError as err:
        logger.error('Error connecting to server: %s'%(err.reason))
        logger.debug('Moving message back into front of buffer');
        buffer.prepend(message)
        update_last_send_time(error_send_interval)
    except:
        logger.error('Some other error occurred')
        buffer.prepend(message)
        update_last_send_time(error_send_interval)


def send_messages(messages, node_id):
    if len(messages) > 0:
        logger.info('Sending %d messages to server'%len(messages))

        # TODO: Get this working sending results in bulk
        data_messages = []


        for message in messages:
            data_message = {
                'device_id': message.device_id,
                'node_id': node_id,
                'message': message.data,
                'recorded_ts': message.recorded_ts
            };
            data_messages.append(data_message)

        logger.debug('data_messages: %s'%repr(data_messages))

        data_messages_json = json.dumps(data_messages)
        logger.debug('data_messages_json: %s'%data_messages_json)

        data=urllib.parse.urlencode({"messages": data_messages_json}).encode('utf-8')
        logger.debug('Data stream: %s'%data)

        logger.debug('Connecting to service url: %s'%service_url)
        service_request = urllib.request.Request(
            service_url,
        )
        try:
            #service_request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
            response_stream = urllib.request.urlopen(service_request, data, timeout=30)
        except HTTPError as err:
            logger.error('Error connecting to server: %s - %s'%(err.code, err.reason))
            logger.debug('Moving messages back to front buffer')
            buffer.prepend_messages(messages)
            update_last_send_time(error_send_interval)
        except URLError as err:
            logger.error('Error connecting to server: %s'%(err.reason))
            logger.debug('Moving messages back to front buffer')
            buffer.prepend_messages(messages)
            update_last_send_time(error_send_interval)
        except:
            logger.error('Some other error occurred');
            buffer.prepend_messages(messages)
            update_last_send_time(error_send_interval)

def update_last_send_time(interval):
    global next_send_time
    current_time = time.time();
    next_send_time = current_time + interval
    logger.debug('Updated next_send_time to: %d + %d = %d'%(current_time, interval, next_send_time))