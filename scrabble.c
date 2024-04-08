#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter

int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int get_score(string player);

int main(void)
{
    string player1, player2;
    int score1, score2;

    // Get string from players

    player1 = get_string("Player 1: ");
    player2 = get_string("Player 2: ");

    // Calculate the scores based on the string given by two players

    score1 = get_score(player1);
    score2 = get_score(player2);

    // Print out who is the winner

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }

    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }

    else
    {
        printf("Tie!\n");
    }
}

int get_score(string player)
{
    int score = 0;

    for (int i = 0; i < strlen(player); i++)
    {
        if isupper (player[i])
        {
            score = score + points[player[i] - 65];
        }

        if islower (player[i])
        {
            score = score + points[player[i] - 97];
        }
    }
    return score;
}
