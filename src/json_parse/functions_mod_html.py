
import json


# Paragraphs
# (a)
# (1)
# (i)
# (A)
# (1)
# (I)




# Create attributes for the paragraphs listed
class PCitation:
    # lst: list of all paragraphs
    #   Returns list
    def __init__(self, list_object):
        self.lst = list_object
    
    # Get attributes
    # lnum: list number, starts at 0
    #   Returns int
    # citation: citation is pulled from the list number in the 
    #   Returns string or int
    def get_attributes(self, list_number):
        lnum = list_number
        citation = self.lst[lnum]  
        
        # Check if it is an alpha character
        # is_alpha: checks if it is a letter
        #   Returns boolean or 'N/A'
        # is_caps: checks if the letter is a capital letter
        #   Returns boolean or 'N/A'
        while True:
            try:
                citation.isalpha()
                is_alpha = True
                break
            except:
                is_alpha = False
                break
        if is_alpha and citation.isupper():
            is_caps = True
        else:
            is_caps = False
            
        # Previous value attributes
        # prev_value: previous value in the list
        #   Returns string or int
        # prev_is_alpha: if previous value is a letter
        #   Returns boolean or 'N/A'
        # prev_letter: all lowercase a-h, j-u, w, y-z
        #   Returns string
        if lnum > 0:
            prev_value = self.lst[lnum - 1]
            while True:
                try:
                    prev_value.isalpha()
                    prev_is_alpha = True
                    break
                except:
                    prev_is_alpha = False
                    break
        else:
            prev_value = 'N/A'
            prev_is_alpha = 'N/A'
            
        # Next value attributes
        # next_value: next value in the list
        #   Returns string or int
        # next_value_len: length of next value
        #   Returns int
        if lnum != len(self.lst):
            next_value = self.lst[lnum]
            next_value_len = len(str(next_value))
        else:
            next_value = 'N/A'
            next_value_len = 'N/A'
            
        # Check if next value is a letter
        # next_is_alpha: checks if next value is the list
        #   Returns Boolean or 'N/A'
        while True:
            try:
                next_value.isalpha()
                next_is_alpha = True
                break
            except:
                next_is_alpha = False
                break
            
        # Find the previous letter and if it's an alpha character
        # prev_lett_alpha: whatever the last letter is, checks if it's an alpha
        #   Returns Boolean or 'N/A'
        prev_lett_alpha = False
        if lnum != 0:
            for x, i in reversed(list(enumerate(self.lst[:(lnum)]))):
                # First iteration of the loop assumes no alpha character
                while True:
                    try:
                        i.isalpha()  
                        prev_lett_alpha = True
                        prev_letter = i
                        break
                    except:
                        break
                if prev_lett_alpha == True: break
        else:
            prev_lett_alpha = 'N/A'
            prev_letter = 'N/A'
            
        # Find the next leter and if it's an alpha character
        # next_lett_alpha: whatever the next letter is, checks if it's an alpha
        #   Returns Boolean or 'N/A'
        next_lett_alpha = False
        if (lnum + 1) != len(self.lst):
            for x, i in enumerate(self.lst[(lnum + 1):len(self.lst)]):
                # Last iteration of the loop assumes no alpha character
                while True:
                    try:
                        i.isalpha()
                        next_lett_alpha = True
                        next_letter = i
                        break
                    except:
                        break
                if next_lett_alpha == True: break
        else:
            next_lett_alpha = 'N/A'
            next_letter = 'N/A'
        
        # Finally, check if the value is roman numeral, or just a letter
        # All roman numerals share the following characteristics:
        #   - prev value may be number
        #   - next value may be capital A
        #   - next value may be ii
        #   - prev actual letter could have been <= h
        #   - NOT: next value is 1
        #   - next value may be i
        #   - is alpha and has two or more characters
        # is_rom_numeral = checks if previous letter was a roman numeral
        #   Returns Boolean or 'N/A'
        if is_alpha == True and \
           (citation[0] in 'ivx' and len(citation) >= 1) and \
           next_value != 1:
            # Check previous letter if it is the previous letter
            is_rom_numeral = True
        else:
            is_rom_numeral = False

        # Save data in a dictionary, and return it
        d = {
            'citation': citation,
            'is_alpha': is_alpha,
            'is_rnumeral': is_rom_numeral,
            'prev_val_alpha': prev_is_alpha,
            'prev_letter': prev_letter,
            'next_letter': next_letter
            }
        #print(json.dumps(d, indent = 2))
        return d
            

           
    
    
    
    #prev_is_alpha == False and \
# print(chr(ord(char) - 25))


#charac = input()

# if charac == "Z": # If Z encountered change to A
#    print(chr(ord(charac)-25))

# else:
#    change = ord(charac) + 1
#    print(chr(change))



