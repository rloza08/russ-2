#!/usr/bin/env python3
import utils.auto_json as json
import utils.auto_logger as l
import config.load as config
import api.static_route as static_route
import automation.vlan_handler as vlan_handler
import api.network  as network

def add(netid, storeNumber):
	networkName= "Store_{}".format(storeNumber)
	fname, lower, upper = vlan_handler.createVlanFiles(netid, storeNumber)
	l.logger.debug(fname)

	# Get the ip from the vlan_generated file
	vlans = json.reader(fname.split(".")[0])
	for vlan in vlans:
		ip=None
		if vlan['id'] == int(config.staticRouteNextHop):
			ip = vlan["applianceIp"]
			break

	subnet= "{}/22".format(lower)   # lower
	name="lower summary subnet"
	static_route.addStaticRoute(netid, name, subnet, ip)

	subnet= "{}/22".format(upper)   # lower
	name="upper summary subnet"
	static_route.addStaticRoute(netid, name, subnet, ip)

if __name__ == "__main__":
	storeName = "SHAWS_9845"
	netid = network.getNetIdForStore(storeName)
	storeNumber=network.getStoreNumber(storeName)

	add(netid, storeNumber)
