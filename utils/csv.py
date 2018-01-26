#!/usr/bin/env python3
import json
import utils.auto_logger as l

import csv
import os
import traceback

class writer(object):
	def __init__(self, fname, data):
		# Set the CSV output file and write the header row
		cwd = os.getcwd()
		fName = "{}/../data/{}.csv".format(cwd, fname)
		self.output_file = open(fName, mode='w')
		self.csv_writer = csv.writer(self.output_file, quoting=csv.QUOTE_ALL)
		header = data[0].keys()
		# Header
		print (header)
		self.csv_writer.writerow(header)
		for row in data:
			print (row)
			line=""
			first=True
			for key in row:
				line+=","
				line+=row[key]
			print (line)
		# for row in data:
		 #    print (row)
		# 	self.csv_writer.writerow(csv_row)

	def __del__(self):
		self.output_file.close()


if __name__ == '__main__':
	csvfile = 'firewall-rules.csv'
	fname = "json-csv-conversion"
	convert(fname )

