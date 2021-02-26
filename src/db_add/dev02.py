
from functions import *

# tag_counts()


hlink = 'https://www.acquisition.gov/chapter_99'
html = rq.get(hlink).text
soup = bsp(html, 'html.parser')
# results1 = soup.find('div', id = 'parts-wrapper')
# results2 = results1.find_all('div', class_ = 'clearfix')
res = soup.tbody.find_all('td', class_ = re.compile('.*part-number'))
# res = results2.a['href']
for i in res:
    print(i.find_all('a'))
    
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
























