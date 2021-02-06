# Parse-out FAR part and its name
# Originally, the part names were going to be pulled into each respective
#   citation, but this doesn't seem necessary anymore
# This will still stay in the file though...

import os
from os import path
import json

###############################################################################
# FUNCTIONS

# Add commas and convert to json
def conv_json(file):
  # Convert all dictionaries to strings, then add commas inbetween each object
  with open(file, 'r') as jf:
    contents = jf.read()
    contents = contents.replace('}{', '},{')
  # Overwrite old file with new changes as a list of strings
  with open(file, 'w', encoding = 'utf8') as jf:
    jf.write(contents)
  # Finally, reconvert the file back to a json file
  with open(file, 'r') as jf:
    contents = json.load(jf)
  with open(file, 'w', encoding = 'utf8') as jf:
    json.dump(contents, jf, indent = 2)
    
###############################################################################
# ADD DATA

# Remove all file contents before writing anything, but only if it exists
jname = os.path.basename(__file__).split('.')[0]
jname = 'json/' + jname + '.json'
if path.exists(jname): open(jname, 'w').close()

# https://acqnotes.com/acqnote/careerfields/federal-acquisition-regulation-index
far = [
       'Part 1-Federal Acquisition Regulations System', 
       'Part 2-Definitions of Words and Terms', 
       'Part 3-Improper Business Practices and Personal Conflicts of Interest', 
       'Part 4-Administrative Matters', 
       'Part 5-Publicizing Contract Actions', 
       'Part 6-Competition Requirements', 
       'Part 7-Acquisition Planning', 
       'Part 8-Required Sources of Supplies and Services', 
       'Part 9-Contractor Qualifications', 
       'Part 10-Market Research', 
       'Part 11-Describing Agency Needs', 
       'Part 12-Acquisition of Commercial Items', 
       'Part 13-Simplified Acquisition Procedures', 
       'Part 14-Sealed Bidding', 
       'Part 15-Contracting by Negotiation', 
       'Part 16-Types of Contracts', 
       'Part 17-Special Contracting Methods', 
       'Part 18-Emergency Acquisitions', 
       'Part 19-Small Business Programs', 
       'Part 20-[RESERVED, not currently in use]', 
       'Part 21-[RESERVED, not currently in use]', 
       'Part 22-Application of Labor Laws to Government Acquisitions', 
       'Part 23-Environment, Energy and Water Efficiency, Renewable Energy Technologies, Occupational Safety, and Drug-Free Workplace', 
       'Part 24-Protection of Privacy and Freedom of Information', 
       'Part 25-Foreign Acquisition', 
       'Part 26-Other Socioeconomic Programs', 
       'Part 27-Patents, Data, and Copyrights', 
       'Part 28-Bonds and Insurance', 
       'Part 29-Taxes', 
       'Part 30-Cost Accounting Standards Administration', 
       'Part 31-Contract Cost Principles and Procedures', 
       'Part 32-Contract Financing', 
       'Part 33-Protests, Disputes, and Appeals', 
       'Part 34-Major System Acquisition', 
       'Part 35-Research and Development Contracting', 
       'Part 36-Construction and Architect-Engineer Contracts', 
       'Part 37-Service Contracting', 
       'Part 38-Federal Supply Schedule Contracting', 
       'Part 39-Acquisition of Information Technology', 
       'Part 40-[RESERVED, not currently in use]', 
       'Part 41-Acquisition of Utility Services', 
       'Part 42-Contract Administration and Audit Services', 
       'Part 43-Contract Modifications', 
       'Part 44-Subcontracting Policies and Procedures', 
       'Part 45-Government Property', 
       'Part 46-Quality Assurance', 
       'Part 47-Transportation', 
       'Part 48-Value Engineering', 
       'Part 49-Termination of Contracts', 
       'Part 50-Extraordinary Contractual Actions', 
       'Part 51-Use of Government Sources by Contractors', 
       'Part 52-Solicitation Provisions and Contract Clauses', 
       'Part 53-Forms'
      ]

# Start writing to file
with open(jname, 'w', encoding = 'utf8') as jf:
  # Add open bracket before adding data through loop
  jf.write('[')
  # Perform multiple splits to separate the '-' and the spaces
  for i in far:
    spl1 = i.split('-')
    fpart = spl1[0]
    spl1 = fpart.split(' ')
    fpart2 = spl1[1]
    fpart3 = fpart + '-'
    fname = i.replace(fpart3, '')
    # Create dictionary to start adding values
    d = {
         'part': int(fpart2),
         'name': str(fname)
        }
    json.dump(d, jf, indent = 2)
  # Add closing brackets after for loop ends
  jf.write(']')

# At this stage, json files are actually lists with strings
# This turns them into actual json files
conv_json(jname)

print('Finished pushing data to ' + jname)

###############################################################################
# CLEAN-UP DATA

with open(jname, 'r') as jf:
  data = json.load(jf)
  for i in data:
    # Replace original 'RESERVED' string to just one word
    if 'RESERVED' in i['name']:
      i['name'] = 'RESERVED'
  # Save new data over the old data
  data = data

# New data overrites old data
with open(jname, 'w', encoding = 'utf8') as jf:
  json.dump(data, jf, indent = 2)

print("Fished updating " + jname)

