import logging

__author__ = 'nick'

logger = logging.getLogger(__name__);

# TODO: Store the following on disk
buffer = []
important_buffer = []

def append(message):
    """Adds message to the buffer"""
    buffer.append(message)
    logger.debug('Added message to buffer: %s'%vars(message))
    logger.info('Current buffer count: %d'%count())

def get_all():
    """Returns array of all buffered messages and clears buffer"""
    global buffer
    messages = buffer
    buffer = []
    logger.info('Returning contents and cleared buffer, current count: %d'%count())
    return messages

def get():
    message = buffer.pop()
    logger.info('Popped one message out of buffer, current count: %d'%count())
    return message

def count():
    return len(buffer)



def important_append(message):
    """Adds message to the important buffer

    These are messages that are to be sent out immediately
    """
    important_buffer.append(message)
    logger.debug('Added message to important buffer: %s'%vars(message))
    logger.info('Current import buffer count: %d'%important_buffer())

def important_get_all():
    """Return arra of all buffered important messages and clears it"""
    global important_buffer
    messages = important_buffer
    important_buffer = []
    logger.info('Return contents and cleared important buffer, current count: %d'%important_count())
    return messages

def important_get():
    message = important_buffer.pop()
    logger.info('Popped one message out of important buffer, current count: %d'%important_count())
    return message

def important_count():
    return len(important_buffer)
