import string

# Get the alphabet from the string module
alpha = string.ascii_uppercase

input = "PELCGBVFSHA"

output = ""
for letter in input:
    # Get the index of the letter in the alphabet
    index = alpha.index(letter)
    # Add 13, modulo 26 and get new letter
    new = alpha[(index + 13) % 26]
    output += new

print(output)
