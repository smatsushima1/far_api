import json

doc = open('C:/Users/smats/git/far_api/src/app/js/json/parts.json', 'r', encoding = 'utf8').read()
d1 = json.loads(doc)
doc2 = open('C:/Users/smats/git/far_api/src/app/js/json/parts2.json', 'w', encoding = 'utf8')
json.dump(d1, doc2)









