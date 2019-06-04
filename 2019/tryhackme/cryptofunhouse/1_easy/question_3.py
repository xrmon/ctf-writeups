import base64

# Decode as base64
input = "YmFzZTY0"
output = base64.b64decode(input)
# Convert to string and remove b' and '
output = str(output)[2:-1]
print(output)
