#!/usr/bin/env python3
import re
import api.network as network
import os

def getStoreNumber(storeName):
	storeNumber = int(re.sub("[^0-9]", "", storeName))
	netid = network.getNetIdForStore(storeName)
	return netid, storeNumber

if __name__ == '__main__':
	storeName = "SHAWS_9845"
	getStoreNumber(storeName)

