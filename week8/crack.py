import sys
import itertools
import string
import crypt

#check if the atleast 2 arguments, print usage msg is not and exits
if len (sys.argv) != 2:
    print ("Usage: ./crack hash")
    sys.exit (1)

#assign variable
code = sys.argv[1]

#assign salt by taking 1st 2 chars of string
s = code[:2]

#assign maximum length of word
lenSt = 5

#loop creates length of word check and increments of no result founf
for length in range(1, lenSt, 1):

    #using the builtin iterate function to creat a list of word permutation using the string.ascii_letters
    #for possible values of a work of length size.
    keywords = [''.join(i) for i in itertools.permutations(string.ascii_letters, length)]

    #loop to take each combo has and check aganist code entered, if matached end with 0 return
    for wrd in keywords:
        #crypt.crypt only work in unix enviroment
        if crypt.crypt(wrd, s) == code:
            print (wrd)
            sys.exit(0)