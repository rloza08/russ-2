#!/usr/bin/env python3
import os
import utils.auto_json as json
import utils.auto_logger as l
from jinja2 import Environment, FileSystemLoader
import traceback


PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
	autoescape=False,
	loader=FileSystemLoader(os.path.join(PATH, '../templates')),
	trim_blocks=False)

class jinjaAuto(object):
	def render_template(self, template_filename, context):
		result=None
		try:
			result = TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)
		except Exception as err:
			l.logger.error("template_filename:{}".format(template_filename))
			traceback.print_tb(err.__traceback__)
		return result

	def createOutput(self, template, output, context):
		fname = "../data/{}".format(output)
		with open(fname, 'w') as f:
			output = self.render_template(template, context)
			if output is None:
				l.logger.error("failed")
				return
			f.write(output)
			l.logger.debug(output)

def createContext():
	context = {
		'networkid': "L_650207196201623673",
		'vlan' : {}
	}

	fname = "funnel_vlans_table"
	vlans = json.reader(fname)

	for key, value in vlans.items():
		vlanId = int(key)
		subnet=value
		octets=subnet.split(".")
		octets="{}.{}.{}".format(octets[0], octets[1], octets[2])
		context["vlan"][vlanId] = {}
		context["vlan"][vlanId]['octets'] = octets
		context["vlan"][vlanId]['subnet'] = subnet
	return context

def main():
	netid="1234"
	template="vlans_set_template.json"
	output="vlans_generated_{}.json".format(netid)
	context = createContext()
	l.logger.debug(context)
	obj = jinjaAuto()
	obj.createOutput(template, output, context)

if __name__ == "__main__":
	main()


"""	
ISSUES:
inja2.exceptions.UndefinedError: dict object has no element 18

added dummy entry to funnel_vlans_table.json

"""