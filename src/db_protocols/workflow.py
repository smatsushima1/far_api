
from functions import *


# Protocol types:
# Protocol 0: everything has articles and headers, with no bold or lists (366)
# Protocol 1: no headers, bold and lists for paragraphs (526)
# Protocol 2: vaar specific, strong for everything and h2 = h1 (47)
# Protocol 3: nfs specific, only p tags and literally nothing else (49)
# Protocol 4: contains headers, but no articles (294)


run = 9
idnum = 503
reg = ''
if run == 1:
    add_prot0(idnum, reg, 'log/add_prot0.txt')
elif run == 2:
    html_pull(idnum, 'html/html_pull01.html')
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
elif run == 8:
    dev_next()
elif run == 9:
    add_prot1(idnum, reg, 'log/add_prot1.txt')



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


