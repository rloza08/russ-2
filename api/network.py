#!/usr/bin/env python3
import config.load as config
import utils.auto_json as json
import utils.auto_logger as l
from api.meraki_patch import meraki
import traceback

class networks(object):
	def getNetIdForStore(self, storeName):
		success, stores = self.list(config.orgid)
		if not success:
			l.logger.error("failed. orgid:{} storeName:{}".format(config.orgid, storeName))
			return None
		netid=None
		for store in stores:
			if store["name"] == storeName:
				netid=store["id"]
				break
		l.logger.info(netid)
		return netid

	def list(self, orgid):
		success = False
		self.networks=None
		try:
			success, self.networks = meraki.getnetworklist(config.apikey, orgid)
			if success:
				l.logger.debug("success")
				l.logger.debug(json.make_pretty(self.networks))
			else:
				l.logger.error("failed.")
				l.logger.error("vlan: {}".format(vl))
		except Exception as err:
			l.logger.error("orgid: {}".format(orgid))
			traceback.print_tb(err.__traceback__)
		return success, self.networks

	def getdetail(self, networkid):
		success = False
		self.network=None
		try:
			success, self.network= meraki.getnetworkdetail(key.apikey, networkid)
			l.logger.debug(json.make_pretty(self.network))
		except Exception as err:
			l.logger.error("orgid: {}".format(networkid))
			traceback.print_tb(err.__traceback__)
		return success, self.network

	def update(self, networkid, name):
		success = False
		self.network=None
		try:
			success, self.network = meraki.updatenetwork(config.apikey, networkid, name, tz="US/Pacific", tags=None)
			l.logger.debug(json.make_pretty(self.network))
		except Exception as err:
			l.logger.error("orgid: {}".format(networkid))
			traceback.print_tb(err.__traceback__)
		return success, self.network

	def add(self, orgid, name, nettype):
		# nettype : wireless, Switch, "Security appliance"
		success = False
		self.network = None
		try:
			success, self.network = meraki.addnetwork(config.apikey, orgid, name, nettype, tags=None, tz="US/Pacific")
			json.writer("network_{}".format(name), self.network)
			if not success:
				l.logger.warning("failed, {} {}: {}".format(name, nettype, self.network))

		except  Exception as err:
			l.logger.error("orgid:{} name:{} nettype:{}".format(orgid, name, nettype))
			traceback.print_tb(err.__traceback__)
		return success, self.network

	def deln(self, networkid):
		success = False
		str=None
		try:
			success, str = meraki.delnetwork(config.apikey, networkid)
			l.logger.debug("success {}".format(networkid))
		except Exception as err:
			l.logger.error("networid:{} {}".format(networkid, str))
			traceback.print_tb(err.__traceback__)
		return success, str

def getCreatedNetworkId(networkName):
	fname = "network_{}".format(networkName)
	network = json.reader(fname)
	if network is None:
		l.logger.error("unable to load rules from firewall_template")
	return network["id"]

def create(storeNumber):
	"""Creates a networks and returns a network id"""
	#store="mx{}a".format(storeNumber)
	networkName= "Store_{}".format(storeNumber)

	obj=networks()
	success, netid = obj.add(config.orgid, networkName, nettype="appliance")
	return success, netid

def list(orgid):
	"""List all networks"""
	obj=networks()
	obj.list(orgid)

def getNetIdForStore(storeName):
	obj=networks()
	netid = obj.getNetIdForStore(storeName)
	return netid

if __name__ == '__main__':
	#create("test_reno116_ubuntu", "appliance")
	#list(config.orgid)
	getNetIdForStore("SHAWS_9845")
