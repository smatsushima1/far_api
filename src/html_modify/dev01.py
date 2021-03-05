
from functions import *
    




# go_ind = 1
# mod_protocol0(961)
# mod_protocol0('html/dev_contents1.html', True)
# extract_headers(go_ind)
# html_pull(130, 'html/dev_contents2.html')







######################################################################
# Try using wrap() to wrap all the other content in a new div

# Also, search in the bsp documentation to find tags directly beneath other tags:

    
######################################################################
# Make all text look pretty
        # for x, j in enumerate(i):
        #     # Make all the text look pretty
        #     hstr1 = j.get_text().strip()
        #     hsplit = hstr1.split()
        #     hstr2 = ''
        #     for k in hsplit:
        #         hstr2 += k + ' '
        #     print(hstr2 + '\n')
        #     if x == 4:
        #         break


######################################################################
# Separate each article by section and save this into another table
#        for j in soup.find_all('h2', limit = 5):
#            print('#' * 80, file = lf)            
    # hid = j['id']
#     for k in soup.find('h4', id = hid).find_previous_siblings():
#         print(j, file = lf)
#         print(k.previous, file = lf)
    # h2res = soup2.find('h2', id = j['id'])

    # print('\n', file = lf)
    # print(j.get_text().lstrip(), file = lf)
    # print('\n', file = lf)
#            print(j, file = lf)
    # print('\n', file = lf)
#            print(j.next_sibling.next, file = lf)
    # for k in j.find_previous_siblings():
    #     print(k, file = lf)
    # print('\n', file = lf)
    # print(j.previous_sibling, file = lf)
#print(soup2.find('h2', id="ariaid-title3").nextSibling.next)

##############################################################################
# 21 February:
# - great progress! - the database needed much cleaning
# - everything seems cleaned for now...
# - first started extracting headers but lots to improve:
#    - route stdout to a file
#    - add in scope and definition types
#    - be sure subparts can be entered in
#    - read over data in db and find missing information
#    - lots of regs left early...

##############################################################################
# Possible steps forward:
# - create separate functions for parsing headers of different types
#     - traditional headings (god bless them)
#     - bold headings
#     - strong headings (why...)
#     - missplaced h2 headings
# - all these should add up to the total amount of records we have to parse
# - maybe first iterate through each reg and fix headings, then worry about
#       other stuff within
#     - headings will serve as the basis to grab the other information

##############################################################################
# Desired format:
# - only headers in the regular format
# - only paragraphs
#     - first isolate all sections, remove all formatting, convert to paragraphs
#     - no lists
# - no unaltered

##############################################################################
# Add attributes to tags
    # headers = soup.find_all('h1')
    # for i in headers:
    #     header = i.get_text().strip()
    #     hsplit = header.split()
    #     hstr = ''
    #     for j in hsplit:
    #         hstr += j + ' '
    #     print(hstr)
    #     soup2 = bsp(hstr, 'html.parser')
    #     htag = soup2.new_tag('h2')
    #     htag.string = hstr
    #     htag['href'] = '#ugh_derp'
    #     print(htag)

##############################################################################
# Inserts new div class
        # new_div = soup.new_tag('div', class_ = 'text')
        # div_ntoc = soup.find('div', class_ = 'toc')
        # div_ntoc.insert_after('', new_div)

##############################################################################
# Replace class with a new one
# For j in soup.find_all('h5'):
    # hchange = header_change(reg, hstr)
    # if hchange == 1:
    #     ntag = soup.new_tag('b')
    #     ntag.string = j.string
    #     j.insert_after(ntag)
    #     j.unwrap()

##############################################################################
# Multiple try except attempts
    # Use this for TOC, if thats what you want...
    #print(h1_text)
    # try:
    #     toc = soup.find('div', class_ = 'body')
    # except AttributeError:
    #     pass
    # try:
    #     toc = soup.find('div', id = 'Table of Contents1')
    # except:
    #     toc = ''
    # toc_final = str(main_title) + str(toc)
    # print(toc_final)
    # for x, j in enumerate(soup2.find('div', class_ = )


##############################################################################
# Remove span classses
    # Remove all span classes in their separate objects
    # for i in soup.find_all('span'):
    #     i.unwrap()


##############################################################################
# Separate contents of sections/subsections
    # Use this for headers
    # Separate each article by section and save this into another table
    # for x, j in enumerate(soup2.find_all('h2')):
    #     if x == 2:
    #         # h2res = soup2.find('h2', id = j['id'])
    #         print(j.get_text().lstrip())
    #         print(j)
    #         print(j.next_sibling.next)
    #     else:
    #         continue
        # print(j['id'])
        # print(soup2.find_next_sibling('h2', id = j['id']))
    # print(soup2.find('h2', id="ariaid-title3").nextSibling.next)


##############################################################################
# Different types
# We'll make our own TOC!!!!!! Don't Extract!!!
# Insert all headings as titles
# Meaning, we will have:
# - main: all text combined
# - toc: table of contents
# - header: titles of subparts
# - body: sections and subsections


# Steps:
# 1) Save current TOC into json file, links to each section
# 1a) Possibly save TOC and reformat structure, along with each a href
# 2) From this TOC json file, iterate over each section then save those sections
#    as independent json files
# 3) Fix paragraphs now or later?


########################### For FAR, DFARS. GSAM... ###########################
# h1 = Parts
# h2 = Subparts
# h3 = Sections
# h4 = Subsections

# TOC:
# div class= 'body'

# Content (FAR, DFARS, GSAM):
# article role= 'article'
# div class= 'body conbody'
# *To pull data, get all get_text between two headings
# *Each subsection gets its own division?

# All contents:
# div class='nested0'


################################ Supplementals ################################
# h1 = Parts
# h2 = Subparts
# h3 = Sections
# h4 = Subsections

# TOC:
# *Usually not found...
# div class= 'field-items'
# div id='Table of Contents1"
# *Create my own? Ugh...

# Content:
# div class= 'field-items'
# div id='middlecontent'
# field-items consists of everything, including table of contents
# *To pull data, get all get_text between two headings
# *Each subsection gets its own division?

# All contents:
# div id='middlecontent'


# regulation-index-browse_wrapper
# look into .extrar() for beautiful soup to extract contents in between tags
# changin the names of tags and attributes

