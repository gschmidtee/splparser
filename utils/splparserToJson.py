###############################################
# initial code sample produced by: Sara Alspaugh
# date: 11/6/2017
# modified by: BAH, Greg Schmidt
# - added cmd args and usage
# - added writeJson
# date: 11/6/2017 
###############################################

import sys
sys.path.append('../')
import json
import getopt
import json
import io


###############################################
## usage for cmd args
###############################################
def usage():
  print 'python splparserToJson.py -h -s <Splunk_search_query>'
  print ' -h : help menu'
  print ' -o : output filename'
  print ' -s : Splunk search query'
  print '-----------------------------------------------------'
  print ' e.g. python splparserToJson.py -o testout.json -s "sourcetype=access method=GET learn"'


###############################################
## write data to json
###############################################
def writeJson(data, filename):
  try:
    to_unicode = unicode
  except NameError:
    to_unicode = str

  # Write JSON file
  with io.open(filename, 'w', encoding='utf8') as outfile:
    str_ = json.dumps(data, indent=2, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))


###############################################
# global parameters
###############################################
query = "*"
outputfilename = "queryOutput.json"

import splparser


###############################################
# process command arguments
###############################################
try:
  opts, args = getopt.getopt(sys.argv[1:], "hs:o:")
except getopt.GetoptError:
  usage()
  sys.exit(2)
for opt, arg in opts:
  if opt == '-h':
    usage()
    sys.exit(0)
  elif opt == '-o':
    outfilename = arg
  elif opt == '-s':
    query = arg
  else:
    usage()
    sys.exit(2)

print "Search query = " + query


###############################################
# main processing 
###############################################

parsetree = splparser.parse(query)
parsetree_as_json = parsetree.jsonify()


###############################################
# dump the json to file 
###############################################

writeJson(parsetree_as_json, outfilename)
