
from functions import *
from dev01 import *


# Identify the different types of of headers

def header_types(reg, text):
    # Turn None type to an empty string
    if text is None:
        text = ''
    # Isolate the first part of the citation
    text2 = text.strip().split(' ')[0]
    # Return for DFARS
    if text2.startswith('assignments') or \
       text2.startswith('spare') or \
       text2[1] == '-':
        return 2
    # Return an exit code
    elif text == '':
        return 1
    # Majority of the other citations
    elif text2.startswith('part') or \
         text2.startswith('subpart') or \
         text2.count('.') > 0:
        return
    # Process alternatives
    else:
        return 3


def dev_header(id_num):
    db = db_init()
    conn = db[0]
    cur = db[1]
    tname1 = 'dev_all_parts05'
    qry_str1 = 'select * from {table1} where {field1} = %s;'
    # Run for the real results
    qry1 = sql.SQL(qry_str1).format(table1 = sql.Identifier(tname1),
                                    field1 = sql.Identifier('id_num')
                                    )
    values1 = (id_num, )
    res = qry_execute(conn, qry1, values1, True)  
    # Start looping through values
    for i in res:
        idnum = i[0]
        reg = i[1]
        part = i[2] 
        url = i[8]
        html = i[9]
        soup = bsp(html, 'html.parser')
        find_res = soup.find('h2', id = 'ariaid-title39')
        print(find_res.find_all_next('p'))
            

run = 2
idnum = 978
if run == 1:
    mod_protocol0(idnum)
elif run == 2:
    html_pull(idnum, 'html/html_pull01.html')
elif run == 3:
    extract_headers(0, 'log/log02.txt', True)
elif run == 4:
    extract_headers_test('log/log02.txt', 'log/log03.txt')
elif run == 5:
    dev_header(idnum)


# str1 = '1474.201Reserved'
# print(reformat_headers('dfarspgi', str1))
    
# str2 = ''
# print(str2.strip())






# str1 = 'assignments_part_1 -ugh herp'

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


