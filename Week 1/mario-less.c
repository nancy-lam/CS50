#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    // Prompt user for positive integer
    do
    {
        n = get_int("Height: ");
    }

    while (n < 1);

    // Print a half pyramid bricks
    for (int i = 0; i < n; i++)
    {
        for (int k = n - i; k >= 2; k--)
        {
            printf(" ");
        }

        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
