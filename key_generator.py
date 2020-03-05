# Gennadii Sytov - CS485 - Winter2020 - Project 2

import random

class KeyGenerator:

    constant_34bit = pow(2, 34)
    constant_33bit = pow(2, 33) - 1
    constant_32bit = pow(2, 32)

    def __init__(self, seed = None, publicKeyFileName = "pubkey.txt", privateKeyFileName = "prikey.txt"):
        self.publicKeyFileName = publicKeyFileName
        self.privateKeyFileName = privateKeyFileName
        self.random = random
        self.random.seed(seed)

        self.createKeys()


    def millerRabinPrimalityTest(self, p, r):
        a = self.random.randint(2, p - 2)
        z = pow(a, r, p)
        if z == 1 or z == p - 1:
            return True
        while r != p - 1:
            z = pow(z, 2, p)
            r *= 2
            if z == 1:
                return False
            elif z == p - 1:
                return True
        
        return False
    
    def primalityTest(self, p, s = 100):
        if p <= 1 or p == 4:
            return False
        if p == 2 or p == 3:
            return True
        if p % 2 == 0:
            return False

        r = p - 1
        while r % 2 == 0:
            r //= 2

        for i in range(1, s):
            if self.millerRabinPrimalityTest(p, r) == False:
                return False
        
        return True
    
    def generateQPrime(self):
        q = self.random.randint(self.constant_32bit, self.constant_33bit)
        if q % 2 == 0:
            q += 1
        while q % 12 != 5:
            q += 2

        while q < self.constant_33bit:
            if self.primalityTest(q) == True:
                return q
            q += 12
        
        return self.generateQPrime()

    def generatePPrime(self):
        q = self.generateQPrime()
        p = 2*q + 1
        if self.primalityTest(p) == True:
            return p
        return self.generatePPrime()

    def createKeys(self):
        p = self.generatePPrime()

        d = self.random.randint(1, p-2)

        e2 = pow(2, d, p)

        public_key = "2 " + str(e2) + " " + str(p)
        private_key = str(d)

        self.saveResultsToFile(self.publicKeyFileName, public_key)
        self.saveResultsToFile(self.privateKeyFileName, private_key)

    def saveResultsToFile(self, dest_file, result):
        try:
            file = open(dest_file, 'w')
        except IOError:
            print("Error: Can't create the \"" + dest_file + "\" file.")
        with file:
            file.write(result)
               
