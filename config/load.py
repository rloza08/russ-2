#!/usr/bin/env python3
import utils.auto_json as json
import os
def proxysettings(proxyUser, proxyPassword):
	url = "http://{}:{}@phxproxyvip.safeway.com:8080".format(proxyUser, proxyPassword)
	os.environ['HTTPS_PROXY'] = url

def getOrgId():
	orgName = config[0]["org-name"]
	orgid=None
	for org in orgs:
		if org["name"] == orgName:
			orgid=org["id"]
			break
	return orgid

config = json.reader("safeway-config", "config")
personal = json.reader("../../safeway-personal")
orgs = json.reader("../config/safeway-orgs")

apikey=personal[0]["apikey"]


firewall=config[0]["firewall"]
staticRouteNextHop=firewall['staticRouteNextHop']
firewallConverted=firewall["output_file"]

orgid = getOrgId()

useProxy=personal[0]["useProxy"]
if useProxy:
 	proxyUser = personal[0]['proxy_user']
 	proxyPassword = personal[0]['proxy_password']
 	proxysettings(proxyUser, proxyPassword)

vlan=config[0]["vlan"]
vlanFunnelFile=vlan["funnel_file"]
vlanUpdateOnly=vlan["update_only"]
netxFile=vlan['netx_file']
devicePrefix = vlan["device_prefix"]
devicePostfix = vlan["device_postfix"]

vpn = config[0]["vpn"]
hubnetworks=vpn["hubnetworks"]
defaultroute=vpn["defaultroute"]
