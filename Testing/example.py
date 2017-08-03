# '''
# Identifiers
# \d any number
# \D anything but a number
# \s space
# \S anything but a number
# \w character
# \W anything but a character
# . any character, except for a newline
# \b the whitespace around words
# \. a period
#
# Modifiers
# {1,3} we'are expecting 1-3
# + match 1 or more
# ? match 0 or 1
# * match 0 or more
# $ match the end of a string
# ^ matching the beginning of a string
# [] range or variance
# {x} expecting "x" amount
#
# White Space Characters
# \n new line
# \s space
# \t tab
# \e escape
# \f from feed
# \r return
# '''

import re
exampleString = '''Jessica is 15 is old, and Daniel is 27 years old. Edward is 97, and his
grandfather Oscar is 102.'''

ages = re.findall(r'\d{1,3}', exampleString)
names = re.findall(r'[A-Z][a-z]*', exampleString)
words = re.findall(r'[A-Z][^A-Z]*', "OffDry")

print(ages)
print(names)
print (words)
