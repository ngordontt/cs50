import sys

#input is saved as a string
x = input("Please enter cred card number: ")
#converts to int
ccNo = int(x)

#ccNo_1 = [-1, 0, 1234, 423456789456122223, 1234567894561, 4234567894561, 344234567894561, 374234567894561, 5142345678945611, 5242345678945611, 5342345678945611, 5442345678945611, 5542345678945611, 4542345678945611, 378282246310005, 5555555555554444, 5105105105105100, 4111111111111111, 4012888888881881, 4222222222222, 1233256]
#ccNo_1 = [5142345678945611]
#ccNo_1 = [378282246310005]
#ccNo = 378282246310005

#function to print invalid
def invalid():
            print("INVALID")

# for ccNo in ccNo_1:
length = len(str(abs(ccNo)))

#test is number is valid by length
if length >= 13 and length <= 16:

    #Find fist or firs 2 digits
    res1 = int(str(ccNo)[:1])
    res2 = int(str(ccNo)[:2])

    #function to check if number is valid
    def valid(number):

        #zero sum variables
        p1sum = p2sum = 0
            
        #this starts at 2nd last digit and steps in 2
        for i in range(length - 2, 0 - 1, -2):
            #gets value of current position
            p1 = int(str(number)[i]) * 2
            
            #sum number if greater than 9
            if p1 > 9:
                p1 = (int(str(p1)[:1]))+(p1 % 10)
            p1sum += p1

        #starting from left differ is number is even
        if length % 2 == 0:
            start = 1
        else:
            start = 0

        for t in range(start, length, 2):
            p2 = int(str(number)[t])
            p2sum += p2

        #adds together both calculations
        tot = p2sum + p1sum

        #checks if last digit of total is a zero
        if tot % 10 == 0:
            return 1
        else:
            return 0

    #If card is 14 digits invalid
    if  length == 14:
        invalid()


    #13 or 16 digit logic for visa
    if  length == 13 or length == 16:

        if (res1 == 4):
            if (valid(number = ccNo) == 1):
                print("VISA")
            else:
                invalid()
        #check if res2 is in the range of number 51-55
        if res2  in list(range(51,56)):
            if (valid(number = ccNo) == 1):
                print("MASTERCARD")
            else:
                invalid()
        else:
            invalid()

    #15 digit logic for visa

    if  length == 15:
        
        if (res2 == 34 or res2 == 37):
            if (valid(number = ccNo) == 1):
                print("Amex")
            else:
                invalid()
        else:
            invalid()
else:
    invalid()