
import json





# Create attributes for the paragraph citations listed
# Paragraphs will be listed in the following format:
# (a)
# (1)
# (i)
# (A)
# (1)
# (I)

# Attributes:
# lst: list of all paragraphs; returns list
# lnum: list number, starts at 0; returns integer
# citation: citation is pulled from the list number; returns string
# is_alpha: checks if it is a letter; returns boolean
# is_caps: checks if the letter is a capital letter; returns boolean
# prev_value: previous value in the list; returns string
# prev_is_alpha: if previous value is a letter; returns boolean
# prev_letter: previous letter, skips over numbers; returns string
# prev_letter_caps: whether previous letter is in caps; returns boolean
# next_value: next value in the list; returns string
# next_is_alpha: checks if next value is the list; returns boolean
# next_letter: next letter, excludes integers; returns string
# next_letter_caps: whether the next letter is in caps; returns boolean
# is_rom_numeral = checks if previous letter was a roman numeral; returns boolean
class PCitation:
    def __init__(self, list_object):
        self.lst = list_object
        
    # Define all the attributes listed above
    def get_attributes(self, list_number):
        lnum = list_number
        citation = str(self.lst[lnum])
        is_alpha = citation.isalpha()
        is_caps = citation.isupper()
        
        # Previous value attributes
        if lnum != 0:
            prev_value = str(self.lst[lnum - 1])
            prev_is_alpha = prev_value.isalpha()
            prev_letter = 'N/A'
            prev_letter_caps = False
            for x, i in reversed(list(enumerate(self.lst[:(lnum)]))):
                if str(i).isalpha():
                    prev_letter = str(i)
                    prev_letter_caps = prev_letter.isupper()
                    break
        else:
            prev_value = 'N/A'
            prev_is_alpha = False
            prev_letter = 'N/A'
            prev_letter_caps = False

        # Next value attributes
        if (lnum + 1) != len(self.lst):
            next_value = str(self.lst[lnum + 1])
            next_is_alpha = next_value.isalpha()
            next_letter = 'N/A'
            next_letter_caps = False
            for x, i in enumerate(self.lst[(lnum + 1):len(self.lst)]):
                if str(i).isalpha():
                    next_letter = str(i)
                    next_letter_caps = next_letter.isupper()
                    break
        else:
            next_value = 'N/A'
            next_is_alpha = False
            next_letter = 'N/A'
            next_letter_caps = False
        
        # Finally, check if the value is roman numeral, or just a letter
        # All roman numerals share the following characteristics:
        #   - prev value may be number
        #   - next value may be capital A
        #   - next value may be ii
        #   - prev actual letter could have been <= h
        #   - NOT: next value is 1
        #   - next value may be i
        #   - is alpha and has two or more characters
        if is_alpha and \
           citation[0] in 'ivx' and \
           next_value != 1:
            is_rom_numeral = True
        else:
            is_rom_numeral = False

        # Special roman numeral check but only if this is an 'i'
        if citation == 'i':
            is_rom_numeral = case_i_rnum(lnum,
                                         self.lst,
                                         next_value,
                                         next_is_alpha)

        # Save data in a dictionary, and return it
        d = {
            'citation': citation,
            # 'prev_letter': prev_letter,
            # 'next_letter': next_letter,
            'is_rnumeral': is_rom_numeral          
            # 'is_alpha': is_alpha,
            # 'prev_val_alpha': prev_is_alpha

            }
        #print(json.dumps(d, indent = 2))
        return d

           
# Only run this if the current iteration is an 'i'
# Required: current iteration, list, next value, next value is alpha
def case_i_rnum(curr_iteration,
                current_list,
                next_value,
                next_value_is_alpha):
    new_list = []
    for x, i in reversed(list(enumerate(current_list[:(curr_iteration)]))):
        # Skip over upper-case citations
        if str(i).isupper(): continue
        new_list.append(i)
        # Only do testing if the string is a letter
        if str(i).isalpha():
            print(new_list)
            # ...'g', 1, 2, 3, 'i', 1...
            if next_value == 1:
                return False
            # ...'g', 1, 2, 3, 'i', 4...
            elif next_value_is_alpha == False and next_value != 1:
                return True
            # ...'g', 1, 2, 3, 'i', 'ii'...
            elif next_value_is_alpha and next_value[0] in 'ivx':
                return True
            # Tests for 'i' to 'i' lists
            if str(i)[0] in 'ivx':
                # ...'h', 1, 'i', 'i'...
                if len(new_list) == 2:
                    return False
                # ...'h', 1, 'i', 2, 3, 'i', 'j'...
                elif next_value_is_alpha and next_value[0] not in 'ivx':
                    return False
                break
            # Tests for non 'i' to 'i' lists
            else:
                # ...'g', 1, 'h', 'i'...
                if len(new_list) == 2:
                    return True
                # ...'g', 1, 2, 3, 'i', 'h'...
                elif next_value_is_alpha and next_value[0] not in 'ivx':
                    return True
                break
    
    
    #prev_is_alpha == False and \
# print(chr(ord(char) - 25))


#charac = input()

# if charac == "Z": # If Z encountered change to A
#    print(chr(ord(charac)-25))

# else:
#    change = ord(charac) + 1
#    print(chr(change))



