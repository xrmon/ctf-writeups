import binascii

input = "8fd2c6939bc7d8f49fd998f4fb9b9e9e9a93c798f4df9b9b8a8a8a"

# Decode input from hex string to bytes
bytes = binascii.unhexlify(input)

out = ""
for byte in bytes:
    # xor with key byte
    dec = byte ^ 0xAB
    # Convert to character
    out += chr(dec)

print(out)
