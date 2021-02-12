
import os
from os import path
import json
from bs4 import BeautifulSoup as bsp
import urllib as ul
import re


#################################### Basics ###################################
# Remove all file contents before writing anything, but only if it exists
def rem_file(fname, dname):
    file_name = dname + '/' + fname + '.' + dname
    if path.exists(file_name):
        open(file_name, 'w').close()
    return file_name


def success_comp(fname):
    print('Succesfully completed: ' + fname + '\n')
     
     
################################# JSON Parsing ################################
# Parse-out FAR part and its name
# Originally, the part names were going to be pulled into each respective
#   citation, but this doesn't seem necessary anymore
# This will still stay in the file though...
def add_far_parts():
    jname = rem_file('far_parts', 'json')

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
    
    dlist = []
    for i in far:
        spl = i.split('-')
        part = spl[0]
        name = spl[1]
        fpart = part.split(' ')[1]
        fname = name.replace(fpart + '-', '')
        # Error checks
        if 'RESERVED' in fname:
            fname = 'RESERVED'
        dlist.append({'part': int(fpart), 'name': str(fname)})
    json.dump(dlist, open(jname, 'w', encoding = 'utf8'), indent = 2)  
    success_comp(jname)


# Add links to href sits
def add_reg_links():
    jname = rem_file('reg_links', 'json')
    
    # The following string could have been anywhere on acq.gov
    srch = 'https://www.acquisition.gov/browse/index/far'
    # Open the url and save it as an html object
    resp = ul.request.urlopen(srch)
    html_res = resp.read()
    # Turn it into html and parse out the content
    soup = bsp(html_res, 'html.parser')
    htext = soup.find('div', class_ = 'reg-container clearfix')
    res = htext.find_all('a')
    
    dlist = []
    for i in res:
        rtext = i.get_text()
        reg = rtext.strip()
        hrtext = i.attrs['href']
        href = hrtext.strip().replace('/browse/index', '')
        # Error checks
        if 'Smart' in reg:
            continue  
        dlist.append({'reg': reg, 'link': str(href)})
    # Add AFFARS regs to the list
    dlist.append({'reg': 'AFFARS MP', 'link': '/affars/mp'})
    dlist.append({'reg': 'AFFARS PGI', 'link': '/affars/pgi'})
    json.dump(dlist, open(jname, 'w', encoding = 'utf8'), indent = 2)  
    success_comp(jname)
    

# Start extracting links to the Parts and save href in json file
def add_all_parts():
    jname = rem_file('all_parts', 'json')
    
    # An empty dictionary is created because, there will be objects with lists
    data = json.load(open('json/reg_links.json', 'r'))
    d = {}
    for i in data:
        htext = str(i['link'])
        reg = htext.strip('/')
        print('Adding data to: ' + reg)
        d[i['reg']] = parts_hrefs(reg, htext)
    json.dump(d, open(jname, 'w', encoding = 'utf8'), indent = 2)
    success_comp(jname) 


# Parse each part for each regulation; used with add_all_parts
def parts_hrefs(regulation, htext):
    # Open the url and save it as an html object
    reg = regulation.strip()
    reg = reg.strip('_')
    base = 'https://www.acquisition.gov'
    hlink = base + htext
    html = ul.request.urlopen(hlink).read()
    hsoup = bsp(html, 'html.parser')
    # Finding this div applies to FAR, DFARS, and GSAM
    # If there were no results, it would be a null object
    hres = hsoup.find('div', id = 'parts-wrapper')
    if hres is not None:
        # All the a tags have our information within the div tag   
        res = hres.div.find_all('a')
        ind = 1
    # This only gets run for supplementals
    # The tbody tag will always have our information
    # The td tags have long class names, so regex was needed to parse it
    else:
        res = hsoup.tbody.find_all('td', class_ = re.compile('.*part-number'))
        ind = 0
    dlist = add_to_dict(reg, res, base, ind)
    return dlist


# Returns dictionary of objects; used with parts_href
# JSON objects will be structured:
# {"part": ,
#  "subpart": ,
#  "section": ,
#  "subsection": ,
#  "reg": ,
#  "type": ,
#  "fac": ,
#  "link": ,
#  "html":
#  }
def add_to_dict(regulation, rlist, addr, reg_ind):
    dlist = []
    for i in rlist:
        # The part numbers will always just be the text
        hpart = return_part(i.get_text()).strip()
        part_final = final_part(hpart)
        # If its for the main regs, 'href' will be in the 'attrs'
        if reg_ind == 1:
            hlnk = addr + i.attrs['href'].strip()
        else:
            hlnk = addr + i.a['href'].strip()
        ret_text = {'part': part_final,
                    'subpart': 0,
                    'section': 0,
                    'subsection': 0,
                    'reg': regulation.replace('/', ''),
                    'type': 'main',
                    'fac': '2021-04',
                    'link': hlnk,
                    'html': 'N/A'
                    }
        dlist.append(ret_text)
    return dlist


# Returns the part number regardless of what type it is; used with parts_href
def return_part(ptext):
    sp_text = ptext.split()
    cnt = len(sp_text)
    # If its just a number, the list will be 1 object
    if cnt > 1:
        ptext = sp_text[cnt - 1]
    return ptext


# Return only the far equivalent part; used with add_to_dict
def final_part(part):
    strip_part1 = part.strip("mp_")
    strip_part2 = strip_part1.strip("pgi_")
    lp = len(strip_part2)
    if lp <= 2:
        return strip_part2
    elif lp == 3:
        if strip_part2[1] == str(0):
            return strip_part2[2]
        else:
            return strip_part2[1:]
    elif lp == 4:
        if strip_part2[2] == str(0):
            return strip_part2[3]
        else:
            return strip_part2[2:]
    else:
        return strip_part2


########################## CSS and JavaScript Parsing #########################
# Only one result found for 'autonumber', but not usable
def search_css(search_text):
    # First find CSS sheets
    html = open('html/css_sheets.html', 'r').read()
    # Turn it into html and parse out the content
    soup = bsp(html, 'html.parser')
    htext = soup.find_all('style')
    # First add all values in list
    list1 = []
    for i in htext:
        for j in i:
            list1.append(j)
    # Add the values of the previous list into another list
    list2 = []
    for k in list1:
        res = k.split(';')
        for l in res:
            if l == '':
                continue
            list2.append(l)
    # Parse the html out of each item and save to a new list
    list3 = []
    for m in list2:
        start = m.find('("') + len('("')
        end = m.find('")')
        link = m[start:end]
        if link == '':
            continue
        list3.append(link)
    # Search in each link and print each result if it contains the styles
    for n in list3:
        html = ul.request.urlopen(n).read()
        if search_text in str(html):
            print('Results found in: ' + n)


# Search through each script tag
# No results found for 'autonumber'
def search_jscripts(srch_text):
    html = open('html/css_sheets.html', 'r').read()
    # Turn it into html and parse out the content
    soup = bsp(html, 'html.parser')
    htext = soup.find_all('script')
    # First add all values in list
    list4 = []
    for p in htext:
        if p.attrs['src'].startswith('//code'):
            continue
        list4.append(p.attrs['src'])
    # Search for string inside each jscript file
    for q in list4:
        txt = ul.request.urlopen(q).read()
        if srch_text in str(txt):
            print('Results found in: ' + q)


# The results of the searches suggest that the tags I'm looking for are
# embedded somewhere else. If I can't find them anywhere, then the only
# other way to go about this is to save everything as is and apply my own
# tags. For obvious reasons, this would be much too impractical. It would
# invovled:
# - saving all the text as is, only find non-header tags, check to see if it
#   starts with an open parenthesis then go to the first close parenthesis
# - this would leave me to parse-out the paragraph
# - depending on what type of paragraph it is, it could require a specific
#   indent
# - we already know the strucutre of the FAR, so this would be a simple test
# - they will always go a, 1, i, A, 1, i
# - knowing this would mean I can set-up indents based on what value this is


# Links within html should be the following:
#   PART_SUBPART_SECTION_SUBSECTION_REG_TYPE
# For example: FAR 1.105-2 = 1_1_5_2_far_body
# PART: integers from 0-53
# SUPBART: integers from 0-?
# SECTION: integers from 0-?
# SUBSECTION: integers from 0-?
# REG: the regulation in lower case with no spaces; citations shall not include
#      the supplemental regulation number in front; for example, a reference
#      for DFARS 202.101 will not be 202_1_1_0_dfars_body, but instead will be
#      1_1_1_0_dfars_body
# TYPE: the type of link in reference:
#   - body: the most prevalent, the citation html body
#   - toc: the toc for each part and each associated regulation
#   - main: the concatentation of the toc, and all appropriate bodies

# As such, the associated json objects will be structured similarly:
# {"part": ,
#  "subpart": ,
#  "section": ,
#  "subsection": ,
#  "reg": ,
#  "type": ,
#  "fac": ,
#  "link": ,
#  "html":
#  }





































