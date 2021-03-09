
from functions import *


# Works! Use this as a way to combine all into articles
def dev_next():
    # Connect to database
    db = db_init()
    conn = db[0]
    cur = db[1]
    html = '''<html><title>Test Title</title><b>This is supposed to be a title</b><p>Paragraph 1</p><p>Paragraph 2</p><p>Paragraph 3</p><b>This is supposed to be another title</b><p>Paragraph 4</p><p>Paragraph 5</p><p>Paragraph 6</p></htnl>'''
    soup = bsp(html, 'html.parser')
    for i in soup.find_all('b'):
        # First save i as hlist as the initial
        hlist = str(i)
        # Search for same-level tags, which should be paragraphs
        for j in i.find_next_siblings():
            # Stop recursing as soon as we hit another bold
            if j.name == 'b':
                break
            # Keep adding values to hlist
            hlist += str(j) + ''
            # Remove tag from tree as soon as we successfully add it
            j.decompose()
        # Add article to encompass all the text
        ntag = soup.new_tag('article')
        ntag['class'] = 'nested2'
         # hlist is currently a string - it needs to be converted to html       
        ntag.append(bsp(hlist, 'html.parser'))
        # Replace the current bold to the new tag
        i.replace_with(ntag)
    print('%s\n%s' % (cb(), soup.prettify()))
    
    


str1 = 'SUBPART 5601.1 - PURPOSE, AUTHORITY, ISSUANCE'
if re.match('.*(\s)part(\s)[1-9].*', str1, re.I):
    print('yay')


