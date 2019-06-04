import base64

# Decode as base64
input = "dXNlcjEyMzpzdHIwbmdQNCQkV29yZA=="
creds = base64.b64decode(input)
# Convert to string and remove b' and '
creds = str(creds)[2:-1]
# Split around the ':' and print the second item
password = creds.split(':')[1]
print(password)
