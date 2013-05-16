import quopri
import json
import os, errno

HOME = "/Users"
USER = "raymond"
DIR = "Projects/semantix"
FILE = "cpk.txt"
OUTPUT = "out.txt"

file = open("/".join([HOME, USER, DIR, FILE]), 'r')

#just a string
line1 = file.readlines()

#get the body (unicode) of the first object in the JSON
body = json.loads(line1[0]).values()[0]

#use the quopri module to decode the qp_encoded body of each page
#but in this case just decoding the first body of the loading page
decoded_qp = quopri.decodestring(body)

#remove the file if exists
try:
    os.remove("/".join([HOME, USER, DIR, OUTPUT]))
except OSError:
    pass

#write decoded body to output file
out_file = open("/".join([HOME, USER, DIR, OUTPUT]), 'w')
out_file.write(decoded_qp)
out_file.close()
