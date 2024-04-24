from cs50 import get_int

height = 0
while height < 1 or height > 8:
    height = get_int("Height: ")

# Loop through rows and columns

for i in range(height):
    for space in range(height - i - 1):
        print(" ", end="")
    for j in range(i+1):
        print("#", end="")
    print("  ", end="")
    for k in range(i+1):
        print("#", end="")
    print()
