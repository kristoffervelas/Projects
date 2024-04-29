#turn letters into morse code and maybe vice versa

morse = ['.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-', '-.--', '--..']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


#convert morse to string
def to_string():
    print("separate the morse code by spaces")
    #gets the morse code from user and splits it into a list
    get_morse = str(input("Enter the morse code you want to translate into words: "))
    morse_split = get_morse.split(" ")
    
    index = 0
    final_words = []
    #same as the words to morse
    for i in morse_split:
        index = morse.index(i)
        final_words.append(alphabet[index])
    
    wordsOutput = " ".join(final_words)
    print(wordsOutput)

#convert string to morse 
def to_morse():
    #get phrase from user and split into a list while making it lowercase

    get_string = str(input("Enter the phrase you want to translate into morse code: "))
    string_split = list(get_string.lower())

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
        final_morse.append(morse[index] + " ")

    #Joins the final morse list into one string
    morse_code = " ".join(final_morse)

    print(morse_code)

#morse to string or string to morse ask
ask_option = str(input("What do you want to do (morse to words: press 1)(words to morse: press 2) >> "))

if ask_option == "1":
    to_string()
elif ask_option == "2":
    to_morse()
else:
    print("Cannot understand.")
    ask_option = str(input("What do you want to do (morse to words: press 1)(words to morse: press 2) >> "))

"""
problem: find a way to get every character in the string and somehow get the index of that in the alphabet and the morse list

PROBABLE PROBLEM FIX

index = 0
final_morse = []


#first make everything lower case in case theres caps
for i in string_split:
    index = alphabet.getindex(i) something like this
    final_morse.append(morse[index])

then join the morse list
""" 

#try to implement this into an app
