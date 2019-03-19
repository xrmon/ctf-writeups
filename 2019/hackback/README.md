This is a writeup from the HackBack inter-university CTF in the UK, produced by tryhackme: https://tryhackme.com/. This CTF was great fun, the challenges weren't too difficult but were challenging enough to get a sense of satisfaction when you solved them. I thought I'd do a writeup for one of the challenges that I solved 🎉.

# Go to Hell, Diffie!

In this challenge, we are told that Andrew wants to send a secure message by securely sharing a key and encrypting the message with AES-CBC (cipher-block-chaining):

-----------------------------
*Andrew is a developer and he’s been assigned with the task of sending a secure message to her supplier. While he has been extremely determined, he does not have a lot of knowledge about security. 
Here are some of the steps he took to develop the secure application:*
* *he tried to establish a shared key(in a not so secure way)*
* *he then used this shared key to encrypt the messages(due to his knowledge of security he used the AES-CBC to encrypt this message)*

*In this challenge, remember that Andrew does not have a lot of information about how hashing or stages during encryption work(including deriving a key and IV).*

-----------------------------

We are given a PCAP file, which when opened up in Wireshark shows ascii information sent in plaintext over UDP. First a prime **P**=13 and generator **g**=6 is sent, followed by each party sending 
a public exponent. Party 1 sends the exponent **A**=8 (marked ex1 in the PCAP and party B sends the exponent **B**=9 (marked ex2 in the PCAP).

![PCAP file showing the Diffie hetman values being exchanged](https://raw.githubusercontent.com/xrmon/ctf-writeups/master/2019/hackback/pcap_screenshot.png)

Before we go on, let’s get a quick primer on how Diffie Hellman works:

### Recap on Diffie-Hellman
Take prime **P** and generator **g**. Here, P=13 and g=6.

A generator simply means that any number modulo P can be reached by multiplying g by itself some number of times. So for P=13 and g=6:
6^0 ≡ 1  
6^1 ≡ 6  
6^2 ≡ 10  
6^3 ≡ 8  
6^4 ≡ 9  
6^5 ≡ 2  
6^6 ≡ 12  
6^7 ≡ 7  
6^8 ≡ 3  
6^9 ≡ 5  
6^10 ≡ 4  
6^11 ≡ 11  
6^12 ≡ 1  

(For reference, this was done with the following Python script. Also note we are using **congruence** ≡ not **equality** =, which you can read about 
[here](https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/congruence-modulo))
```
for i in range(0, 13):
    print("6^" + str(i) + " ≡ " + str(6**i % 13))
```

Both **P** and **g** are publicly shared. Next Alice chooses a secret exponent **a** and calculates A=g^a, and Bob chooses a secret exponent **b** and calculates B=g^b. Alice and Bob share **A** 
and **B** with one another - noone except Alice knows **a**, and no-one except Bob knows **b**.

Alice can now calculate a secret key **K** = B^a = (g^b)^a = g^ab. She does not need to know **b** to do this, since Bob has sent her **B** publicly. Bob can also calculate **K** = A^b = (g^a)^b = 
g^ab. He likewise does not need to know **a** to do this. However, an eavesdropper knows neither **a** nor **b** and cannot find **K**. Fantastic! Or can’t they?

### Solving the problem
In the real world to break Diffie Hellman you need to solve something called the **Discrete Logarithm Problem**, and it’s *very very hard*. However, because the numbers here are so small it’s 
trivial to do it by hand.

We know that A = 8 ≡ 6^a. Normally, it is very difficult to find the **a** such that g^a ≡ A modulo P. This is the discrete logarithm problem and it’s where the security of Diffie Hellman comes 
from. However, here we can simply refer to the table I printed above and see that 6^3 ≡ 8, hence a = 3. We can now calculate the secret key K ≡ B^a ≡ 9^3 ≡ 27 ≡ 1.

Hence the secret key is 1 - how secure!

I didn’t actually solve the third part to this problem during the CTF, which was to derive an AES key and decrypt the traffic, though from talking to an admin afterwards it was annoyingly just a 
matter of guesswork. I had tried keys and IVs of 01010101010101010101010101010101 (each byte is 1), 31313131313131313131313131313131 (ascii 1’s), 11111111111111111111111111111111 (each hex digit 
is 1) FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF (every bit is 1) etc. Apparently, the solution used AES256 instead of 128, and the key was simply 01010101…. So my first guess was correct apart from the key 
length.

I loved the first part of the challenge. It’s great to use some maths for an actual challenge. To be honest, I found the latter part a little annoying, since it involved a little too much 
guesswork. Even though the options seem simple, there’s a few too many variables at play - we don’t know if the IV and the key are the same, we don’t know the key length, we don’t know if it’s 
ascii 1’s or hex 1’s or byte 1’s. A little nudge would have been nice to save the tedious guesswork.

Overall though this CTF was great fun, I had a blast - I wish them good luck for their next event, which I’m told will be in the Autumn.
