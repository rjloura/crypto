#http://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-63ver1.0.2.pdf
import sys
import math
import re
import string

# For English
ALPHA_SIZE = 26

if len(sys.argv) != 2:
    print "\tUsage: " + sys.argv[0] + " <password>"
    exit(1)

upper = re.compile(r'[A-Z]')
lower = re.compile(r'[a-z]')
num = re.compile(r'[0-9]')
password = sys.argv[1]

search_space = 0
character_space = 0

if upper.search(password):
    print "Uppercase Alpha Detected"
    character_space += ALPHA_SIZE

if lower.search(password):
    print "Lowercase Alpha Detected"
    character_space += ALPHA_SIZE

if num.search(password):
    print "Numbers Detected"
    character_space += 10

if set(string.punctuation).intersection(password):
    print "Special characters detected"
    character_space += len(string.punctuation)


'''
>>> math.log(26, 2)* len("abcdabcd")
37.60351774512874
'''

'''
Search Space = Sum(possible characters) from 1 to length of password.

Example for password with 3 lower case characters:
Search Space = 26*26*26 + 26*26 + 26
'''
for i in range(1, len(password)+1):
    search_space += character_space**i
    
# This seems to be slightly off from the Table A.1 in the link above.
entropy = math.log(character_space, 2) * len(password)

print "\n====Results===="
print "Alphabet Length: {}".format(character_space)
print "Search Space: {}".format(search_space)
print "Entropy: {}".format(entropy)
