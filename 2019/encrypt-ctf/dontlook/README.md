### Dontlook at this Challenge

I noticed the encrypt CTF on ctftime the other day and thought I'd have a go. After having some fun with the crypto challenges a reversing challenge called "Dontlook at this challenge" caught my eye. Since we were told not to, we of course have to look at this.

The challenge is worth 500 points, more than any other challenge, but despite spending several hours reversing I was a little disappointed that the solution was so simple. Judging by the 96 solves it attracted, quite a few others solved it too. The challenge requested that a writeup was written - so here it is.

We are given an 32-bit i386 file *a.out*. When ran we are asked for a license key and told to make a keygen:

```
$ ./a.out
Welcome To The Uncrackable Software!!!
make a keygen and get rewarded!....
Enter The Correct License Key:
```

We'll open the file up in radare and begin to take a look. For some reason Radare couldn't find the main function, but after a quick look the entry function looks reasonably legit, with the usual call to *__libc_start_main*. 

![Radare couldn't find the main function, but the entry function looks reasonably legit](https://raw.githubusercontent.com/xrmon/ctf-writeups/master/2019/encrypt-ctf/dontlook/entry_function.png)

This program has various features that make it a pain to reverse statically, so I loaded it onto my linux VPS and began reversing it dynamically. Stepping through manually we find something that looks suspiciously like a main function, with calls to libc functions like *ptrace* and *puts*. Strangely, this is at a a strange address **0x5657b9b4**, whereas the same code is at **0x9b4** when we analyse the file statically, without the radare debugger. Clearly, some kind of ASLR is moving the *.text* section about, which makes setting breakpoints a pain.

![Stepping through manually we find something that looks like the main function](https://raw.githubusercontent.com/xrmon/ctf-writeups/master/2019/encrypt-ctf/dontlook/main_function.png)

The first thing we notice is a call to *ptrace*, where the program attempts to trace itself. This is a common method to prevent debuggers, as *ptrace* will fail when the process is already being debugged. If we carry on from here we get a lovely message printing "so you wanna trace me?", and the program quits out.

Fortunately this is easy to combat by opening the file in radare's write mode, seeking to the conditional jump at **0x9e0** and replacing it with an unconditional jump with the *wx eb* command (0xEB is the x86 opcode for an unconditional jump). Now, the program will still call ptrace and this will fail, but it will move on regardless.

As a side note, the read-only data for the file is accessed relative to the EBX register, so radare can't statically find the strings such as is used in puts above. I found all the strings by stepping through with the debugger and inspecting the registers just before each function call.

![Replace the conditional jump after ptrace with a conditional one](https://raw.githubusercontent.com/xrmon/ctf-writeups/master/2019/encrypt-ctf/dontlook/jump.png)

Next we see a call to *signal* which creates a signal handler for signal number 5, SIGTRAP. If we inspect the function that is specified as the handler, we find a function which simply prints a message with *puts*. I can only assume this is supposed to intercept breakpoints as another anti-debugger technology (since SIGTRAP is used by debuggers to implement breakpoints). We could easily have overwritten the call to *signal* with nops with a command like *wx 9090909090*. However for whatever reason this didn't affect radare's debugger functionality and I didn't have to do anything. If anyone knows why this was the case, I'd love to know why.

The final anti-reversing trick is a call to *sleep* for 2 seconds. This doesn't really do much to affect our analysis, but my guess is this is to prevent a brute force attack to guess the key. We could easily overwrite this with nops, but we don't really need to since we don't really need to brute force when we can simply reverse the binary.

Going further into the main function, we load a bunch of strings onto the stack which when printed look  suspiciously like an encrypted flag of some sort.

![Encrypted flag on stack](https://raw.githubusercontent.com/xrmon/ctf-writeups/master/2019/encrypt-ctf/dontlook/encrypted_flag.png)

At this point the program does all sorts of crazy stuff involving opening itself, reading certain bytes and writing this out to a file called "dontlook". It then reopens this file, does some processing on it and eventually deletes this file. I spent a few hours reversing this stuff, but the final solution didn't require much knowledge of it at all. I'd be curious to see the source code to see what the program was actually doing here.

After some searching, I found the important bit of the program. Buried in a side function called from the main function, we find a call to *printf("Enter The Correct License Key: ")*, and *scanf("%100s", input)*. This is the bit that reads in the licence key. A function is then called, and we either branch to print *"[\*] Access Granted!"* or an empty line *""*. It looks like the function we just called is some sort of comparison function which takes as input the user's input, and some string generated by the rest of the program (involving that crazy section where it reads itself that I only got halfway through).

![The important bit that checks the flag](https://raw.githubusercontent.com/xrmon/ctf-writeups/master/2019/encrypt-ctf/dontlook/important_bit.png)

We can simply set a breakpoint here in the radare debugger and read the arguments passed to this checking function dynamically, and sure enough we get a flag. We could have spent hours reversing the program statically - and I'm unsure whether this was the intended solution. But this way is far easier!

![Getting the flag by setting a breakpoint and reading the strings at eax](https://raw.githubusercontent.com/xrmon/ctf-writeups/master/2019/encrypt-ctf/dontlook/flag.png)

We can read the flag as **encryptCTF{dontl00k__1ts_my_secret}**!

