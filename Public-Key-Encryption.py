#!/usr/bin/env python
# coding: utf-8

# Author: Amrutha Purna Vadrevu| Last edited: 21/11/2023

#Task1: Alternative Method of Public-Key Encryption

# What the code does: 
# The code generates a public-private key pair which is used to encrypt a plaintext, generate ciphertext and which can also be used to decrypt the ciphertext to retrieve the original plaintext. 

## Required Inputs:
# 1. n = enter the number of elements for easy key
# 2. plaintext = enter the message that needs to be encrypted

## Output:
# 1. e - easy key (part of private key)
# 2. h - hard key (public key)
# 3. ciphertext - message encrypted using public key
# 4. plaintext - ciphertext decrypted using private key (this is the same as the original message)

### 1.1: Generation of Public-Private Key Pair

# Property: A public key (h) is generated from a private key (e, q, w) where e is the easy key and q, w are co-primes with the following property: 

# hi = (w ei mod q) for 1 <= i <= n

# Easy key, e, is chosen such that it is a random set of integers e = (e1, e2, . . . , en) such that each new element of the set is greater than the sum of the previous elements in the set 

# In[1]:

#### Importing necessary libraries

import random #To generate random set of integers
import math #To use gcd function


# In[2]:


def generate_public_key(n):
    
    #Generation of e, the easy key, which is part of the private key
    
    e = [] # An empty list to store the random set of positive integers with the given property
    prev_sum = 0
    for i in range(n):
        ei = random.randint(prev_sum + 1, prev_sum + 2 * n) # To ensure a sensible list of numbers, the upper limit is set to (prev_sum + 2n)
        e.append(ei)
        prev_sum += ei

        
    # Select a prime number q such that q > 2en
    
    q = random.randint(2 * e[-1] + 1, 10000)
    while not is_prime(q):
        q = random.randint(2 * e[-1] + 1, 10000)

        
    # Select a random w such that gcd(w, q) = 1
    
    w = random.randint(2, q-1)
    while math.gcd(w, q) != 1:
        w = random.randint(2, q-1)

    # Compute h
    h = [w * e[i] % q for i in range(n)]

    return h, (e, q, w) #Public-Private key pair


#### Function to check whether a number is prime or not

# In[3]:


def is_prime(num):
    if num>1:
        for i in range(2, int((num/2) + 1)): # If num is divisible by any number between 2 and n / 2, it is not prime
            if((num % i) == 0):
                return False
                break
            else: 
                return True
    else: 
        return False


#### Functions to convert plaintext to bits and vice-versa

# The message is in plaintext. For encryption and decryption, the plaintext needs to be converted to binary data since the model works on each bit of the message. After decryption, the decrypted message will be in binary form, which needs to be converted back to plaintext. 

# In[4]:


def convert_plaintext_to_bits(plaintext):
    bits = []
    for char in plaintext:
        binary_representation = bin(ord(char))[2:].rjust(8, '0') # Starting from the third bit to remove the "0b" prefix of binary number. If the character does not have 8 bits, it is padded with 0. Else, it is left as it is.   
        bits.extend(map(int, binary_representation)) # characters in the binary_representation string are converted to integers and added to the bits list

    return bits


def convert_bits_to_plaintext(bits):
    plaintext = ""
    char_bits = []
    for bit in bits:
        char_bits.append(bit) # Creating a list of 8 bits
        if len(char_bits) == 8: 
            char = chr(int("".join(map(str, char_bits)), 2)) # combines all the bits into a continuous binary representation which is then converted to ASCII character
            plaintext += char
            char_bits = []

    if char_bits:  # If there are remaining bits
        char = chr(int("".join(map(str, char_bits)), 2))
        plaintext += char

    return plaintext


#### Encryption
# Property: To encrypt an n-bit message m = (m1,m2, . . . ,mn) for Bob, Alice would compute c = h1m1+ h2m2 + · · · + hn*mn.
# The message needs to be split into blocks of length h (with n bits) so that the property can be applied to each bit of message and hard key to generate the ciphertext. 


# In[5]:


def encrypt(plaintext, h):
    bits = convert_plaintext_to_bits(plaintext)

    # Split the message into blocks of size len(h)
    blocks = [bits[i:i+len(h)] for i in range(0, len(bits), len(h))]
    
    # Encrypt each block separately
    encrypted_blocks = [sum(h[j] * block[j] for j in range(len(block))) for block in blocks]

    return encrypted_blocks


#### Decryption
 
# To decrypt a ciphertext c, Bob can compute c′ = c w^(−1) mod q so that in fact, c′ = e1m1 + e2m2+ · · · + en*mn. The property in the first step of the public key generation (that each ei is greater than the sum of all previous values) allows Bob to recover each bit of the plaintext one at a time. To do this from c′, start from en and check if the existing sum (starting with c′) is larger than or equal to en. If it is, then mn = 1 and you compute c′ = c′ − en, but if it’s not then mn = 0). Then do the same for e(n−1), and so on, all the way to e1.

# In[6]:


def decrypt(ciphertext_blocks, e, q, w):
    w_inv = pow(w, -1, q)
    bits = []

    for block in ciphertext_blocks:
        c_prime = block * w_inv % q

        block_bits = []

        for ei in reversed(e):
            if c_prime >= ei:
                block_bits.insert(0, 1)
                c_prime -= ei

            else:
                block_bits.insert(0, 0)

        bits.extend(block_bits)

    plaintext = convert_bits_to_plaintext(bits)

    return plaintext


# In[7]:


n = int(input("Enter the number of random integers to be generated: "))
h, (e, q, w) = generate_public_key(n)
print("Public key:", h)
print("Private key:", (e, q, w))


# In[8]:


plaintext = input("Enter the message: ")


# In[9]:


ciphertext = encrypt(plaintext, h)
print("Encrypted message:", ciphertext)


# In[10]:


plaintext_prime = decrypt(ciphertext, e, q, w)
print("Decrypted message:", plaintext_prime)
