#!/usr/bin/env python3
import os
import auto_logger as l
import meraki
import meraki_patch
import auto_api_key as key

meraki_patch.set()


print ("MKLOG_SCREEN:",l.LOGSCREEN)
print ("MKLOG_FILE:",l.LOGFILE)
print ("MKLOG_LEVEL:", l.LOGLEVEL)


l.logger.debug("Showing DEBUG level")
l.logger.info("Showing INFO level")
l.logger.warning("Showing WARNING level")
l.logger.error("Showing ERROR level")

