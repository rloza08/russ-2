# https://raw.githubusercontent.com/meraki/dashboard-api-python/master/meraki.py

import api.meraki as meraki
import json
import utils.auto_logger as l

def __returnhandler_custom(statuscode, returntext, objtype, suppressprint):
	"""

	Args:
		statuscode: HTTP Status Code
		returntext: JSON String
		objtype: Type of object that operation was performed on (i.e. SSID, Network, Org, etc)
		suppressprint: Suppress any print output when function is called

	Returns:
		errmsg: If returntext JSON contains {'errors'} element
		returntext: If no error element, returns returntext

	"""

	validreturn = meraki.__isjson(returntext)
	noerr = False
	errmesg = ''


	if validreturn:
		returntext = json.loads(returntext)

		try:
			errmesg = returntext['errors']
		except KeyError:
			noerr = True
		except TypeError:
			noerr = True

	if str(statuscode) == '200' and validreturn:
		l.logger.debug('{0} Operation Successful - See returned data for results\n'.format(str(objtype)))
		return (True, returntext)
	elif str(statuscode) == '200':
		_str='{0} Operation Successful\n'.format(str(objtype))
		l.logger.debug(_str)
		return (True, None)
	elif str(statuscode) == '201' and validreturn:
		_str='{0} Added Successfully - See returned data for results\n'.format(str(objtype))
		l.logger.debug(_str)
		return (True, returntext)
	elif str(statuscode) == '201':
		_str='{0} Added Successfully\n'.format(str(objtype))
		l.logger.debug(_str)
		return (True, returntext)
	elif str(statuscode) == '204' and validreturn:
		_str='{0} Deleted Successfully - See returned data for results\n'.format(str(objtype))
		l.logger.debug(_str)
		return (True, returntext)
	elif str(statuscode) == '204':
		_str = '{0} Deleted Successfully\n'.format(str(objtype))
		l.logger.debug(_str)
		return (True, None)
	elif str(statuscode) == '400' and validreturn and noerr is False:
		l.logger.error('Bad Request - See returned data for error details\n')
		return (False, returntext)
	elif str(statuscode) == '400' and validreturn and noerr:
		l.logger.error('Bad Request - See returned data for details\n')
		l.logger.error(returntext)
		return (False, returntext)
	elif str(statuscode) == '400':
		l.logger.error('Bad Request - No additional error data available\n')
	elif str(statuscode) == '401' and validreturn and noerr is False:
		l.logger.error('Unauthorized Access - See returned data for error details\n')
		return (False, returntext)
	elif str(statuscode) == '401' and validreturn:
		l.logger.error('Unauthorized Access')
		return (False, returntext)
	elif str(statuscode) == '404' and validreturn and noerr is False:
		l.logger.error('Resource Not Found - See returned data for error details\n')
		return (False, errmesg)
	elif str(statuscode) == '404' and validreturn:
		l.logger.error('Resource Not Found')
		return (False, returntext)
	elif str(statuscode) == '500':
		l.logger.error('HTTP 500 - Server Error')
		return (False, returntext)
	elif validreturn and noerr is False:
		l.logger.error('HTTP Status Code: {0} - See returned data for error details\n'.format(str(statuscode)))
		return False, errmesg
	else:
		l.logger.error('HTTP Status Code: {0} - No returned data\n'.format(str(statuscode)))
		return (False, returntext)

def set():
	if l.USEPATCH:
		meraki.__returnhandler = __returnhandler_custom


set()
