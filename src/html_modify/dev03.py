
from functions import *
from dev01 import *





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
        find_res = soup.find('h2', id = 'ugh-derp')
        print(find_res)
        # find_res = soup.find('h2', id = 'ariaid-title39')
        # print(find_res.find_all_next('p'))
            

# 'far',
# 'dfars',
# 'dfarspgi',
# 'diar',
# 'gsam',
# 'epaar',
# 'hsar',
# 'hudar'


# Error at 112, 154, 155, 157, 899, 1063, 1070, 1086, 1109, 1124
run = 1
idnum = ''
reg = ''
if run == 1:
    mod_protocol0(idnum, reg, 'log/log_prot0.txt')
elif run == 2:
    html_pull(idnum, 'html/html_pull01.html')
elif run == 3:
    extract_headers(0, 'log/log02.txt', True)
elif run == 4:
    extract_headers_test('log/log02.txt', 'log/log03.txt')
elif run == 5:
    dev_header(idnum)



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


