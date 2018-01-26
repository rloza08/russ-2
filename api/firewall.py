#!/usr/bin/env python3
import config.load as config
import utils.auto_json as json
import utils.auto_logger as l
from api.meraki_patch import meraki
import traceback

class firewall(object):
	"""
	This allows to test each rule , good for finding bugs in the rules
	"""
	def setEach(self, netid):
		success=False
		str=None
		try:
			fname = config.firewallConverted
			fwrules = json.reader(fname)
			singleRule = []
			for rule in fwrules:
				singleRule.append(rule)
				success, str = meraki.updatemxl3fwrules(config.apikey, netid, singleRule)
				l.logger.debug(rule["comment"])
			if not success:
				l.logger.error("failed rule comment:{} {}".format(rule["comment"], str))
		except Exception as err:
			l.logger.error("exception failure netid:{}".format(netid))
			traceback.print_tb(err.__traceback__)
		return success, str

	def set(self, netid):
		success=False
		str=None
		try:
			fname = config.firewallConverted
			fwrules = json.reader(fname)
			success, str = meraki.updatemxl3fwrules(config.apikey, netid, fwrules)
			if not success:
				l.logger.error("failed netid:{} {}".format(netid, str))
		except Exception as err:
			l.logger.error("exception failure netid:{}".format(netid))
			traceback.print_tb(err.__traceback__)
		return success, str

	def get(self, netid):
		self.firewalls = None
		try:
			success, self.firewalls = meraki.getmxl3fwrules(config.apikey, netid)
			if not success:
				l.logger.error("failed netid:{} {}".format(netid, self.firewalls))
			fname = "firewall_{}".format(netid)
			json.writer(fname, self.firewalls)
		except Exception as err:
			l.logger.error("exception failure netid:{}".format(netid))
			traceback.print_tb(err.__traceback__)

def get(netid):
	"""Gets firewall rules for a given netid into a json file"""
	obj = firewall()
	obj.get(netid)

def set(netid):
	"""Sets the firewall from a json file"""
	obj = firewall()
	obj.set(netid)

def setEach(netid):
	"""Sets the firewall from a json file"""
	obj = firewall()
	obj.setEach(netid)

if __name__ == '__main__':
	obj=firewall()
	networkid = "L_686798943174001160"

	#obj.get(networkid)
	success, str= obj.set(networkid)
