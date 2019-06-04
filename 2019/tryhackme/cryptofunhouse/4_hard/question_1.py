import binascii

# Import from freq.py
from freq import frequencies

def InvShiftRows(state):
    new = [-1]*16
    # First row, no shift
    new[0] = state[0]
    new[4] = state[4]
    new[8] = state[8]
    new[12] = state[12]
    # Second row, right shift 1
    new[5] = state[1]
    new[9] = state[5]
    new[13] = state[9]
    new[1] = state[13]
    # Third row, right shift 2
    new[10] = state[2]
    new[14] = state[6]
    new[2] = state[10]
    new[6] = state[14]
    # Fourth row, right shift 3
    new[15] = state[3]
    new[3] = state[7]
    new[7] = state[11]
    new[11] = state[15]
    return new

with open("ciphertexts.txt") as f:
    texts = f.read().split()

# Track the number of times we see every possible byte for each position
counts = []
seen = [0]*256
for i in range(0, 16):
    counts.append(seen.copy())

# Iterate through every ciphertext and count the bytes
for text in texts:
    ciphertext = binascii.unhexlify(text)
    for pos in range(0, 16):
        byte = ciphertext[pos]
        # Update the count for this byte in this position
        counts[pos][byte] += 1

bytes = []
maps = []
for pos in range(0, 16):
    print("==================")
    print("pos", pos)
    print("==================")
    bytes.append({})

    # Build the dictionary bytes mapping frequencies to bytes
    for byte in range(0, 256):
        count = counts[pos][byte]

        if count != 0:
            # If this frequency is already in the list, subtract a small value
            while count in bytes[pos].keys():
                count -= 0.01
            # Add to our dictionary
            bytes[pos][count] = byte

    # Sort the frequencies
    freqs = sorted(bytes[pos].keys(), reverse=True)
    print(freqs, len(freqs))

    # Guess the plaintext for each byte based on the frequencies
    map = {}
    for i in range(0, len(freqs)):
        letter = frequencies[pos][i]
        freq = freqs[i]
        byte = bytes[pos][freq]
        print(hex(byte), "=>", letter)
        map[byte] = letter
    maps.append(map)
    print("length", len(map))
    print(counts[pos])

# Print the decrypted ciphertexts
i = 0
for text in texts:
    state = []
    ciphertext = binascii.unhexlify(text)
    for pos in range(0, 16):
        byte = ciphertext[pos]
        letter = maps[pos][byte]
        state += letter
    # Correct for ShiftRows
    new = InvShiftRows(state)
    out = ''.join(new)
    if i < 20:
        if (i % 4 == 0):
            print("")
            print("0123456789abcdef")
        print(out, state, text)
        #print(in)
        i += 1
    else:
        break

# Attempt to decrypt the target ciphertext
text = "67a2401f0f36c3b680abb775ecedf311"
ciphertext = binascii.unhexlify(text)
state = []
for pos in range(0, 16):
    byte = ciphertext[pos]
    letter = maps[pos][byte]
    state += letter
# Correct for ShiftRows
new = InvShiftRows(state)
out = ''.join(new)
print("")
print("")
print("Target ciphertext:")
print("")
print("0123456789abcdef")
print(out, state, text)
#print(in)
i += 1
