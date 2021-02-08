
import json
# lst = ['a', 'b', 1, 'c', 1, 2, 'i', 'ii', 'iv', 'xi', 3, 'A']
# last_str = ''
# for i in lst:
#     while True:
#         res_list = [i, lst.i[i + 1]]
#         cval = res_list[0]
#         nval = res_list[1]
#         i.isalpha()
#         try:
#             if cval == 'i' and nval == 'h':
#                 print(i + ': not a roman numeral')
#             elif i != 'i'
#             else:
#                 print(i + ': definitely a roman numeral')
#             last_str = i
#             break
#         # Only runs for integers
#         except:
#             print(str(i) + ': integer')
#             break



# lnum: list number
# lst: list
# citation: citation is pulled from the list number in the 
# isalph: checks if it is a letter
# is_rnumeral
# prev_value: previous value in the list
# prev_isalpha: if previous value is a letter
# prev_letter: all lowercase a-h, j-u, w, y-z
# next_value: next value in the list
# next_value_len: length of next value
# next_isalpha: checks if next value is the list
class PCitation:
    def __init__(self, list_object):
        self.lst = list_object
    # Get attributes
    def get_attributes(self, list_num):
        lnum = list_num
        citation = self.lst[lnum]        
        # Check if it is alpha
        while True:
            try:
                citation.isalpha()
                isalph = True
                break
            except:
                isalph = False
                break
        # Previous values
        if lnum > 0:
            pvalue = self.lst[lnum - 1]
            while True:
                try:
                    pvalue.isalpha()
                    pisalpha = True
                    break
                except:
                    pisalpha = False
                    break
        else:
            pvalue = 'N/A'
            pisalpha = 'N/A'
            pletter = 'N/A'
        # Next values
        if lnum != len(self.lst):
            nvalue = self.lst[lnum]
            nvalue_len = len(str(nvalue))
        else:
            nvalue = 'N/A'
            nvalue_len = 'N/A'
        # Check if next value is a letter
        while True:
            try:
                nvalue.isalpha()
                nisalpha = True
                break
            except:
                nisalpha = False
                break
        # Check when previous value is letter
        prev_lalpha = False
        if lnum != 0:
            for x, i in reversed(list(enumerate(self.lst[:(lnum - 1)]))):
                # First iteration of the loop assumes no alpha character
                if x == 0:
                    prev_lalpha = False
                # Break the loop here so that it stop repeating
                elif prev_lalpha == True:
                    break
                while True:
                    # pletter will only be saved if it runs true
                    try:
                        i.isalpha()  
                        prev_lalpha = True
                        pletter = i
                        break
                    except:
                        prev_lalpha = False
                        pletter = 'N/A'
                        break
    #            print(str(x) + ' - ' + str(i) + ' - ' + str(pletter) + ' - ' + str(prev_lalpha))
                if prev_lalpha == True:
                    break
                else:
                    continue
        else:
            prev_lalpha = 'N/A'
            
        
   
        
        
        
        
        
        
        # if lnum != 0:
        #     # Runs in reverse to find any letter paragraphs immediately before
        #     for x, i in reversed(list(enumerate(self.lst[:(lnum - 1)]))):
        #         pletter = ''
        #         # First iteration of the loop assumes no alpha character
        #         if x == 0:
        #             prev_lalpha = False
        #         # Break the loop here so that it stop repeating
        #         elif prev_lalpha == True:
        #             break
        #         while True:
        #             # pletter will only be saved if it runs true
        #             try:
        #                 i.isalpha()
        #                 prev_lalpha = True
        #                 pletter = i
        #                 break
        #             except:
        #                 prev_lalpha = False
        #                 break
        #         continue
        # Check to see if its a roman numeral
        # This probably needs more work
        # Here is current definitino of a roman numeral:
        # - MUST: prev value is number
        # - next value is capital A
        # - next value is ii
        # - prev actual letter was <= h
        # - NOT: next value is 1
        # - next value is i
        # - two or more character with i in it
        if isalph == True and \
           pisalpha == False and \
           (citation in 'ivx' or len(citation) >= 1) and \
           nvalue != 1:
            isrnumeral = True
        else:
            isrnumeral = False
    # Save data in a dictionary, and return it
        d = {
            'citation': citation,
            'is_alpha': isalph,
            'is_rnumeral': isrnumeral,
            'prev_val_alpha': pisalpha
            }
        print(d)
        return d



# Paragraphs
# (a)
# (1)
# (i)
# (A)
# (1)
# (I)

# T: a, 1, i, ii
# T: a, 1, i, 2
# T: a, b, c, d, e, f, g, h, 1, i, 2, 3, 4, i
# F: a, b, c, d, e, f, g, h, 1, i, 1, i
# T: a, b, c, d, e, f, g, 1, i, 2, 3, h, 1, i, i
# T: a, b, c, d, e, f, g, 1, i, 2, 1
# F: a, b, c, d, e, f, g, 1, i, 1, i

# loop through all values to find whether each item isalpha
# save whether it is as a dictionary
# loop through list of dictionaries:
# use fun to make a class for each iteration
# add function to strip out paragraph
# each iteration will have attributes:
#     - isalpha
#     - is_rnumeral
#     - prev_value
#     - prev_isalpha
#     - prev_letter: all lowercase a-h, j-u, w, y-z
#     - next_value
#     - next_isalpha

# All roman numerals have a combination of these:
# - MUST: prev value is number
# - next value is capital A
# - next value is ii
# - prev actual letter was <= h
# - NOT: next value is 1
# - next value is i
# - two or more character with i in it





# print(chr(ord(char) - 25))


#charac = input()

# if charac == "Z": # If Z encountered change to A
#    print(chr(ord(charac)-25))

# else:
#    change = ord(charac) + 1
#    print(chr(change))

