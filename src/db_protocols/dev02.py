
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
    

def dev_next2():
    # Connect to database
    db = db_init()
    conn = db[0]
    cur = db[1]
    html = '''<html><title>Test Title</title><b>This is supposed to be a title</b><p>Paragraph 1</p><p>Paragraph 2</p><p>Paragraph 3</p><b>This is supposed to be another title</b><p>Paragraph 4</p><p>Paragraph 5</p><p>Paragraph 6</p></htnl>'''
    soup = bsp(html, 'html.parser')
    res = soup.find_all('ol')
    if res:
        print('yay')
    else:
        print('nopw')


#dev_next2()

# Extract bold headers
# Runtime: 0.094"
def extract_bheaders(id_num, log_file, get_text_ind):
    start_time = start_function('extract_bheaders')
    # Connect to database
    db = db_init()
    conn = db[0]
    cur = db[1]
    qry_str1 = 'select * from {table1} where {field1} = %s;'
    qry1 = sql.SQL(qry_str1).format(table1 = sql.Identifier('dev_all_parts05'),
                                    field1 = sql.Identifier('id_num')
                                    )
    values1 = (id_num, )
    res = qry_execute(conn, qry1, values1, True)
    # Start parsing html
    lfile = init_write_file(log_file)
    with open(lfile, 'w', encoding = 'utf8') as lf:
        # Start looping through values
        for i in res:
            idnum = i[0]
            html = i[9]
            soup = bsp(html, 'html.parser')
            for j in soup.find_all('b'):
                if get_text_ind:
                    jprint = j.get_text().strip()
                else:
                    jprint = j
                print('%s: %s' % (idnum, jprint), file = lf)
    db_close(conn, cur)
    end_function(start_time)
    
extract_bheaders(506, 'log/extract_bheaders.txt', True)
    
    


