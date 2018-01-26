#!/usr/bin/env python3
import config.load as config
import utils.auto_json as json
import utils.auto_logger as l
from api.meraki_patch import meraki
import traceback
import api.network as networks
import api.meraki as meraki

# success, str = meraki.getmxvpnfwrules(config.apikey, config.orgid)
# str = json.make_pretty(str)
# l.logger.info("{} {}".format(success, str))

# def updatemxvpnfwrules(apikey, orgid, vpnrules, syslogDefaultRule=False, suppressprint=False):

class vpn(object):
	def updateVpnSettings(self, networkid, hubnetworks, defaultroute, subnets, usevpn):
		success = False
		str = None
		try:
			mode = 'spoke'
			success, str = meraki.updatevpnsettings(config.apikey, networkid, mode,
			                                        subnets, usevpn, hubnetworks, defaultroute)
			if success:
				l.logger.debug("success")
				json.writer("vpn_updatevpnsettings_{}".format(networkid), str)
			else:
				l.logger.error("failed.")
				l.logger.error("{}".format(str))
		except  Exception as err:
			l.logger.error("networkid: {} str:{}".format(networkid, str))
			traceback.print_tb(err.__traceback__)
		return success, str



""""
	hubnetworks = 

"""
def updatevpnsettings(networkid, hubnetworks, defaultroute, subnets, usevpn):
	usevpn = [True, True]
	obj = vpn()
	obj.updateVpnSettings(networkid, hubnetworks, defaultroute, subnets, usevpn)

if __name__ == '__main__':
	hubnetworks = ["N_686798943174001360"]
	defaultroute = [True]
	subnets = ["10.235.88.0/22", "10.171.88.0/22"]
	usevpn = [True, True]
	updatevpnsettings("Test_Store_1234", hubnetworks, defaultroute, subnets, usevpn)

