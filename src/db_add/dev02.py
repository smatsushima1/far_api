
from functions import *



def dev_read_html():
    html = open('c:/users/smats/dfars.html', 'r', encoding = 'utf8').read()
    soup = bsp(html, 'html.parser')
    print(soup.prettify())
    #html_final = url = str(str(soup).encode('utf-8'))
    fname = init_write_file('html/dev_contents4.html')
    with open(fname, 'w', encoding = 'utf8') as wf:
        wf.write(str(soup))
        wf.close()
    

# Updates table to include html portion of the web link provided
# Total run time: 1595.066 seconds
def add_html2():
    start_time = start_function('add_html')
    # Connect to database
    conn = db_connect()
    cur = conn.cursor()
    tname = 'dev_all_parts2'
    qry = 'select * from %s where %s = %s;'
    cur.execute(qry, (AsIs(tname), 
                      AsIs('id_num'),
                      AsIs('96')
                      ))
    res = cur.fetchall()
    # Start adding html to the DB
    for i in res:
        url = i[8]
        idnum = i[12]
        print('%s: Working' % (str(idnum)))
        # id_num 96 and 144 have ASCII characters in their title
        # This converts their characters to UTF-8
        try:
            html = ul.request.urlopen(url).read()
        except:
            print('nope')
            url = str(str(url).encode('utf-8'))
            url_final = url[2:len(url) - 1]
            update_one(cur, tname, 'hlink', url_final, idnum)
            print('%s: Updated' % (str(idnum)))
            html = ul.request.urlopen(url_final).read()
        soup = bsp(html, 'html.parser')
        print('soup')
        # All the main content is listed under the class below
        hres = soup.find('div', class_ = 'field-items')
        # For all others, content is listed under 'field-items'
        update_one2(cur, tname, 'htext', str('hres'), idnum)
    # Finish
    conn.commit()
    cur.close()
    end_function(start_time)
    

# Updates only one field in a table
# Maybe later update to include logic to update multiple fields
def update_one2(cur, table_name, field_name, value, id_num):
    qry = 'update {table} set {field} = %s where id_num = %s'
    cur.execute(sql.SQL(qry).format(table = sql.Identifier(table_name),
                                    field = sql.Identifier(field_name)),
                (value, id_num)
                )


# add_html2()
dev_read_html()
















