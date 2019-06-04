import binascii

# Decode as hex
input = "7472796861636b6d65"
output = binascii.unhexlify(input)
# Convert to string and remove b' and '
output = str(output)[2:-1]
print(output)
