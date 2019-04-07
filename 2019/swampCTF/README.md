# We Three Keys

This was a fun challenge based around an interesting quirk of block ciphers in CBC mode.

*Side note: in this challenge we are actually given the source code for the server, given here as serv.py. I didn't notice this during the CTF so I'll write from the perspective of solving the challenge blind. There's a few cool tricks you can do to see what's going on.*

### Challenge

In this challenge we connect to a TCP service and are able to encrypt and decrypt arbitrary messages with any of three unknown keys. The challenge is to recover the three keys. Actually, the trick here is to recover the IVs through a quirk of the CBC mode of operation - the challenge just happens to use the key as the IV.

![The program allows arbitrary encryption and decryption with 3 unknown keys](https://raw.githubusercontent.com/xrmon/ctf-writeups/master/2019/swampCTF/encrypt.png)

### Getting information

From the source code we can see this is AES CBC. However, having missed the source code entirely, I was able to deduce that this was CBC mode on some block cipher with block size 16 (almost certainly AES). Recall that CBC mode on a block cipher works as follows (image credit Wikipedia):

![CBC mode encryption diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/CBC_encryption.svg/1202px-CBC_encryption.svg.png)

![CBC decryption diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/CBC_decryption.svg/1202px-CBC_decryption.svg.png)

To prevent blocks with the same plaintext being encrypted to the same ciphertext, we xor each plaintext with the previous ciphertext before encrypting. We do the inverse to decrypt. The first plaintext is instead xored with an IV, since there is no previous ciphertext to xor it with.

We can verify that the server uses CBC mode by encrypting a ciphertext with at least two blocks, then making some changes to the first block and decrypting. The first block will decrypt to nonsense: changing one bit of the ciphertext will change around 50% of the bits in the resulting plaintext. However, the second block will only have a few changes in the exact positions that we edited in the first block, due to the xor operation.

![We can verify it is CBC by changing bytes in the first block](https://raw.githubusercontent.com/xrmon/ctf-writeups/master/2019/swampCTF/check_cbc.png)

### Solution

An interesting quirk of CBC mode is that we can recover the IVs used. Note that in the real world this doesn't necessarily help us too much - IVs don't necessarily need to be secret (although they usually need to be random). However in this case the key used is the same as the IV, so recovering the IV trivally breaks the encryption.

Say we decrypt the ciphertext blocks A and B. Both are decrypted, then xored with either the IV or the previous ciphertext. Therefore as output we get the decrypted blocks D(A) ⊕ IV, and D(B) ⊕ A, where D represents our decryption function (in this case AES, but this would work with any other block cipher in CBC mode). Now imagine that instead of A and B, we send the same block A twice. Now, we get the plaintext blocks PT1 = D(A) ⊕ IV, and PT2 = D(A) ⊕ A. Since xor is self-inverse, we can trivially rearrange to get:

D(A) = PT1 ⊕ IV, and D(A) = PT2 ⊕ A

Therefore:

PT1 ⊕ IV = PT2 ⊕ A

And so:

IV = PT1 ⊕ PT2 ⊕ A

Now, if we make the ciphertext block A all zeros (000000…), anything xored with A is itself. So, in the case where we simply send two blocks of all zeros we have:

IV = PT1 ⊕ PT2

Now we just have to do this.

![Recovering the first IV](https://raw.githubusercontent.com/xrmon/ctf-writeups/master/2019/swampCTF/key_1.png)

![Recovering the second IV](https://raw.githubusercontent.com/xrmon/ctf-writeups/master/2019/swampCTF/key_2.png)

![Recovering the third IV](https://raw.githubusercontent.com/xrmon/ctf-writeups/master/2019/swampCTF/key_3.png)

We xor both plaintext blocks for each key and recover the three IVs:

IV1: flag{w0w_wh4t_l4

IV2: zy_k3yz_much_w34

IV3: k_crypt0_f41ls!}

And get the flag:

flag{w0w_wh4t_l4zy_k3yz_much_w34k_crypt0_f41ls!}

I wrote a neat python script, which you can find at recover_iv.py.