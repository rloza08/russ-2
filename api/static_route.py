#!/usr/bin/env python3
import config.load as config
import utils.auto_logger as l
import api.meraki as meraki
import traceback
import api.network as networks

class staticRoute(object):
	def add(self, netid, name, subnet, ip):
		# PROTECTING PRODUCTION using only test store
		# assert(netid=="L_686798943174001160")
		# ONLY run using the api testing org id
		success=False
		str=None
		try:
			success, str = meraki.addstaticroute(config.apikey, netid , name, subnet, ip)
			if not success:
				l.logger.error("{}".format(str))
		except Exception as err:
			l.logger.error("exception failure netid:{}".format(netid))
			traceback.print_tb(err.__traceback__)
		return success, str

def addStaticRoute(netid, name, subnet, ip):
	obj = staticRoute()
	obj.add(netid, name, subnet, ip)

if __name__ == '__main__':
	store="mx1234a"
	networkname= "Test_Store_1234"
	ip = "10.235.91.1"

	# subnet= "10.171.88.0/22"   # lower
	# name="static route lower summary"
	# addStaticRoute(networkname, name, subnet, ip)
	#
	# subnet= "10.235.88.0/22"   # upper
	# name="static route upper summary"
	# addStaticRoute(networkname, name, subnet, ip)

