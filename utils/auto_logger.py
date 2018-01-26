# Add environment variables driven customizatio
import logging
import os

USEPATCH=os.environ.get("MKLOG_PATCH","USE")
LOGSCREEN=os.environ.get("MKLOG_SCREEN","SCREEN")
LOGFILE=os.environ.get("MKLOG_FILE","/tmp/meraki_auto.log")
LOGLEVEL=os.environ.get("MKLOG_LEVEL","DEBUG")

logger = logging.getLogger('auto-meraki')
formatter = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s')

if LOGFILE:
	fileHandler = logging.FileHandler("{}".format(LOGFILE))
	fileHandler.setFormatter(formatter)
	logger.addHandler(fileHandler)

if LOGSCREEN:
	consoleHandler = logging.StreamHandler()
	consoleHandler.setFormatter(formatter)
	logger.addHandler(consoleHandler)

if LOGLEVEL == "ERROR":
	logger.setLevel(logging.ERROR)
elif LOGLEVEL == "WARNING":
	logger.setLevel(logging.WARNING)
elif LOGLEVEL == "INFO":
	logger.setLevel(logging.INFO)
elif LOGLEVEL == "DEBUG":
	logger.setLevel(logging.DEBUG)
