import random


#FIX THE FINAL OUTPUT ADD SOME WORDS
#FIND A WAY TO INCLUDE WHITESPACES (method that grabs all the indexes of the whitespaces, and adds them to the new encrypted text)

class Cryptography:
    #all the cryptography techniques will be here

    #some of these need a key for decrypting

    #CAESAR CIPHER
    def caesarEncrypt(self, phrase, key):
        alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        #copied list that is shifted n times (n = key)
        shiftedAlphabet = alphabet[:]
        #phrase that will contain the encrypted phrase
        encryptedPhrase = ""    

        #removes the last element in the list and puts it in the first index n amt of times (n = key)
        for i in range(int(key)):
            lastLetter = shiftedAlphabet.pop()
            shiftedAlphabet.insert(0, lastLetter)
    
        #for every letter in the phrase, the index is grabbed from the original alphabet list and then that index is used to get the value from the shifted alphabet list.
        for letter in phrase:
            newIndex = alphabet.index(letter)
            encryptedPhrase += shiftedAlphabet[newIndex]

        return encryptedPhrase

    def caesarDecrypt(self, encryptedPhrase, key):
    
        alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    
        #DOING THE SAME THING AS THE ENCRYPTION FUNCTION WITH SHIFTING THE LIST TO THE KEY
        shiftedAlphabet = alphabet[:]
        decryptedPhrase = ""    

        for i in range(int(key)):
            lastLetter = shiftedAlphabet.pop()
            shiftedAlphabet.insert(0, lastLetter)

        #NOW DO THE REVERSE OF GETTING THE INDEX OF EACH LETTER FROM THE ENCRYPTED WORD FROM THE SHIFTED LIST, AND GETTING THE VALUE OF THE SAME INDEX FROM OG ALPHABET LIST, GIVING THE PLAINTEXT
        for letter in encryptedPhrase:
            ogIndex = shiftedAlphabet.index(letter)
            decryptedPhrase += alphabet[ogIndex]

        
        
        return decryptedPhrase

    #HASHING
    def hashing(self, phrase):
        hashChar = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9']
        hashed = ""
        for i in range(len(phrase)):
            randIndex = random.randint(0, len(hashChar) - 1)
            hashed += hashChar[randIndex]
        return hashed

    #ATBASH CIPHER
    def atbash(self, phrase):
        alphabet = {'a':'z','b':'y','c':'x','d':'w','e':'v','f':'u',
                    'g':'t','h':'s','i':'r','j':'q','k':'p','l':'o',
                    'm':'n','n':'m','o':'l','p':'k','q':'j','r':'i',
                    's':'h','t':'g','u':'f','v':'e','w':'d','x':'c',
                    'y':'b','z':'a'}
        phraseList = []
        for thing in phrase:
            phraseList.append(thing)

        for i in range(len(phraseList)):
            if phraseList[i] in alphabet:
                phraseList[i] = alphabet[phraseList[i]]
            
        final = "".join(phraseList)
        return final

    #MORSE CODE

    #convert string to morse 
    def string_to_morse(self, phrase):
        morse = ['.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-', '-.--', '--..']
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        #get phrase from user and split into a list while making it lowercase

        string_split = list(phrase.lower())

        #removes all spaces in the new list

        for char in string_split:
            if char == " ":
                string_split.remove(char)

        #gets the index to be used to get each element from morse list, and the final list for the morse output
        index = 0
        final_morse = []

        #gets the proper index from the alphabet that is the same with the iterator and appends the same index from the morse list into the final morse output list.
        for i in string_split:
            index = alphabet.index(i)
            final_morse.append(morse[index])

        #Joins the final morse list into one string
        morse_code = " ".join(final_morse)

        return morse_code
    
    #convert morse to string
    def morse_to_string(self, phrase):
        morse = ['.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-', '-.--', '--..']
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        
        #gets the morse code from user and splits it into a list
        morse_split = phrase.split(" ")
    
        index = 0
        final_words = []
        #same as the words to morse
        for i in morse_split:
            index = morse.index(i)
            final_words.append(alphabet[index])
    
        wordsOutput = "".join(final_words)
        return wordsOutput



    #def symmetric(self, phrase, key):

    #def assymetric(self, phrase):

#OPTIONS MENU

#def options(choice):
#    print("Which encryption method would you like to use: ")
    
#NOTE: when doing the decrypt, you should only do it after phrase is encrypted, because then it will just to the reverse with the original phrase.


#Main method(runs on start)
def main():
    
    obj = Cryptography()
    
    print("What would you like to do: ")
    #functions list
    funcList = ("Caesar Cipher Encrypt", "Caear cipher Decrypt", "Hashing", "Atbash Cipher", "String to Morse", "Morse to String")
    #lists out all the functions to choose from
    for i in range(len(funcList)):
        print(str(i + 1) + ") " + funcList[i])
        
    mainOption = input("Enter the number >> ")
    
    #MUST MAKE THE NUMBER OPTIONS A STRING
    #CaesarCipherEncrypt
    if mainOption == "1":
        CCEphrase = input("Enter the phrase you want to encrypt with Caesar: ")
        CCEkey = input("Enter the key: ")
        print(obj.caesarEncrypt(CCEphrase, CCEkey))
    #CaesarCipherDecrypt
    elif mainOption == "2":
        CCDphrase = input("Enter the phrase you want to decrypt with Caesar: ")
        CCDkey = input("Enter the key: ")
        print(obj.caesarDecrypt(CCDphrase, CCDkey))
    #Hashing
    elif mainOption == "3":
        Hphrase = input("Enter the phrase you want to hash: ")
        print(obj.hashing(Hphrase))
    #AtbashCipher
    elif mainOption == "4":
        Aphrase = input("Enter the phrase you want to encrypt with atbash: ")
        print(obj.atbash(Aphrase))
    #StringtoMorse
    elif mainOption == "5":
        STMphrase = input("Enter the phrase you want to turn into morse code: ")
        print(obj.string_to_morse(STMphrase))
    #MorsetoString
    elif mainOption == "6":
        MTSphrase = input("Enter the morse you want to turn into plaintext: ")
        print(obj.morse_to_string(MTSphrase))

    
    
#Run main method on start of program
if __name__ == '__main__':
    main()



