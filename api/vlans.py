#!/usr/bin/env python3
import config.load as config
import utils.auto_json as json
import utils.auto_logger as l
from api.meraki_patch import meraki
import traceback

class vlans(object):
	"""Reads vlans from file and sets them up on MERAKI Infra"""
	def list(self, fname):
		try:
			vlans = json.reader(fname)
			for vl in vlans:
				l.logger.info("vlan: {}".format(vl))
		except  Exception as err:
			l.logger.error("failed.")
			l.logger.error("fname: {}".format(fname))
			traceback.print_tb(err.__traceback__)


	def createUpdateVlanList(self, netid):
		fname = "vlans_generated_{}".format(netid)
		apikey = config.apikey
		vlans = json.reader(fname)
		for vl in vlans:
			try:
				networkid = vl['networkId']
				id = vl['id']
				name = vl['name']
				subnet = vl['subnet']
				applianceIp = vl['applianceIp']
				if id in config.vlanUpdateOnly:
					success = True
				else:
					success, _err = meraki.addvlan(apikey, networkid, id, name, subnet, applianceIp)

				if success :
					fixedipassignments = vl['fixedIpAssignments']
					reservedipranges = vl['reservedIpRanges']
					vpnnatsubnet = None
					dnsnameservers =  vl['dnsNameservers']
					success = True
					_err = ""
					if fixedipassignments or \
							reservedipranges or \
							vpnnatsubnet or \
							dnsnameservers:
						success, _err = meraki.updatevlan(apikey, networkid, id, name, subnet, applianceIp,
						                fixedipassignments,
						                reservedipranges,
						                vpnnatsubnet,
						                dnsnameservers)

				if success:
					l.logger.debug("success")
					l.logger.debug("vlan: {}".format(vl))
				else:
					l.logger.error("failed.")
					l.logger.error("vlan: {}".format(vl))
					return False
			except Exception as err:
				l.logger.error("exception")
				traceback.print_tb(err.__traceback__)
		return True

	def get(self, netid):
		self.vlans = None
		try:
			success, self.vlans = meraki.getvlans(config.apikey, netid)
			if not success:
				l.logger.error("failed netid:{} {}".format(netid, self.vlans))
			fname = "vlans_{}".format(netid)
			json.writer(fname, self.vlans)
			l.logger.info("netid:{} {}".format(netid, json.make_pretty(self.vlans)))
		except Exception as err:
			l.logger.error("exception failure netid:{}".format(netid))
			traceback.print_tb(err.__traceback__)

	def delete(self, netid, vlanid):
		self.vlans = None
		try:
			success, self.vlans = meraki.getvlans(config.apikey, netid)

			success, self.vlans = meraki.delvlan(config.apikey, netid, vlanid)
			if not success:
				l.logger.error("failed netid:{} vlanid:{}".format(netid, vlanid))
			l.logger.debug("netid:{} vlanid:{}".format(netid, vlanid))
		except Exception as err:
			l.logger.error("exception failure netid:{} vlanid:{}".format(netid, vlanid))
			traceback.print_tb(err.__traceback__)

def get(netid):
	"""Gets vlans for a given netid into a json file"""
	obj=vlans()
	obj.get(netid)

def createUpdateVlanList(netid):
	"""Sets vlans from a json file"""
	obj=vlans()
	obj.createUpdateVlanList(netid)

def delete(netid, vlanid):
	"""Sets vlans from a json file"""
	obj=vlans()
	obj.delete(netid, vlanid)

def list(fname):
	"""List all vlans in a json file"""
	obj=vlans()
	obj.list(fname)

if __name__ == '__main__':
	fname="set-vlans"
	networkid = "N_686798943174003679"
	networkid_get = "L_650207196201623673"
	networkid = "L_686798943174001160"

	#get(networkid_get)
	#create(networkid)
	delete(networkid, 1)