ptA = "9c53fc4f03020389898c77d7cdaa0f74fa3f9d28787533fed6fb1fe3b9f56340"
ptB = "bf164d661c22f304765e22c443bf0fb5c56f120d2f5b895b1b2b41ac1cc83c81"
ptC = "dbccb2cd811df9b97b9e34789c010e05b093d1bff86d8d8924f80049f0722f78"

ptA1 = int(ptA[:32], 16)
ptA2 = int(ptA[32:], 16)
ptB1 = int(ptB[:32], 16)
ptB2 = int(ptB[32:], 16)
ptC1 = int(ptC[:32], 16)
ptC2 = int(ptC[32:], 16)

IV1 = ptA1 ^ ptA2
IV2 = ptB1 ^ ptB2
IV3 = ptC1 ^ ptC2

flag = int.to_bytes(IV1, 16, 'big') + \
       int.to_bytes(IV2, 16, 'big') + \
       int.to_bytes(IV3, 16, 'big')

print("IV1:", int.to_bytes(IV1, 16, 'big'))
print("IV2:", int.to_bytes(IV2, 16, 'big'))
print("IV3:", int.to_bytes(IV3, 16, 'big'))
print("")
print("Flag:", flag)
