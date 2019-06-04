# CryptoFunHouse CTF-style challenges

Both of these challenges are rather difficult. Don't be disheartened if you have to use the sample plaintext or part of this writeup to solve them.

If you're interested, the program used to create the challenge can be found under the *go_program* directory. Assuming you have Go installed, you can run it with:

```
go get https://github.com/xrmon/aes
go run one.go
```

This will download & run the AES implementation at https://github.com/xrmon/aes.

The book used in the challenge was *The Economy of Machinery and Manufactures*, by Charles Babbage (available in three parts [here](http://historyofeconomicthought.mcmaster.ca/babbage/index.html)). To make the challenge easier all punctuation and numbers were removed, roman numerals were converted to text, and letters were converted to lower case. The book is otherwise unaltered.

###Question 1

Usually, the Rijndael cipher (AES) is iterated over several rounds to ensure a secure encryption: for AES with a 128-bit key, 10 rounds are necessary. It comes as no surprise that when only a single round is used, the cipher is very weak.

The key point is that in Rijndael, the MixColumns step it not applied on the final round. With only one round, the MixColumns operation never happens. We must also remember that an additional AddRoundKey operation is applied with the master key before the rest of the algorithm. As such, the encryption process for AES-ONE looks like this:

* **AddRoundKey** with master key
* **SubBytes**
* **ShiftRows**
* **AddRoundKey** with first round key

If you've forgotten how any of these three operations work, have a quick read [here](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard).

Notice in the SubBytes operation, the input value of one byte of the state has no impact on the output value of any other byte. In addition, the position of that byte in the state has no impact on its output value. As such, the ShiftRows and SubBytes operations can be swapped (in maths terms, we say the operations **commute**). Therefore, the encryption process of AES-ONE is equivalent to:

* **AddRoundKey** with master key
* ***ShiftRows***
* ***SubBytes***
* **AddRoundKey** with first round key

Now, in the AddRoundKey step, once again, the value of any one byte has no impact on the value of any other byte during the operation (remember, each byte is xored with the corresponding byte of the key). This time, the byte's position in the array does have an impact, as each byte of the key will usually be different, so the ShiftRows operation is not commutative with AddRoundKey. However, we can swap the order of AddRoundKey and ShiftRows if we first apply ShiftRows to the master key. Thus, our encryption process is equivalent to:

- ***ShiftRows***
- ***AddRoundKey*** with ***ShiftRows***(master key)
- **SubBytes**
- **AddRoundKey** with first round key

Since both the keys are fixed throughout all the ciphertexts in the challenge, we can model the AddRoundKey, SubBytes and AddRoundKey steps as some unknown permutation that maps every byte onto some other byte. This permutation will be different for each of the 16 positions of the state. The encryption process is now fairly simple:

* **ShiftRows**
* ***Unknown permutation***

The cipher now looks vaguely similar. Remember how the substitution cipher, covered in part 2, is essentially a permutation of the alphabet, where each letter of the alphabet is mapped to another letter of the alphabet:

 A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

 X H W Y M N P R F J O A C Z U L G K T B I V S Q D E

So A->X, B->H etc. Our new unknown permutation is fairly similar: each byte between 0 and 255 is mapped to some byte between 0 and 255. In addition, we know that the plaintext is lower-case english text with spaces. So we would expect to see a total of 27 different bytes in each position, when we analyse the ciphertexts. We can then perform frequency analysis, with a bit of manual guesswork, to deduce the mapping of bytes in the ciphertext to english letters. Crucially, and perhaps most challengingly, there is a different mapping for each of the 16 positions in the AES state - so we need to perform 16 different sets of frequency analysis to deduce the solution, and the online substitution cipher solvers will not work.

This is rather difficult, since frequency analysis isn't perfect and some letters will need swapping for each of the 16 positions. To help with this, the target plaintext contains the word "rijndael", in the hopes of providing a recognizable word to use as an anchor point when swapping letters and cracking the cipher. By swapping letters and developing a mapping for each of the 16 positions so that the ciphertexts roughly decode as English, it is possible to break the cipher and discover that the target plaintext is "rijndael is king". A sample solution is provided in question_1.py, which uses the manually developed frequency orderings in freq.py. This doesn't decode the entire plaintext, but the first few plaintexts and the target all decode in their entirety. With more work, or a smarter algorithm, the entire plaintext could be decoded.

A slightly easier, but still impressive solution was to use the provided plaintext to break the cipher. Spaces are reliably the most common 'letter' in English, so it is easy to deduce that the start of the plaintext is something of the form "xxx xxxxxxx xx xxxxxxxxx xxx xxx". Looking at the linked plaintext, we know this is "the economy of machinery and man". By comparing the plaintext to the bytes of the ciphertext with the bytes of the plaintext (remembering that everything is lower case and there is no punctuation), we can deduce the 16 permutations of bytes to letters without needing full frequency analysis. In the crypto world we'd call this a **known plaintext attack** since knowing a sample of plaintext-ciphertext pairs, we can go on to break other ciphertexts. The provided plaintext can also be used with the first solution to fine-tune the mappings given by frequency analysis, during the phase of manually swapping letters.

### Question 2

Given two plaintext-ciphertext pairs, it is possible to deduce the key used in the encryption, assuming a 128-bit master key is used. Let's take two plaintext-ciphertext pairs deduced through our frequency analysis in the first part:

*"the economy of m": 7468652065636f6e6f6d79206f66206d -> 0c9e246cb8a1bfa3b0e947a1a94c8d11*

*"achinery and man": 616368696e65727920616e64206d616e -> 998fffc15bd9cf74804d59fc23cb6e59*

Remember that the AES-ONE encryption process is equivalent to **ShiftRows** followed by our unknown permutation of **AddRoundKey** and **SubBytes**. To makes things simple, let's apply **ShiftRows** to our plaintexts right away:

*"tcymem  ofenoho ": 7463796d656d20206f66656e6f686f20 -> 0c9e246cb8a1bfa3b0e947a1a94c8d11*

*"aennnaai mhy crd": 61656e6e6e616169206d687920637264 -> 998fffc15bd9cf74804d59fc23cb6e59*

Hence the encryption operation is now:

- **AddRoundKey** with **ShiftRows**(master key)
- **SubBytes**
- **AddRoundKey** with first round key

Let's get some notation. Let x be a byte of the plaintext, and r be the corresponding byte of the first round key, and k be the corresponding byte of the 128-bit master key after ShiftRows. We'll also say that E(x) represents the encrypted output of byte x, and s(x) represents the output of byte x in the AES s-box. Putting this all together, we can create an equation for the encryption process of AES-ONE:

E(x) = s(x ⊕ k) ⊕ r

Take byte x', where x' is from a different plaintext and is in the same position as byte x. We can now write an equation for the encryption of x':

E(x') = s(x' ⊕ k) ⊕ r

Now, let's combine the two equations and cancel out the round key r:

E(x) ⊕ E(x') = s(x ⊕ k) ⊕ s(x' ⊕ k) ⊕ r ⊕ r

E(x) ⊕ E(x') = s(x ⊕ k) ⊕ s(x' ⊕ k)

The values of E(x), E(x'), x and x' are known through our two plaintext-ciphertext pairs. The unknown key value k appears in both instances of the sbox, meaning we can't rearrange the equation in terms of k like we did back in school. However, there are only 256 possible values of the key, meaning we can brute force the value of k and find the value which satisfies the equation.

Unfortunately, when we try this, we don't get a unique value for each key byte. In fact, we end up with two possible values for each position (see code in question_2.py):

```
Key byte for pos 0: 0x4e N
Key byte for pos 0: 0x5b [
Key byte for pos 5: 0x30 0
Key byte for pos 5: 0x36 6
Key byte for pos 10: 0x61 a
Key byte for pos 10: 0x76 v
Key byte for pos 15: 0x21 !
Key byte for pos 15: 0x22 "
Key byte for pos 4: 0x73 s
Key byte for pos 4: 0x78 x
Key byte for pos 9: 0x56 V
Key byte for pos 9: 0x5a Z
Key byte for pos 14: 0x25 %
Key byte for pos 14: 0x64 d
Key byte for pos 3: 0x16
Key byte for pos 3: 0x5f _
Key byte for pos 8: 0x2b +
Key byte for pos 8: 0x64 d
Key byte for pos 13: 0x33 3
Key byte for pos 13: 0x38 8
Key byte for pos 2: 0x74 t
Key byte for pos 2: 0x79 y
Key byte for pos 7: 0x23 #
Key byte for pos 7: 0x34 4
Key byte for pos 12: 0xc
Key byte for pos 12: 0x43 C
Key byte for pos 1: 0x30 0
Key byte for pos 1: 0x3b ;
Key byte for pos 6: 0x2d -
Key byte for pos 6: 0x30 0
Key byte for pos 11: 0x2a *
Key byte for pos 11: 0x6e n
```

If you got this far, well done. To solve for a unique key value we'll need to go back to our original equations. Where Xi is the input byte in the ith position, Ki is the key byte in the ith position after ShiftRows and Ri is the first round key byte in the ith position, we can say that:

E(Xi) = s(Xi ⊕ Ki) ⊕ Ri,  *and*

E(Xi') = S(Xi' ⊕ Ki) ⊕ Ri,  *for 0 <= i < 16*.

Thus we have 32 equations that the master key must satisfy.  Since there are two possibilities for each of the 16 positions, there are 16 possible keys to check. Through the Rijndael key schedule, the first round key is derived from the master key (although each byte of the round key can depend on several bytes of the master key, so we must now brute force the entire 16-byte master key, rather than individual bytes). The values of the round keys follow a recurrence relationship starting from the master key, implemented in question_2.py as the function *getRoundKey*. The Rijndael key schedule is described in detail [here](https://en.wikipedia.org/wiki/Rijndael_key_schedule).

The Python solution script can easily brute force these possibilities and deduce that the key is *4e30745f73302d346456616e43336421*, or "N0t_s0-4dVanC3d!" as text.
