from bs4 import BeautifulSoup
import quopri
import json
import os, errno

INPUT_FILE = "cpk.txt"
OUTPUT_FILE = "out.txt"

#remove the file if exists
try:
    os.remove(OUTPUT_FILE)
except OSError:
    pass

# Open the file.
inputFile = open(INPUT_FILE, 'r')
# Read the file contents.
lines = inputFile.readlines()

# Loop through each line in the file.
index = 0
for line in lines:
    line = lines[index]
    index += 1

    # load the line and the value that we want.
    body = json.loads(line).values()[0]

    # Use the quopri module to decode the qp_encoded value of each page.
    decoded_qp = quopri.decodestring(body)
    soup = BeautifulSoup(decoded_qp)

    print soup.title

    # Write decoded values to the output file.
    out_file = open(OUTPUT_FILE, 'a')
    out_file.write(decoded_qp)
    out_file.write("\n")
    out_file.close()

