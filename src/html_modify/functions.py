
import json


# Calling it:
# cdev = paragraph_attributes(num2)
# final_list = []
# for x, i in enumerate(num2):
#     final_list.append(cdev.get_attributes(x))
# for i in final_list:
#     idict = json.loads(i)
#     print('paragraph: ' + idict['para'])

# Create attributes for the paragraph citations listed
# Attributes:
# lst: list of all paragraphs; returns list
# lnum: list number, starts at 0; returns integer
# paragraph: paragraph is pulled from the list number; returns string
# is_alpha: paragraph is a letter; returns boolean
# is_caps: paragraph is a capital letter; returns boolean
# prev_value: previous value in the list; returns string
# prev_is_alpha: previous value is a letter; returns boolean
# prev_letter: previous letter, skips over numbers; returns string
# prev_letter_caps: previous letter is in caps; returns boolean
# next_value: next value in the list; returns string
# next_is_alpha: next value is a letter; returns boolean
# next_letter: next letter, excludes integers; returns string
# next_letter_caps: next letter is in caps; returns boolean
# is_rom_numeral =  paragraph is a roman numeral; returns boolean
# is_num_last = paragraph is number after capital paragraphs; returns boolean
# is_rom_num_last = paragraph is roman numeral after last numbers; returns boolean
class paragraph_attributes:
    def __init__(self, list_object):
        self.lst = list_object
        
    # Define all the attributes listed above
    def get_attributes(self, list_number):
        lnum = list_number
        paragraph = self.lst[lnum]
        is_alpha = paragraph.isalpha()
        is_caps = paragraph.isupper()
        
        # Previous value attributes
        if lnum != 0:
            prev_value = self.lst[lnum - 1]
            prev_is_alpha = prev_value.isalpha()
        else:
            prev_value = 'N/A'
            prev_is_alpha = False

        # Next value attributes
        if (lnum + 1) != len(self.lst):
            next_value = self.lst[lnum + 1]
            next_is_alpha = next_value.isalpha()
        else:
            next_value = 'N/A'
            next_is_alpha = False
        
        # Check whether is a value or roman numeral
        is_rom_numeral = is_rnum(lnum,
                                 self.lst,
                                 paragraph,
                                 is_alpha,
                                 next_value,
                                 next_is_alpha
                                 )

        # Finally, find the indentation level of the paragraph
        # Currently, can't find any way to detect if the number or roman
        #   numeral citation is the first or second tier
        # As such, it will remain as false for now; taking too long to solve...
        is_number2 = False
        is_rom_numeral2 = False
        indentation = find_indentation(paragraph,
                                       is_alpha,
                                       is_rom_numeral,
                                       is_caps,
                                       is_number2,
                                       is_rom_numeral2
                                       )

        # Save data in a dictionary, and return it
        d = {'iter': lnum,
             'para': paragraph,
             'ind': indentation,
             'pv': prev_value,
             'pv_al': prev_is_alpha,
             'nv': next_value,
             'nv_al': next_is_alpha
             }
        return json.dumps(d, indent = 2)


# Returns whether the paragraph is a roman numeral
# All roman numerals share the following characteristics:
#   - prev value may be number
#   - next value may be capital A
#   - next value may be ii
#   - prev actual letter could have been <= h
#   - NOT: next value is 1
#   - next value may be i
#   - is alpha and has two or more characters
def is_rnum(para_iteration,
            para_list,
            para_val,
            para_is_alpha,
            next_val,
            next_val_is_alpha
            ):
    if para_iteration == 0:
        return False
    elif para_val == 'i':
        new_list = []
        for x, i in reversed(list(enumerate(para_list[:(para_iteration)]))):
            # Skip over upper-case paragraphs
            if str(i).isupper():
                continue
            new_list.append(i)
            # Only do testing if the string is a letter
            if str(i).isalpha():
                # ...'g', 1, 2, 3, 'i', 1...
                if next_val == 1:
                    return False
                # ...'g', 1, 2, 3, 'i', 4...
                elif next_val_is_alpha == False and next_val != 1:
                    return True
                # ...'g', 1, 2, 3, 'i', 'ii'...
                elif next_val_is_alpha and next_val[0] in 'ivx':
                    return True
                # Tests for 'i' to 'i' lists
                if str(i)[0] in 'ivx':
                    # ...'h', 1, 'i', 'i'...
                    if len(new_list) == 1:
                        return False
                    # ...'h', 1, 'i', 2, 3, 'i', 'j'...
                    elif next_val_is_alpha and next_val[0] not in 'ivx':
                        return False
                # Tests for non 'i' to 'i' lists
                else:
                    # ...'g', 1, 'h', 'i'...
                    if len(new_list) == 1:
                        return True
                    # ...'g', 1, 2, 3, 'i', 'h'...
                    elif next_val_is_alpha and next_val[0] not in 'ivx':
                        return True
                break
    elif para_is_alpha and para_val[0] in 'ivx' and next_val != 1:
        return True
    else:
        return False


# Determine if this is a number after the capital letters
# IN PROCESS: currently just returning False
def is_number2(para_iteration,
               para_list,
               para_val,
               para_is_alpha
               ):
    if para_iteration == 0 or para_val.isalpha():
        return False
    list_back = []
    for x, i in reversed(list(enumerate(para_list[:(para_iteration)]))):
        list_back.append(i)
        # Only do testing if the string is a letter
        if str(i).isalpha() and str(i).isupper():
            list_forw = []
            for y, j in enumerate(para_list[para_iteration:]):
                list_forw.append(j)
                if str(j).isalpha() and str(j).isupper() != True:
                    if str(j) == 'i':
                        return False
    
    
    # FAR 52.209-5
    # 1  3  4  4  4  4  5  6  6   5  6  6   6     6   3  2  1  1  1  1
    # a, i, A, B, C, D, 1, i, ii, 2, 1, ii, iii, iv, ii, 2, b, c, d, e
    
    #                                         \/ no             \/ yes
    # a, b, c, 1, 2, 3, i, ii, A, B, 1, 2, 3, 4, i, C, 1, i, D, 4, 5
    #                                         \/ no             \/ yes
    # a, b, c, 1, 2, 3, i, ii, A, B, 1, 2, 3, 4, i, C, 1, i, D, 4, 5
    #                                         \/ yes               \/ no
    # a, b, c, 1, 2, 3, i, ii, A, B, 1, 2, 3, 4, iii, A, 1, iv, A, 4, 5
    #                                         \/ yes               \/ no
    # a, b, c, 1, 2, 3, i, ii, A, B, 1, 2, 3, 4, C, 1, iv, A, 4, 5    
    #                                         \/ yes
    # a, b, c, 1, 2, 3, i, ii, A, B, 1, 2, 3, 4, d, 1, i, A, 1, 2
    #                                         \/ no
    # a, b, c, 1, 2, 3, i, ii, A, B, 1, 2, 3, 4, d, 1, i, A, 1, 2
    

# Determine if this is the second set of roman numerals
# IN PROCESS: currently just returning False
def is_rnum2(para_iteration,
             para_list,
             para_val
             ):
    pass


# Returns the indentation level
# Paragraphs will be listed in the following format:
# (a)
# (1)
# (i)
# (A)
# (1)
# (i)
def find_indentation(para_val,
                     para_is_alpha,     
                     para_is_rnum,
                     para_is_caps,
                     para_is_num2,
                     para_is_rnum2
                     ):
    if para_is_alpha and para_is_caps != True and para_is_rnum != True:
        return 1
    elif para_is_alpha != True and para_is_num2 != True:
        return 2
    elif para_is_rnum:
        return 3
    elif para_is_caps:
        return 4
    elif para_is_num2:
        return 5
    elif para_is_rnum2:
        return 6
    
    
    #prev_is_alpha == False and \
# print(chr(ord(char) - 25))


#charac = input()

# if charac == "Z": # If Z encountered change to A
#    print(chr(ord(charac)-25))

# else:
#    change = ord(charac) + 1
#    print(chr(change))

# Old copy just in case
# class PCitation:
#     def __init__(self, list_object):
#         self.lst = list_object
        
#     # Define all the attributes listed above
#     def get_attributes(self, list_number):
#         lnum = list_number
#         citation = str(self.lst[lnum])
#         is_alpha = citation.isalpha()
#         is_caps = citation.isupper()
        
#         # Previous value attributes
#         if lnum != 0:
#             prev_value = str(self.lst[lnum - 1])
#             prev_is_alpha = prev_value.isalpha()
#             prev_letter = 'N/A'
#             prev_letter_caps = False
#             for x, i in reversed(list(enumerate(self.lst[:(lnum)]))):
#                 if str(i).isalpha():
#                     prev_letter = str(i)
#                     prev_letter_caps = prev_letter.isupper()
#                     break
#         else:
#             prev_value = 'N/A'
#             prev_is_alpha = False
#             prev_letter = 'N/A'
#             prev_letter_caps = False

#         # Next value attributes
#         if (lnum + 1) != len(self.lst):
#             next_value = str(self.lst[lnum + 1])
#             next_is_alpha = next_value.isalpha()
#             next_letter = 'N/A'
#             next_letter_caps = False
#             for x, i in enumerate(self.lst[(lnum + 1):len(self.lst)]):
#                 if str(i).isalpha():
#                     next_letter = str(i)
#                     next_letter_caps = next_letter.isupper()
#                     break
#         else:
#             next_value = 'N/A'
#             next_is_alpha = False
#             next_letter = 'N/A'
#             next_letter_caps = False
        
#         # Finally, check if the value is roman numeral, or just a letter
#         # All roman numerals share the following characteristics:
#         #   - prev value may be number
#         #   - next value may be capital A
#         #   - next value may be ii
#         #   - prev actual letter could have been <= h
#         #   - NOT: next value is 1
#         #   - next value may be i
#         #   - is alpha and has two or more characters
#         if is_alpha and \
#            citation[0] in 'ivx' and \
#            next_value != 1:
#             is_rom_numeral = True
#         else:
#             is_rom_numeral = False

#         # Special roman numeral check but only if this is an 'i'
#         if citation == 'i':
#             is_rom_numeral = case_i_rnum(lnum,
#                                          self.lst,
#                                          next_value,
#                                          next_is_alpha)

#         # Save data in a dictionary, and return it
#         d = {
#             'citation': citation,
#             # 'prev_letter': prev_letter,
#             # 'next_letter': next_letter,
#             'is_rnumeral': is_rom_numeral          
#             # 'is_alpha': is_alpha,
#             # 'prev_val_alpha': prev_is_alpha

#             }
#         #print(json.dumps(d, indent = 2))
#         return d

