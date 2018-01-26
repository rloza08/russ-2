#!/usr/bin/env python3
import json
import utils.auto_logger as l

import csv
import os
import traceback

class Json:
	def make_pretty(self, my_json):
		return (json.dumps(my_json, indent=4, sort_keys=True))

	def convertCsvToJson(self, fname):
		self.item = {}
		cwd = os.getcwd()
		csvfile = "{}/../data/{}.csv".format(cwd, fname)
		jsonfile = "{}/../data/{}.json".format(cwd, fname)

		entries = []
		with open(csvfile, newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for entry in reader:
				entries.append(entry)
		self.writerFullPath(jsonfile, entries)
		#l.logger.info("success")
		return entries

	def writerFullPath(self, fname, data):
		str = self.make_pretty(data)
		with open(fname, 'w') as f:
			json_data=f.write(str)

	def writer(self, fname, data):
		cwd = os.getcwd()
		file = "{}/../data/{}.json".format(cwd, fname)
		self.writerFullPath(file, data)

	def csvWriter(self, fname, data):
		cwd = os.getcwd()
		fname = "{}/../data/{}.csv".format(cwd, fname)
		with open(fname, 'wb') as f:
			w = csv.DictWriter(f, data.keys())
		w.writerow(data)
		f.close()

	def reader(self, fname, dataDir="data"):
		data = None
		try:
			cwd = os.getcwd()
			file = "{}/../{}/{}.json".format(cwd, dataDir, fname)

			json_data=open(file).read()
			data = json.loads(json_data)
			#l.logger.debug("data: {}".format(data))
		except Exception as err:
			l.logger.error("fname:{} {}".format(fname, file))
			traceback.print_tb(err.__traceback__)
		return data

def reader(fname, configDir="data"):
	"""Reads json file"""
	data = Json().reader(fname, configDir)
	return data

def writer(fname, data):
	Json().writer(fname, data)

def convert(fname):
	"""Converts a csvfile into json"""
	return Json().convertCsvToJson(fname )

def make_pretty(my_json):
	return Json().make_pretty(my_json)

if __name__ == '__main__':
	csvfile = 'firewall-rules.csv'
	fname = "json-csv-conversion"
	convert(fname )

