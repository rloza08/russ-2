#!/usr/bin/env python3
import api.vpn as vpn
import utils.auto_json as json
import config.load as config
import automation.vlan_handler as vlan_handler

def setupSiteToSiteVpn(netid, storeNumber):
	# Load vlan table
	store="mx{}a".format(storeNumber)
	networkName= "Store_{}".format(storeNumber)

	vlan_handler.createVlanFiles(netid, storeNumber)
	netx = json.reader(config.netxFile)

	# Generate vpn hubnetworks and vpn-subnets
	hubnetworks = config.hubnetworks
	defaultroute = config.defaultroute

	upper = "{}/22".format(netx['upper'])
	lower = "{}/22".format(netx['lower'])
	subnets = []
	usevpn = []
	subnets.append(lower)
	usevpn.append(True)     # enable the subnet above
	subnets.append(upper)
	usevpn.append(True)     # enable the subnet above

	# Upload to meraki
	vpn.updatevpnsettings(netid, hubnetworks, defaultroute, subnets, usevpn)

if __name__ == '__main__':
	storeNumber="9611"
	setupSiteToSiteVpn(storeNumber)

