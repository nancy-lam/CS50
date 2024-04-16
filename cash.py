from cs50 import get_float

change = 0

while True:
    change = round(100*(get_float("Change: ")))
    if change > 0:
        break

quarter = int(change/25)
dime = int((change % 25)/10)
nickle = int(((change % 25) % 10)/5)
penny = int(((change % 25) % 10) % 5)

count = quarter + dime + nickle + penny


# Print out the number of change
print(count)
