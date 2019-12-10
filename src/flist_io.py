import logging
import flist_api as api

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("flist")

def logException(logger: logging.Logger, ex: Exception, msg: str =None):
    logger.error(((msg + " :") if msg is not None else "") + str(ex))


def msg(msg: str):
    implicitLogger = api.implicitly("prog.logger")
    logger = implicitLogger or logger
    logger.info(msg)

class FlistException(Exception):
    pass
