
from functions import *

# tag_counts()

db = db_init()
conn = db[0]
cur = db[1]

# tname = 'dev_reg_links01'
# qry_str = 'drop table if exists {table}, {table1};'
# qry = sql.SQL(qry_str).format(table = sql.Identifier(tname),
#                               table1 = sql.Identifier('ugh'))
# res = qry_execute(conn, qry, '', False)
# print(res)

# qry_str = 'select * from {table};'
# tname = 'ugh'
# qry = sql.SQL(qry_str).format(table = sql.Identifier(tname))
# print(qry.as_string(conn))






tname = 'reg_links01'
value_string = '({values} varchar, {values} varchar, {values} numeric)'
value_string2 = '(%s varchar, %s varchar, %s numeric)'
values = ('reg', 'link', 'order_num')
values2 = ('reg varchar', 'link varchar', 'order_num numeric')
drop_create_tables4(conn, tname, value_string2, values)
# print(cur.mogrify('select * from %s', (tname, )))






# values2 = ("reg varchar", "link varchar", "order_num numeric")
# drop_create_tables2(conn, tname, values2)
# drop_create_tables4(conn, tname, value_string, values)

# tup1 = ['ugh', 'derp', 'three']
# for i in tup1:
#     print(i)

# hlink = 'https://www.acquisition.gov/chapter_99'
# html = rq.get(hlink).text
# soup = bsp(html, 'html.parser')
# # results1 = soup.find('div', id = 'parts-wrapper')
# # results2 = results1.find_all('div', class_ = 'clearfix')
# res = soup.tbody.find_all('td', class_ = re.compile('.*part-number'))
# # res = results2.a['href']
# for i in res:
#     print(i.find_all('a'))
    
    # for j in i.find_all('a'):
    #     print(j)
        # hpart = i.get_text()
        # print(hpart)
        # print(i.a['href'])

    
    
    # results3 = i.find_all('a')
    # for j in results3:
    #     print(j['href'])
    # if i['href'].split('/')[1] == 'content':
    #     print(i.get_text())
    #     if len(i['href'].split('/')) > 2:
    #         print(i['href'])
























