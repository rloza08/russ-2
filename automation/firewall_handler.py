#!/usr/bin/env python3
import api.firewall as firewall
import utils.auto_logger as l
import utils.auto_json as json
import api.devices as devices
import automation.vlan_handler as vlan_handler
import config.load  as config
from copy import deepcopy
import api.network as network
import utils.auto_utils as utils
"""
Inputs: firewall_template, vlan_funnel_table
        output_file from config (default firewall_converted)
"""
class firewallHandler(object):
	def __init__(self, storeNumber):
		self.vlanFunnelTable = vlan_handler.createVlanTable(storeNumber)
		self.firewallOutputFile = config.firewallConverted
		fname = "firewall_template"
		self.fwRules = json.reader(fname, "templates")
		if self.fwRules  is None:
			l.logger.error("unable to load rules from firewall_template")
		self.storeNumber = storeNumber

    # TODO NEEDS TO BE REFACTORED
	def vlansToSubnet(self, ref):
		# DOCUMENT MORE
		vlans = ref.split(",")
		subnets = []
		for vlan in vlans:
			if vlan.find("VLAN") < 0:
				subnet = vlan
			else:
				vlan = vlan.replace("(", ",")
				vlan = vlan.replace(")", ",")
				vlanList = vlan.split(",")
				if len(vlanList) < 2:
					l.logger.error(vlanList)
					assert (0)
				vnumber = vlanList[1]
				offset = vlanList[2]
				offset = offset.replace(".", "")

				lookup = self.vlanFunnelTable.get(vnumber)

				if lookup is None:
					l.logger.error("vlan:{} not found in table".format(vnumber))
					return None

				if offset == "*":
					subnet = lookup
				else :
					_subnet = lookup.split(".")
					offset=int(offset)
					aux = int(_subnet[3].split("/")[0])
					fullOffset = offset+aux
					if (fullOffset>255):
						assert(fullOffset<=255)
					subnet = "{}.{}.{}.{}/32".format(_subnet[0],_subnet[1],_subnet[2],fullOffset)
			subnets.append(subnet)
		ref = ",".join(subnets)
		return ref

	def transformRulesFromVlanToSubnet(self):
		# Using deep copy to avoid future stepping into fw references.
		self.fwNewRules = deepcopy(self.fwRules)
		for rule in self.fwNewRules:
			rule["destCidr"] = self.vlansToSubnet(rule["destCidr"])
			rule["srcCidr"] = self.vlansToSubnet(rule["srcCidr"])
			rule["syslogEnabled"] = False

		rules=[]
		for rule in self.fwNewRules:
			if rule["comment"] == "Default rule":
				continue
			rules.append(rule)
		json.writer(self.firewallOutputFile, rules)
		self.fwRules=deepcopy(rules)
		l.logger.debug("created {}".format(self.firewallOutputFile))

def removeSerials():
	print ("DONE")
	exit(0)
	# Convert meraki template firewall to subnet firewall
	fname = "firewall_serials"
	data = json.convert(fname)
	json.writer(fname, data[0])
	for item in range(len(data)):
		netid = data[item]["id"]
		serial1 = data[item]["serial1"]
		serial2 = data[item]["serial2"]
		# print (netid, serial1, serial2)
		devices.removedevice(netid, serial1)
		devices.removedevice(netid, serial2)
	# Does physical VLAN creation on meraki device
	l.logger.info("success")

def convert(storeNumber):
	obj = firewallHandler(storeNumber)

	# "Source": "VLAN(19).21" to "Source": "167.146.66.21"
	# obj.convertFwRulesToJson(fw_input)
	# Actual Conversion of firewall rules based on VlanTable
	obj.transformRulesFromVlanToSubnet()

def deploy(netid, storeNumber):
	# Convert meraki template firewall to subnet firewall
	convert(storeNumber)
	# Does physical VLAN creation on meraki device
	firewall.set(netid)
	l.logger.info("success")

if __name__ == '__main__':
	storeName = "SHAWS_9845"
	storeNumber, netid =utils.getStoreNumber(storeName)
	convert(storeNumber)
	deploy(netid, storeNumber)
	#removeSerials()
