#include <cs50.h>
#include <stdio.h>

int cal_quarter(int cent);
int cal_dime(int cent);
int cal_nickle(int cent);
int cal_penny(int cent);

int main(void)
{
    int cent;
    int quarter;
    int dime;
    int nickle;
    int penny;

    // Ask for the change owed
    do
    {
        cent = get_int("Change owed: ");
    }

    while (cent < 1);

    // Calculate # of quarter
    quarter = cal_quarter(cent);
    cent = cent - quarter * 25;

    // Calculate # of dime
    dime = cal_dime(cent);
    cent = cent - dime * 10;

    // Calculate # of nickle
    nickle = cal_nickle(cent);
    cent = cent - nickle * 5;

    // Calculate # of penny
    penny = cal_penny(cent);
    cent = cent - penny * 1;

    // Calculate total change
    int coin = quarter + dime + nickle + penny;

    printf("%i\n", coin);
}

int cal_quarter(int cent)
{
    int quarter = cent / 25;
    return quarter;
}

int cal_dime(int cent)
{
    int dime = cent / 10;
    return dime;
}

int cal_nickle(int cent)
{
    int nickle = cent / 5;
    return nickle;
}

int cal_penny(int cent)
{
    int penny = cent;
    return penny;
}
