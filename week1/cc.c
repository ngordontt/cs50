//#include <cs50.h>
#include <stdio.h>
#include <math.h>

void first (int n);
void invalid(void);

// global vaiables
long long int card, divisor;
int res;


int main(void)
{


// variable for length of number
int digits;
long long int digchk, mark, cc;



cc[21] = {-1, 0, 1234, 423456789456122223, 1234567894561, 4234567894561, 344234567894561	, 374234567894561, 5142345678945611, 5242345678945611, 5342345678945611, 5442345678945611, 5542345678945611, 4542345678945611, 378282246310005, 5555555555554444, 5105105105105100, 4111111111111111, 4012888888881881, 4222222222222, 001233};

for(int i = 0; i < 21; i++)
{
card = cc[i];



digits = 0;

//    printf("Number: ");
//    scanf("%lld", &card);

    //logic to check length of number
    digchk = card;
    for(digits = 0; digchk > 0; digits++) digchk/= 10;
    {
       printf("%d\n", digits);
    }

    //check if amount of digits is 13, 15 or 16

    if (digits != 13 && digits != 15 && digits != 16 )
    //if (digits != 13)
    {
        invalid();

    }
    else{

//13 digit logic for visa
        if  (digits == 13 )
        {
            first(1);

                if (res == 4)
                {
                    printf("VISA\n");
                }
                else
                {
                    invalid();
                }

            }

//15 digit logic for Amex
        if  (digits == 15)
        {
            first(2);
             if (res == 34 || res == 37 )
                {
                    printf("AMEX\n");
                }
                else
                {
                    invalid();
                }
        }
//16 digit logic for visa and master card
        if  (digits == 16)
        {
            first(2);

            if (res >= 51 && res >= 55 )
            {
                printf("MASTERCARD\n");
            }

            first(1);

            else if (res == 4)
            {
                printf("VISA\n");
            }
            else
            {
                invalid();
            }
        }
    }
return 0;
}

// FUNCTION FOR INVALID

void invalid(void)
{
    printf("INVALID\n");
}

//Funtion to find x amount of first digits
void first(int n)
{
long long int num = card;
int log10 = (log(num)/log(10))+1;
divisor = pow(10, log10-n);
res = num / divisor;
}
}