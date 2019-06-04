# Relative frequencies of letters for each round

# Initially english, reorder as required
english = [
    # Position 0 swapped a & i, u & c
    [' ', 'e', 't', 'i', 'o', 'a', 'n', 's', 'r', 'h', 'd', 'l', 'c', 'u', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'],
    # Position 1 swapped u & f
    [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'c', 'f', 'm', 'u', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'],
    # Position 2 swapped a & i
    [' ', 'e', 't', 'i', 'o', 'a', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'],
    # Position 3 swapped d & c
    [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'c', 'l', 'u', 'd', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'],
    # Position 4 swapped l & d
    [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l', 'd', 'u', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'],
    # Position 5 swapped a & i, l & c, m & u
    [' ', 'e', 't', 'i', 'o', 'a', 'n', 's', 'r', 'h', 'd', 'c', 'm', 'l', 'u', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'],
    # Position 6
    [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'],
    # Position 7 swapped b & y
    [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'b', 'w', 'g', 'p', 'y', 'v', 'k', 'x', 'q', 'j', 'z'],
    # Position 8
    [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'],
    # Position 9 moved a after i
    [' ', 'e', 't', 'o', 'i', 'a', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'],
    # Position 10 swapped b & y
    [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'b', 'w', 'g', 'p', 'y', 'v', 'k', 'x', 'q', 'j', 'z'],
    # Position 11 swapped u & d
    [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'u', 'l', 'd', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'],
    # Position 12
    [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'],
    # Position 13 swapped o & i, moved f left 2
    [' ', 'e', 't', 'a', 'i', 'o', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'f', 'c', 'm', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'],
    # Position 14
    [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'],
    # Position 15 swapped p & g, m & f
    [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'f', 'm', 'y', 'w', 'p', 'g', 'b', 'v', 'k', 'x', 'q', 'j', 'z'],
]

# Apply ShiftRows so list is in correct order for ciphertexts
frequencies = [-1]*16

frequencies[0] = english[0]
frequencies[4] = english[4]
frequencies[8] = english[8]
frequencies[12] = english[12]

frequencies[1] = english[5]
frequencies[5] = english[9]
frequencies[9] = english[13]
frequencies[13] = english[1]

frequencies[2] = english[10]
frequencies[6] = english[14]
frequencies[10] = english[2]
frequencies[14] = english[6]

frequencies[3] = english[15]
frequencies[7] = english[3]
frequencies[11] = english[7]
frequencies[15] = english[11]
