
from functions_add_json import *

#search_css('autonumber')
#search_jscripts('autonumber')

str1 = 'i'
if str1[0] in 'ivx': print('good')






# for far, dfars, dfars pgi, gsam:
# h1 = Parts
# h2 = Subparts
# h3 = Sections
# h4 = Subsections
#
# TOC:
# div class= 'body'
#
# Content:
# article role= 'article'
# div class= 'body conbody'
# *To pull data, get all get_text between two headings
# *Each subsection gets its own division?
#
# Pararaphs
# FAR will always be in this format per FAR 1.105-2:
# (a)
# (1)
# (i)
# (A)
# (1)
# (I)




# for supplementals:
# h1 = Parts
# h2 = Subparts
# h3 = Sections
# h4 = Subsections
#
# TOC:
# *Usually not found...
# div class= 'field-items'
# div id='Table of Contents1"
# *Create my own? Ugh...
#
# Content:
# div class= 'field-items'
# *To pull data, get all get_text between two headings
# *Each subsection gets its own division?










# Steps:
# 1) Save current TOC into json file, links to each section
# 1a) Possibly save TOC and reformat structure, along with each a href
# 2) From this TOC json file, iterate over each section then save those sections
#    as independent json files
# 3) Fix paragraphs now or later?



















# with open(hname2, 'w', encoding = 'utf8') as hn2:
#   soup = bsp(contents, 'html.parser')
#   res = soup.find_all('tbody')
#   for i in res:
#     hn2.write(str(i.prettify()))
#     break






# open the url and save it as an html object
# resp = ul.request.urlopen(res)
# html_res = resp.read()

# turn it into html and parse out the content
# text is always found in the <div id="middlecontent"> area on the webpage
# soup = bsp(html_res, 'html.parser')
# reg_txt = soup.find('div', id = 'middlecontent')

# with open(hfile, 'w', encoding = 'utf8') as h:
#   h.write(reg_txt.prettify())
#   h.close()

#print(reg_txt.prettify())
# look into .extrar() for beautiful soup to extract contents in between tags
# changin the names of tags and attributes





# reg
# part
# subpart
# section
# http_link
# html

# regulation-index-browse_wrapper














