from cs50 import get_string

# Prompt the user for some text
text = get_string("Text: ")

# Count number of letters, words and sentences
letters = 0
words = 1
sentences = 0

for i in range(len(text)):
    if text[i].isalpha():
        letters += 1
    elif text[i].isspace():
        words += 1
    elif text[i] == '.' or text[i] == '!' or text[i] == '?':
        sentences += 1

L = letters/words*100
S = sentences/words*100


# Coleman-Liau index

index = 0.0588 * L - 0.296 * S - 15.8


# Print out the result

if index >= 16:
    print("Grade 16+")
elif index < 1:
    print("Before Grade 1")
else:
    print(f"Grade {round(index)}")
