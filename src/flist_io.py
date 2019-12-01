import logging

class FlistException(Exception):
    pass

logging.basicConfig(level=logging.INFO)

def err(msg, *verbose):
    logging.error(msg)

def msg(msg, *verbose):
    logging.info(msg)

def verbose(msg, *verbose):
    logging.info(msg)
