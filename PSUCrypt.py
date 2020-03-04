# Gennadii Sytov - CS485 - Winter2020 - Project 2

import random

class PSUCrypt:

    def __init__(self, pubkey, prikey, seed = None):
        pk = pubkey.split( )
        if len(pk) < 3:
            raise ValueError("Error parsing the public key.")
        self.d = int(prikey)
        self.e1 = int(pk[0])
        self.e2 = int(pk[1])
        self.p = int(pk[2])
        self.random = random
        self.random.seed(seed)

    def encrypt(self, plaintext): #plaintext of type int
        r = self.random.randint(1, self.p - 1)
        c1 = pow(self.e1, r, self.p)
        c2 = ((plaintext % self.p) * pow(self.e2, r, self.p)) % self.p
        return [c1, c2]

    def decrypt(self, ciphertext): #ciphertext should be a string
        ct = ciphertext.split( )
        if len(ct) < 2:
            raise ValueError("Error parsing the ciphertext.")
        c1 = int(ct[0])
        c2 = int(ct[1])

        P = ((c2 % self.p) * pow(c1, self.p - 1 - self.d, self.p)) % self.p
        return P


# pubkey = "2 7184637153 11839090163"
# prikey = "8836531810"
# pCrypt = PSUCrypt(pubkey, prikey)
# ptx = int("abcd", 16)
# c = pCrypt.encrypt(ptx)
# c = str(c[0]) + " " + str(c[1])
# print("Ciphertext: " + c)
# result = pCrypt.decrypt(c)
# result = format(result, "04x")
# print("Plaintext: " + result)