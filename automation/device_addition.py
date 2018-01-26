#!/usr/bin/env python3
import automation.vlan_converter as fw_Convert
import api.firewall as firewall
import api.network as networks
import utils.auto_logger as l
import api.devices as devices

def deployByNetid(netid, serial):
	devices.claimadd(netid, serial)

def deploy(networkName, serial):
	netid = networks.getNetworkId(networkName)
	deployByNetid(netid, serial)

if __name__ == '__main__':
	serial="Q2PN-KRED-QSMA"
	networkName = "Test_Store_1234"
	deploy(networkName, serial)
