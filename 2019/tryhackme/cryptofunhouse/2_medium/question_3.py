import binascii

input = "feedfaf1d7fbedebfdfaed"

# Decode input from hex string to bytes
bytes = binascii.unhexlify(input)

for key in range(0, 0x100):
    out = ""
    for byte in bytes:
        # xor with key byte
        dec = byte ^ key
        # Convert to character
        out += chr(dec)

    print("Key " + hex(key) + ": " + out)

# Key 0x88 produces the plaintext very_secure
