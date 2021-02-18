
import psycopg2 as pg2

conn = pg2.connect(dbname = "far_api",
                   user = "postgres",
                   host = "localhost",
                   password = "peer")

# Tables can be concatenated in, but not the arguments
def select_all(table_name):
    cur = conn.cursor()
    qry = 'select * from ' + table_name + ';'
    cur.execute(qry)
    results = cur.fetchall()
    for i in results:
        print(i)
    conn.commit()
    cur.close()

cur = conn.cursor()
tname = 'temp_dd_data'
qry = 'insert into ' + tname + ' values (%s, %s, %s, %s, %s, %s, %s);'
dta = ('far', '1', '1', '8', '5', '3', '2')
cur.execute(qry, dta)

select_all(tname)

conn.commit()
cur.close()
conn.close()





