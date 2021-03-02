
from functions import *


# Extracts headers in a separate table
# Runtime: 100.789 seconds
def extract_headers(go_ind):
    if go_ind == 1:
        return
    start_time = start_function('extract_headers')
    # Connect to database
    db = dbi()
    conn = db[0]
    cur = db[1]
    tname = 'dev_all_parts_headers'
    tname_orig = 'dev_all_parts2'
    # Create new table from original instead of creating it from scratch
    qry = '''drop table if exists %s;
             create table %s as
             select * from %s limit 1;
             truncate table %s;
             alter table %s drop column %s;
             '''
    cur.execute(qry,
                (AsIs(tname),
                 AsIs(tname),
                 AsIs(tname_orig),
                 AsIs(tname),
                 AsIs(tname),
                 AsIs('id_num')
                ))
    # Run for the real results
    cur.execute('select * from %s order by %s;',
                (AsIs(tname_orig),
                AsIs('id_num')
                ))
    results = cur.fetchall()
    lfile = init_write_file('log/log_add_headers.txt')    
    with open(lfile, 'w', encoding = 'utf8') as lf:
        for i in results:
            idnum = str(i[12])
            print('%s - %s - %s' % (idnum, i[0], i[5]), end = '', file = lf)
            # Start extracting headers
            extract_h1(conn, tname, i, lf)
            extract_h2(conn, tname, i, lf)
            #lf.write(pstr)
    # Finish
    conn.commit()
    cur.close()
    end_function(start_time)


# For parts
def extract_h1(connection, table_name, record, file_name):
    soup = bsp(record[9], 'html.parser')
    headers = soup.find_all('h1')
    if len(headers) == 0:
        print(' - No', end = '', file = file_name)
        return
    # Insert into table, only changing the html and type
    lst = [record[0],
           # subpart
           record[1],
           # section
           record[2],
           # subsection
           record[3],
           # paragraph
           record[4],
           # reg
           record[5],
           # htype
           'header',
           # fac
           record[7],
           # hlink
           record[8],
           # htext
           str(headers[0]),
           # order_num
           record[10],
           # import_date
           datetime.datetime.now()
           ]
    insert_values(connection, table_name, tuple(lst))
    print(' - +', end = '', file = file_name)
    

# For subparts
def extract_h2(connection, table_name, record, file_name):
    soup = bsp(record[9], 'html.parser')
    headers = soup.find_all('h2')
    if len(headers) == 0:
        print(' - No', file = file_name)
        return
    for i in headers:
        header = i.get_text().strip()
        hsplit = header.split()
        hstr = ''
        # For most other subparts
        try:
            header[0].isalpha()
            spart = hsplit[1].split('.')[1]
            typ = 'header'
        # For scope
        except:
            spart = 0
            if 'scope' in header:
                typ = 'scope'
            elif 'definitions' in header:
                typ = 'definitions'
            else:
                typ = 'other'
        # Insert values
        lst = [record[0],
               # subpart
               str(spart),
               # section
               record[2],
               # subsection
               record[3],
               # paragraph
               record[4],
               # reg
               record[5],
               # htype
               typ,
               # fac
               record[7],
               # hlink
               record[8],
               # htext
               str(i),
               # order_num
               record[10],
               # import_date
               datetime.datetime.now()
               ]
        insert_values(connection, table_name, tuple(lst))
    print(' - +', file = file_name)


# Used for debugging paragraphs
# Modify file_name and idnum as appropriate
def mod_protocol0(idnum, file_name, file_save):
    # Connect to database
    db = db_init()
    conn = db[0]
    cur = db[1]
    tname1 = 'dev_all_parts05'
    qry_str1 = 'select * from {table1} where {field1} = %s;'
    qry1 = sql.SQL(qry_str1).format(table1 = sql.Identifier(tname1),
                                    field1 = sql.Identifier('protocol')
                                    )
    values1 = (0, )
    res = qry_execute(conn, qry1, values1, True)
    reg = res[0][1]
    part = res[0][2] 
    url = res[0][8]
    html = res[0][9]
    soup = bsp(html, 'html.parser')
    # Start parsing html
    lfile = init_write_file('log/log_protocol0.txt')
    with open(lfile, 'w', encoding = 'utf8') as lf:
        # Test to see if all articles are the same
        article_lst = ['nested3', 'nested2', '2Col', 'nested1', 'nested0']
        for i in res:
            soup2 = bsp(i[9], 'html.parser')
            for j in soup2.find_all('article', limit = 10):
                # Need to this in case the articles doesn't have a class
                try:
                    ind = 0
                    for k in j['class']:
                        # Only list article if its not in the lst
                        if k in article_lst:
                            ind = 1
                            break
                    if ind == 0:
                        print('%s - %s' % (i[0], j.attrs), file = lf)
                # Runs if there are no classes for the article
                except:
                    print('%s - No classes' % (i[0]), file = lf)
                
                
                
                
                # try:
                #     for k in j['class']:
                        
                #         if k not in article_lst:
                #             print('%s - %s' % (i[0], j.attrs), file = lf)
                #         else:
                #             continue
                # except:
                #     continue
        return
    
        for i in soup.find_all('br'):
            i.unwrap()
        # Remove all span classes and subsequent autonumbers
        for i in soup.find_all('span'):
            i.unwrap()
        # Remove emphasis classes
        for i in soup.find_all('em'):
            i.unwrap()
        # Remove nav classes
        for i in soup.find_all('nav'):
            i.extract()
        # Fix the TOC
        div_toc = soup.find('div', class_ = 'body')
        if div_toc is not None:
            # Change the class name to toc
            div_toc['id'] = 'toc'
            # Reformat the text in the a tags and modify the href's
            for i in div_toc.find_all('a'):
                txt = i.get_text().strip()
                i.string = txt
                i['href'] = header_ids(reg, part, txt, True)
        else:
            print('No div body', file = lf)
        # Remove all formatting from tables
        for i in soup.find_all('table'):
            del i['class']
            for j in i.find_all('th'):
                del j['class']
                del j['id']
            for j in i.find_all('td'):
                del j['class']
            for j in i.find_all('p'):
                j.unwrap()
        # List all headers
        for i in soup.find_all(re.compile('^h[1-6]$')):
            # Remove all classes
            del i['class']
            hstr = i.get_text().strip()
            i.string = hstr
            orig_id = i['id']
            # Assign new IDs and replace with the old
            new_id = header_ids(reg, part, hstr, False)
            i['id'] = new_id
        # Remove all links to the FAR - they won't work anyway in the app
        for i in soup.find_all('a'):
            try:
                ih = i['href']
                if not ih.startswith('http') and not ih.startswith('#' + reg):
                    i.unwrap()
            except:
                continue
                #print('Unwrapping - %s' % ih, file = lf)
        
        ######################################################################
        # Try using wrap() to wrap all the other content in a new div
        
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
#        return
        
        # Extract all articles and save in the db
        tname2 = 'dev_all_html02'
        values2 = '''(reg varchar,
                      part numeric,
                      subpart numeric,
                      sction numeric,
                      subsction numeric,
                      htype varchar,
                      hlink varchar,
                      htext varchar
                      )'''
        drop_create_tables(conn, tname2, values2)
        # Start adding all text individually based on article classes
        # nested3 = subsections
        # nested2 = sections
        # 2Col = table with two columns
        # nested1 = subparts
        # nested0 = parts
        for i in ['nested3', 'nested2', '2Col', 'nested1', 'nested0']:
            for j in soup.find_all('article', class_ = i):
                if j is None:
                    continue
                # Extract the first heading id number for the DB
                hid = j.find(re.compile('^h[1-6]$'))
                # Remove empty paragraphs
                for k in j.find_all('p'):
                    if k.find('article') or len(k.get_text()) <= 1:
                        k.unwrap()
                insert_htext(conn, tname2, hid['id'], j, url)
                # Remove so text won't be copied again
                j.decompose()


        
        #     print('%s%s%s%s%s' % ('\n' + ('#' * 80),
        #                         '\n',
        #                         i,
        #                         '\n\n',
        #                         i.parent.parent
        #                         ), file = lf)
        # return
        #     #print(i, file = lf)
        #     para_cit = i.string.split()[0]
        #     if para_cit[0] == '(':
        #         lst.append(para_cit[1])
        #         #print(para_cit, file = lf)
        #     else:
        #         lst.append('Skipping')
        #         #print('%s %s' % ('+' * 40, para_cit), file = lf)
        # print(lst, file = lf)
        
    # Save to file only if specified
    jname = init_write_file(file_name)
    if file_save:
        with open(jname, 'w', encoding = 'utf8') as jf:
            jf.write(soup.prettify())
            jf.close()
    db_close(conn, cur)

        
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
# 1 for debug, 0 for extract_headers


# Returns the new ID for each header or href; prepends with # if returning href
def header_ids(reg, part, text, toc_ind):
    hspl = text.split()
    hs0 = hspl[0]
    hs1 = hspl[1]
    # Parts
    if hs0.lower() == 'part':
        id_str = '%s_%s_%s_%s_%s_%s' % (reg, part, 0, 0, 0, 'header')
    # Subparts
    elif hs0.lower() == 'subpart':
        hspl2 = hs1.split('.')
        id_str = '%s_%s_%s_%s_%s_%s' % (reg, part, hspl2[1], 0, 0, 'header')
    # Sections
    elif hs0.find('-') == -1:
        hspl2 = hs0.split('.')
        hsp1 = hspl2[1]
        sp_s = header_link_section(hsp1)
        id_str = '%s_%s_%s_%s_%s_%s' % (reg, part, sp_s[0], sp_s[1], 0, 'body')
    # Subsections
    elif hs0.find('-') != -1:
        ss_spl = hs0.split('-')
        hspl2 = ss_spl[0].split('.')
        hsp1 = hspl2[1]
        sp_s = header_link_section(hsp1)   
        id_str = '%s_%s_%s_%s_%s_%s' % (reg, part, sp_s[0], sp_s[1], ss_spl[1], 'body')
    # print('%s ##### %s' % (text, id_str))
    if toc_ind:
        return '#' + id_str
    else:
        return id_str
    

# Returns the section and subsectino; used with header_ids
def header_link_section(text):
    if len(text) == 3:
        subpart = text[0]
        sction = text[1:]
        if sction == '00':
            sction = '0'
        else:
            sction = sction.lstrip('0')
    elif len(text) == 4:
        subpart = text[:2]
        sction = text[2:]
        if sction == '00':
            sction = '0'
        else:
            sction = sction.lstrip('0')
    else:
        return 'Section is not 3 or 4 characters long...'
    return (subpart, sction)


# Insert htext sections in dev_all_html02
def insert_htext(connection, table_name, header_id, text, url):
    # The header IDs need to be the ones we made, exit function if not
    if header_id.count('_') < 5:
        return
    hid_spl = str(header_id).split('_')
    # Start adding values
    values = (hid_spl[0],
              # part
              hid_spl[1],
              # subpart
              hid_spl[2],
              # sction
              hid_spl[3],
              # subsction
              hid_spl[4],
              # htype
              hid_spl[5],
              # hlink
              url,
              # htext
              str(text)
              )
    insert_values(connection, table_name, values)

    


go_ind = 1
mod_protocol0(754,'html/dev_contents1.html', False)
extract_headers(go_ind)





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

