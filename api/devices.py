#!/usr/bin/env python3
import config.load as config
import utils.auto_json as json
import utils.auto_logger as l
from api.meraki_patch import meraki
import traceback

class devices(object):
	def addtonet(self, networkid, serial):
		success = False
		str = None
		try:
			success, str = meraki.adddevtonet(config.apikey, networkid, serial)
			if success:
				l.logger.debug("success")
				json.writer("addtonet_{}".format(serial), str)
			else:
				l.logger.error("failed.")
				l.logger.error("{}".format(str))
		except  Exception as err:
			l.logger.error("networkid: {} serial:{}".format(networkid, serial))
			traceback.print_tb(err.__traceback__)
		return success, str

	def claim(self, serial, licensekey=None, licensemode=None, orderid=None):
		success = False
		str=None
		try:
			success, self.claim = meraki.claim(config.apikey, config.orgid,
							serial, licensekey,
							licensemode, orderid)
			if not success:
				l.logger.error("orgid: {} serial:{} claim:{}".format(orgid, serial, self.claim))
				json.writer("claim_{}".format(serial), self.claim)
			json.writer("claim_{}".format(serial), self.claim)
		except Exception as err:
			l.logger.error("serial:{}".format(serial))
			traceback.print_tb(err.__traceback__)

		return success, self.claim
"""
Not in Use
"""
def claimadd(networkid, serial):
	"""Creates a networks and returns a network id"""
	obj=devices()
	success, str = obj.claim(serial)
	if success:
		obj.addtonet(networkid, serial)

"""
Not in Use
"""
def removedevice(networkid, serial):
	meraki.removedevfromnet(config.apikey, networkid, serial)

if __name__ == '__main__':
	# serial="Q2PN-KRED-QSMA"
	# networkid = "N_686798943174003816"
	# claimadd(networkid, serial)
	pass