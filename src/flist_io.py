import logging
import flist_api as api

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("flist")

def logException(logger: logging.Logger, ex: Exception, msg: str =None):
    logger.error(((msg + " :") if msg is not None else "") + str(ex))

def logFlistException(logger: logging.Logger, ex: Exception, msg: str =None):
    stepname = api.implicitly_or("state.currentStep", "<no current flist step>")
    msg = ((msg + " :") if msg is not None else "")
    exmsg = str(ex)
    logger.error(f"Error in step {stepname}: {msg}{exmsg}")

def msg(msg: str):
    implicitLogger = api.implicitly_or("prog.logger", logging.getLogger("default"))
    logger = implicitLogger or logger
    logger.info(msg)

class FlistException(Exception):
    pass
