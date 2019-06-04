def ShiftRows(state):
    new = [-1]*16
    # First row, no shift
    new[0] = state[0]
    new[4] = state[4]
    new[8] = state[8]
    new[12] = state[12]
    # Second row, shift left 1
    new[1] = state[5]
    new[5] = state[9]
    new[9] = state[13]
    new[13] = state[1]
    # Third row, shift left 2
    new[2] = state[10]
    new[6] = state[14]
    new[10] = state[2]
    new[14] = state[6]
    # Fourth row, shift left 3
    new[3] = state[15]
    new[7] = state[3]
    new[11] = state[7]
    new[15] = state[11]
    return new

input = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
output = ShiftRows(input)
print(output)
