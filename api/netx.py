#!/usr/bin/env python3
import sys
import os
import socket, struct
import utils.auto_logger as l

# TODO Turn upper and lower into 'u' and 'l' to ensure consistency

# custom modules ?????
sys.path.append('/appl/nms/pyLib')

class NetX(object):
	#
	# Modules for custom NetX routines for retail address space.
	# Includes supporting IPv4 Modules
	#

	def __init__(self):
		offset=0x100
		self.netXOffset={}
		self.netXOffset['a'] = 0x000
		self.netXOffset['b'] = self.netXOffset['a']+offset
		self.netXOffset['c'] = self.netXOffset['b']+offset
		self.netXOffset['d'] = self.netXOffset['c']+offset
		self.netXOffset['e'] = 0x000
		self.netXOffset['f'] = self.netXOffset['e']+offset
		self.netXOffset['g'] = self.netXOffset['f']+offset
		self.netXOffset['h'] = self.netXOffset['g']+offset
		#self.validSubNetList = ['a','b','c','d','e','f','g','h','x']
		self.validSubNetList = ['a','b','c','d','e','f','g','h']

	def getAddr(self, host):
		return socket.gethostbyname(host)

	def getName(self, addr):
		l.logger.debug(addr)
		return socket.gethostbyaddr(addr)[0]

	def dottedQuadToNum(self, ip):
		"convert decimal dotted quad string to long integer"
		return struct.unpack('!L',socket.inet_aton(ip))[0]

	def numToDottedQuad(self, n):
		"convert long int to dotted quad string"
		return socket.inet_ntoa(struct.pack('!L',n))

	def makeMask(self, n):
		"return a mask of n bits as a long integer"
		n = 32 - n
		return (2<<n-1)-1

	def ipToNetAndHost(self, ip, maskbits):
		"returns tuple (network, host) dotted-quad addresses given IP and mask size"
		# (by Greg Jorgensen)
		n = self.dottedQuadToNum(ip)
		m = self.makeMask(maskbits)
		host = n & m
		net = n - host
		return self.numToDottedQuad(net)

	def getThreeOctets(self, slot):
		if slot in ['a','b','c','d']:
			aux = self.netX['upper']
		else:
			aux = self.netX['lower']

		str = self.numToDottedQuad(self.dottedQuadToNum(aux) +  self.netXOffset[slot])
		octets = str.split(".")
		str = "{}.{}.{}".format(octets[0], octets[1], octets[2])
		return str

	def makeNetX(self, ip):
		"returns tuple(Upper,Lower,NetA,NetB,..NetH) for ip in 10.128.0.0/9"
		self.netX = {}

		# test if address in upper or lower block
		base = self.ipToNetAndHost(ip,10)

		if str(base) < '10.192' :
			ipVal = self.dottedQuadToNum(ip)
			ipVal += 0x400000
			ipNew = self.numToDottedQuad(ipVal)
			ip = ipNew

		base = self.ipToNetAndHost(ip,22)

		self.netX={}
		self.netX['upper'] = base
		self.netX['lower'] = self.numToDottedQuad(self.dottedQuadToNum(self.netX['upper']) - 0x400000)

		for slot in self.validSubNetList:
			# if slot == 'x':
			# 	octets = self.netX['upper'].split(".")
			# 	l.logger.debug("validate logic with Michael")
			# 	self.netX['x'] = "{}.{}".format(octets[0], octets[1])
			# else:
			self.netX[slot] = self.getThreeOctets(slot)

		return self.netX

	def getAll(self, _netx=None, _name=None, _addr=None):
		if (_name is None and _addr is None):
			l.logger.error("name and addr are empty")
			return False
		if _name:
			addr = self.getAddr(_name)
			name = _name
		else:
			addr = _addr
			name = None   #FIXME self.getName(addr)
		l.logger.debug(name)
		l.logger.debug(addr)

		# Now build the ranges/etc
		netX = self.makeNetX(addr)

		pickNet = None
		if _netx :
			str = "CC = %s.5" % netX[_netx]
			l.logger.debug(str)
			pickNet = "CC = %s.5" % netX[_netx]

		l.logger.debug("netX created.")
		return netX, pickNet

def _get(netx=None, name=None, addr=None):
	obj = NetX()
	obj.getAll(_netx, name, addr)

def get(name):
	obj = NetX()
	netx, picknet = obj.getAll(None, name, None)
	return netx, picknet

import utils.auto_json as mkjson
import utils.auto_logger as l

if __name__ == '__main__':
	cwd = os.getcwd()
	_netx = None
	_name = None
	_addr = None
	netx, picknet = get("mx9845a")
	str = mkjson.make_pretty((netx))
	l.logger.debug(str)
	#netXPicks = _get(netx=None, name=None, addr="151.101.193.67")
