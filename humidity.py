#!/usr/bin/python

import subprocess
import re
import sys
import time
import datetime
import httplib, urllib
#import gspread
#import getopt

# ===========================================================================
# ThingSpeak Details
# ===========================================================================

api_key = ''

#try:
#  opts, args = getopt.getopt(argv, "hk:", ["apikey="])
#except getopt.GetoptError:
#  print 'humidity.py -k <apikey>'
#  sys.exit(2)
#for opt, arg in opts:
#  if opt in ('-k', '--apikey'):
#    api_key= arg

api_key = sys.argv[1]
print 'api key is"', api_key

# ===========================================================================
# Functions 
# ===========================================================================

def submit(temperature, humidity):
  params = urllib.urlencode({'field1': temperature, 'field2': humidity,'key':api_key})
  headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
  conn = httplib.HTTPConnection("api.thingspeak.com:80")
  conn.request("POST", "/update", params, headers)
  response = conn.getresponse()
  print response.status, response.reason
  data = response.read()
  conn.close()

# Continuously append data
while(True):
  # Run the DHT program to get the humidity and temperature readings!

  output = subprocess.check_output(["./Adafruit_DHT", "2302", "4"]);
  print output
  matches = re.search("Temp =\s+([0-9.]+)", output)
  if (not matches):
	time.sleep(3)
	continue
  temp = float(matches.group(1)) * 9 / 5 + 32
  
  # search for humidity printout
  matches = re.search("Hum =\s+([0-9.]+)", output)
  if (not matches):
	time.sleep(3)
	continue
  humidity = float(matches.group(1))

  print "Temperature: %.1f F" % temp
  print "Humidity:    %.1f %%" % humidity
 
  submit(temp, humidity)

  # Wait 30 seconds before continuing
  time.sleep(10)
