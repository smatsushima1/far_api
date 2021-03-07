
from functions import *

str1 = 'abs'
if str1.startswith('a') or str1.startswith('abc'):
    print('yep')


rnum_list = ['a', 'b', 1, 2, 'i', 'ii', 'iii', 'c', 1, 2, 'i', 'ii', 'iii', 3, 'd', \
            'e', 1, 'i', 'ii', 'iii', 2, 'f', 'g', 'h', 1, 'i', 2, 3, 'i', 4, 'j', 'k', 'l']


cnum = 4
# Required: current iteration, list, next value, next value is alpha
def case_i_rnum(cnum, rnum_list, next_value, next_value_is_alpha):
    new_list = []
    for x, i in reversed(list(enumerate(rnum_list[:(cnum)]))):
        if str(i).isupper(): continue
        new_list.append(i)
        print(i)
        if str(i)[0] in 'ivx':
            print(str(x) + ' - ' + str(i))
            print(new_list)
            # ...'h', 1, 'i', 'i'...
            if len(new_list) == 2:
                # return True
                return 1
            # ...'h', 1, 'i', 2, 3, 'i', 1...
            elif next_value_is_alpha == False and next_value == 1:
                # return False
                return 2
            # ...'h', 1, 'i', 2, 3, 'i', 4...
            elif next_value_is_alpha == False and next_value != 1:
                # return True
                return 3
            # ...'h', 1, 'i', 2, 3, 'i', 'ii'...
            elif next_value_is_alpha and next_value[0] in 'ivx':
                # return True
                return 4
            # ...'h', 1, 'i', 2, 3, 'i', 'j'...
            elif next_value_is_alpha and next_value[0] not in 'ivx':
                # return False
                return 5
            break
        elif str(i).isalpha():
            print(new_list)
            # ...'g', 1, 'h', 'i'...
            if len(new_list) == 2:
                # return True
                return 6
            # ...'g', 1, 2, 3, 'i'...
            if new_list.count(1) > 0:
                # return True
                return 7
            break

for x, i in enumerate(rnum_list):
    if x != len(rnum_list):
        print(str(i))
        print(case_i_rnum(x, 
                          rnum_list, 
                          rnum_list[x + 1], 
                          str(rnum_list[x + 1]).isalpha()))

# print(case_i_rnum(cnum,
#                   rnum_list, 
#                   rnum_list[cnum + 1], 
#                   str(rnum_list[cnum + 1]).isalpha()))



def return_d(citation, next_letter):
    d = {
        'citation': citation,
        'next_letter': next_letter
        # 'is_rnumeral': is_rom_numeral,
        # 'prev_val_alpha': prev_is_alpha
        }
    print(d)
    return d




from functions import paragraph_attributes
num1 = ['a', 'b', '1', '2', 'i', 'ii', 'iii', 'c', '1', '2', 'i', 'ii', 'iii', \
        '3', 'd', 'e', '1', 'i', 'ii', 'iii', '2', 'f', 'g', 'h', '1', 'i', \
        '2', 'i', 'i', 'j', 'k', 'l'
       ]
# FAR 52.209-5
num2 = ['a', 'i', 'A', 'B', 'C', 'D', '1', 'i', 'ii', '2', 'i', 'ii', 'iii', \
        'iv', 'ii', '2', 'b', 'c', 'd', 'e'
       ]

cdev = paragraph_attributes(num2)
final_list = []
for x, i in enumerate(num2):
    final_list.append(cdev.get_attributes(x))
    # d[i] = cdev.get_attributes(x)
# d_final = json.dumps(d, indent = 2)
# print(d_final)

for i in final_list:
    idict = json.loads(i)
    print('paragraph: ' + idict['para'])















