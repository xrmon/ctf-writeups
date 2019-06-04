package main

import (
    "github.com/xrmon/aes"
    "log"
    "fmt"
    "io/ioutil"
    "encoding/hex"
)

func encrypt(input [16]byte) [16]byte {
    // Encrypt provided plaintext with with a secret key with 1 round AES
    key := []byte{0x4e, 0x30, 0x74, 0x5f, 0x73, 0x30, 0x2d, 0x34, 0x64, 0x56, 0x61, 0x6e, 0x43, 0x33, 0x64, 0x21}
    const rounds = 1
    roundKeys := aes.KeyExpansion(key[:], 4, rounds+1)
    return aes.BlockEncrypt(input, rounds, roundKeys)
}

func main() {
    // Read in the input file
    inputs, err := ioutil.ReadFile("input.txt")
    if err != nil {
        log.Fatal(err)
    }

    // Iterate through each 16-byte block
    var num int = (len(inputs)/16)-1
    var outputs = make([]byte, num*33)
    var plains = make([]byte, num*33)
    for i := 0; i < num; i++ {
        // Encrypt block
        var in, out [16]byte
        copy(in[:], inputs[i*16:(i+1)*16])
        out = encrypt(in)
        if i < 20 {
            fmt.Printf("In:  % x (%s)\nOut: % x\n", in, string(in[:]), out)
        }
        for j := 0; j < 16; j++ {
            if (in[j] < 0x61 || in[j] > 0x7A) && in[j] != 0x20 {
                log.Fatalf("Invalid byte: %x (%c) at %d", in[j], in[j], i)
            }
        }
        // Copy hex string into output file and add newline
        var string = hex.EncodeToString(out[:])
        copy(outputs[i*33:], string)
        outputs[(i+1)*33-1] = '\n'
        string = hex.EncodeToString(in[:])
        copy(plains[i*33:], string)
        plains[(i+1)*33-1] = '\n'
    }

    // Write ciphertexts to the output file
    err = ioutil.WriteFile("ciphertexts.txt", outputs, 0640)
    if err != nil {
        log.Fatal(err)
    }
    // Write plaintexts to the output file
    err = ioutil.WriteFile("plaintexts.txt", plains, 0640)
    if err != nil {
        log.Fatal(err)
    }

    // Generate target ciphertext
    var in [16]byte
    copy(in[:], "rijndael is king")
    out := encrypt(in)
    fmt.Printf("\nTarget ciphertext: %x\n", out)
}
