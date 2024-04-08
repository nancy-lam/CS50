#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int cent;

    do
    {
        cent = get_int("Change owed: ");
    }
    while (cent < 1);

    int quarter = cent/25;
    int dime = (cent - quarter * 25)/10;
    int nickle = (cent - quarter * 25 - dime * 10)/5;
    int penny = (cent - quarter * 25 - dime * 10 - nickle * 5);

    // Total change
    int total = quarter + dime + nickle + penny;

    // Print out the number of change
    printf("%i\n", total);

}


