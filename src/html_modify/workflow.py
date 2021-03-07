
from functions import *
  

def dev_article_text(idnum, log_file):
    # Connect to database
    db = db_init()
    conn = db[0]
    cur = db[1]
    # Pull data
    tname1 = 'dev_all_parts05'
    qry_str1 = 'select * from {table1} where {field1} = %s;'
    qry1 = sql.SQL(qry_str1).format(table1 = sql.Identifier(tname1),
                                    field1 = sql.Identifier('id_num')
                                    )
    values1 = (idnum, )
    res = qry_execute(conn, qry1, values1, True)
    # Start parsing html
    lfile = init_write_file(log_file)
    with open(lfile, 'w', encoding = 'utf8') as lf:
        # Start looping through values
        for i in res:
            idnum = i[0]
            reg = i[1]
            part = i[2] 
            url = i[8]
            html = i[9]
            soup = bsp(html, 'html.parser')
            for j in soup.find_all('article'):
                print('%s\n%s\n%s' % (cb(),
                                      j.attrs,
                                      j.find_all_next('p')
                                      ), file = lf
                      )


run = 1
idnum = ''
reg = ''
if run == 1:
    add_prot0(idnum, reg, 'log/add_prot0.txt')
elif run == 2:
    html_pull(idnum, 'html/html_pull.html')
elif run == 3:
    extract_headers(0, 'log/extract_headers.txt', True)
elif run == 4:
    extract_headers_test('log/extract_headers.txt', 'log/extract_headers_test.txt')
elif run == 5:
    dev_header(idnum)
elif run == 6:
    article_classes('log/article_classes.txt')
elif run == 7:
    dev_article_text(idnum, 'log/dev_article_text.txt')



# str1 = 'PGI 242.322Reserved'
# fcit = re.match('.*[0-9]reserved.*', str1, re.I)
# fcit2 = re.match('.*[a-z]derp.*', str3)
# str2 = str1.replace('—', '-').replace('accounting', 'ugh')
# print(re.sub('.*[a-z]derp.*', ' derp', str3, flags = re.I))
# print(str1.lower().replace('reserved', ' reserved'))
# print(fcit2)

# lst = ['a', 'b', 'c', 'd']
# print(' '.join(lst[1:]))

# str2a = 'ugh derp - maximus'
# str2 = ''
# print(str2.replace('- ', ' - ').replace('  ', ' '))



# str_spl = str1.split(' ')[0]
# print(str_spl[len(str_spl) - 1])



# str1 = '§ 1539.2071 Contract clause.'
# print(str1.lower().replace('§', '').lstrip())
# if str1.startswith('§'):
#     print('yay')

# str2 = '501A'
# print(str2[:3])
# print(str2[1:3])
# print(str2[len(str2) - 1])

# str2 = ''
# if len(str2):
#     print('yes')
# else:
#     print('no')


