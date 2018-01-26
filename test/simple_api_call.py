from meraki import meraki
import os

os.environ['HTTPS_PROXY']="http://culproxyvip.safeway.com:8080";

print(meraki.myorgaccess('d10aa87866385c57d835bc7e982a022c610c2755'))