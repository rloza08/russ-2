#!/usr/bin/env python3
import automation.vlan_handler as vlan_handler
import automation.firewall_handler as firewall_handler
import utils.auto_logger as l
import automation.vpn_handler as vpn_handler
import automation.static_route_handler as static_route_handler
import utils.auto_utils as utils

def deploy(storeName):
	netid, storeNumber=utils.getStoreNumber(storeName)

	vlan_handler.deploy(netid, storeNumber)

	static_route_handler.add(netid, storeNumber)

	firewall_handler.deploy(netid, storeNumber)

	vpn_handler.setupSiteToSiteVpn(netid, storeNumber)

	l.logger.info("success")

if __name__ == '__main__':
	storeName = "SHAWS_9611"
	deploy(storeName)


