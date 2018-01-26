#!/usr/bin/env python3
import utils.auto_json as json
import utils.auto_logger as l
import utils.auto_jinja as auto_jinja
import api.vlans as vlans
import config.load as config
import api.network as network
import api.netx as netx
import utils.auto_utils as utils

class vlanTable(object):
	def __init__(self):
		self.funnelFile = config.vlanFunnelFile

	def create(self, store):
		# Get netX for the shop and saves it into the netxFile
		self.createVlanDefs(store)
		self.convertFunnelToJson()

		# Making men and mice format more consistent with netX format
		# Changes from 10.x.a.96/27 to a.96/27
		self.transformFunnelToNetx()

		# Turning funnel (men and mice) into actual shop-subnet info.
		# from g.0/25 to 167.146.68.19
		# generates funnel_vlans_subnet
		self.transformFunnelToSubnet()

		# creates  "95": "167.146.70"
		self.createFunnelVlanTable()
		return self.funnelVlanTable


	def createVlanDefs(self, storeNumber):
		self.NetX = netx.NetX()
		self.validSubnets = self.NetX.validSubNetList
		self.netxFile = config.netxFile
		storeDevice="{}{}{}".format(config.devicePrefix, storeNumber, config.devicePostfix)
		self.netx, picknet = self.NetX.getAll(None, storeDevice, None)
		json.writer(self.netxFile, self.netx)
		l.logger.debug("created {}".format(self.netxFile))

	def convertFunnelToJson(self):
		self.funnel = json.convert(self.funnelFile)
		self.funnelNetxFile = "{}_netx".format(self.funnelFile)
		self.funnelSubnetFile = "{}_subnet".format(self.funnelFile)
		self.funnelVlanFile = "{}_table".format(self.funnelFile)
		return self.funnel

	# Changes from 10.x.a.96/27 to a.96/27
	def transformFunnelToNetx(self):
		for entry in self.funnel:
			subnet = entry["Subnet"].split(".")
			# if there is an x than we need to replace otherwise skip
			if subnet[1]=='x':
				if (subnet[2]>='a' and subnet[2]<='h'):
					entry["Subnet"]=subnet[2]+"."+subnet[3]
		json.writer(self.funnelNetxFile, self.funnel)
		l.logger.debug("created {}".format(self.funnelNetxFile))

	# from g.0/25 to 167.146.68.19
	def transformFunnelToSubnet(self):
		for entry in self.funnel:
			subnet = entry["Subnet"].split(".")
			netxIndex = subnet[0]
			if netxIndex in self.validSubnets:
				subnet[0] = self.netx[netxIndex]
				elem=entry["Subnet"].split(".")
				entry["Subnet"] = "{}.{}".format(subnet[0],elem[1])
				json.writer(self.funnelSubnetFile, self.funnel)
		l.logger.debug("created {}".format(self.funnelSubnetFile))

    # Table of Vlan to convert
	def createFunnelVlanTable(self):
		self.funnelVlanTable={}
		for entry in self.funnel:
			vlan = entry["Vlan"]
			self.funnelVlanTable[vlan]=entry["Subnet"]

		# # Adding fixed in the VlanTable	 (Guest WIFI, Cache VPN Cache Internet)
		self.funnelVlanTable["995"] = "192.168.1.0/24"
		self.funnelVlanTable["996"] = "192.168.100.0/24"
		self.funnelVlanTable["997"] = "192.168.101.0/24"

		json.writer(self.funnelVlanFile, self.funnelVlanTable)
		l.logger.debug("created {}".format(self.funnelVlanFile))

class vlanHandler(object):
	def __init__(self, template, output, netid):
		self.template = template
		self.output = output
		self.netid = netid

	def __init__(self):
		self.template = None
		self.output = None

	def createContext(self):
		self.context = {
			'networkid': None,
			'vlan' : {}
		}

		self.context['networkid']=self.netid
		fname = "{}_table".format(config.vlanFunnelFile)
		vlans = json.reader(fname)

		for key, value in vlans.items():
			vlanId = int(key)
			subnet=value
			octets=subnet.split(".")
			octets="{}.{}.{}".format(octets[0], octets[1], octets[2])
			self.context["vlan"][vlanId] = {}
			self.context["vlan"][vlanId]['octets'] = octets
			self.context["vlan"][vlanId]['subnet'] = subnet
		l.logger.debug(self.context)


	def createVlanGenerated(self):
		obj = auto_jinja.jinjaAuto()
		obj.createOutput(self.template, self.output, self.context)


	def createVlanTable(self, storeNumber):
		self.vlanTable=vlanTable()
		ref=self.vlanTable.create(storeNumber)
		return ref

	def createVlanFiles(self, netid, storeNumber):
		self.createVlanTable(storeNumber)
		# Create/Update for all VLANs
		self.netid = netid
		self.template="vlans_set_template.json"
		self.output="vlans_generated_{}.json".format(netid)
		self.createContext()
		self.createVlanGenerated()
		return self.output


def createVlanTable(storeNumber):
	obj = vlanHandler()
	ref = obj.createVlanTable(storeNumber)
	return ref

def createVlanFiles(netid, storeNumber):
	obj = vlanHandler()
	ref = obj.createVlanFiles(netid, storeNumber)
	lower = obj.vlanTable.netx["lower"]
	upper = obj.vlanTable.netx["upper"]
	return ref, lower, upper

def deploy(netid, storeNumber):
	obj = vlanHandler()
	obj.createVlanFiles(netid, storeNumber)
	# Does physical VLAN creation on meraki device
	vlans.createUpdateVlanList(netid)

if __name__ == "__main__":
	storeName = "SHAWS_9845"
	netid = network.getNetIdForStore(storeName)
	storeNumber=utils.getStoreNumber(storeName)

	#deploy(netid, storeNumber)
	createVlanTable(storeNumber)