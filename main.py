# Gennadii Sytov - CS485 - Winter2020 - Project 2

import sys
import key_generator as KG
import PSUCrypt

def stringToHex(str):
    s_hex = []
    for c in str:
        s_hex.append(ord(c))

    h_str = ""
    for h in s_hex:
        h_str += format(h, "02x")
    return h_str


def getKeyFromFile(file_name):
    try:
        file = open(file_name, 'r')
    except IOError:
        print("Error: Can't open the \"" + file_name + "\" file.")
    with file:
        key = file.readline()
        return key

def getSrcFromFile(src_file, mode):
    try:
        file = open(src_file, 'r')
    except IOError:
        print("Error: Can't open the \"" + src_file + "\" file.")
    with file:
        hex_strings = []
        counter = 0
        i = -1
        while True:
            c = file.read(1)
            if not c:
                break
            if counter % 8 == 0:
                hex_strings.append("")
                i += 1
            if mode == "-e":
                c = format(ord(c), "02x")
                counter += 1
            counter += 1
            hex_strings[i] += c

        if i < 0:
            raise ValueError("Error: the source file is empty!")
        hex_strings[i] = format(int(hex_strings[i], 16), "08x")
        return hex_strings
    
def getCipherTextFromFile(src_file):
    try:
        file = open(src_file, 'r')
    except IOError:
        print("Error: Can't open the \"" + src_file + "\" file.")
    with file:
        cipher_text = []
        i = -1
        while True:
            l = file.readline()
            if not l:
                break
            cipher_text.append(l)
            i += 1

        if i < 0:
            raise ValueError("Error: the cipher text file is empty!")
        return cipher_text


def saveResultsToFile(dest_file, results, option):
    try:
        file = open(dest_file, 'w')
    except IOError:
        print("Error: Can't create the \"" + dest_file + "\" file.")
    with file:
        counter = 0
        char_tup = ""
        for r in results:
            if option == "-e":
                file.write(str(r[0]) + " " + str(r[1]) + "\n")
            else:
                for c in r:
                    char_tup += c
                    counter += 1
                    if(counter == 2):
                        value = int(char_tup, 16)
                        if value != 0:
                            char_tup = chr(value) 
                            file.write(char_tup)
                        counter = 0
                        char_tup = ""


def main():
    argv = sys.argv[1:]
    if len(argv) < 1:
        print("Missing command line arguments!")
        return
    elif len(argv) > 4:
        print("Unknown command line arguments!")
        return

    option = argv[0]
    seed = None
    if option == "-k":
        if len(argv) > 1:
            seed = int(argv[1])
        KG.KeyGenerator(seed)
        print("You have successfully generated the keys. The keys have been saved to the pubkey.txt and prikey.txt files.")
        return

    if len(argv) < 3:
        print("Missing command line arguments!")
        return

    src_file = argv[1]
    dest_file = argv[2]

    if option != "-e" and option != "-d" and option != "-k":
        print("Uknown option. Must be either \'-e\' for encryption, \'-d\' for decryption or \'-k\' for generating keys")
        return
    
    if len(argv) == 4:
        seed = argv[3]

    pub_key = getKeyFromFile("pubkey.txt")
    pri_key = getKeyFromFile("prikey.txt")

    cipher = PSUCrypt.PSUCrypt(pub_key, pri_key, seed)
    if option == "-e":
        src = getSrcFromFile(src_file, option)
    else:
        src = getCipherTextFromFile(src_file)

    results = []
    for s in src:
        if option == "-e":
            i = int(s, 16)
            results.append(cipher.encrypt(i))
        else:
            print(s)
            h = format(cipher.decrypt(s), "08x")
            results.append(h)
    
    print(results)
    saveResultsToFile(dest_file, results, option)

    process = ""
    if option == "-e":
        process = "encryption"
    elif option == "-d":
        process = "decryption"
    print("The " + process + " has finished successfully. The result has been saved to the \"" + dest_file + "\" file.")
    


if __name__ == '__main__':
    main()