import time
from itertools import product
from itertools import combinations
'''
TrieNode class
'''
class TrieNode:
    def __init__(self):
        self.children = {str: TrieNode}
        self.word = []
        
#funtion I wrote to add letters to the Trie but it seems it wasnt needed for this assignment
def add_letter(root: TrieNode, new_word: str, morseLib):
    current = root
    for letter in new_word:
        if letter not in current.children:
            current.children[letter] = TrieNode()
        current = current.children[letter]
    current.word.append(handle_spaced_letters(new_word, morseLib))
    
    
'''
funtion that adds a new word to a trie tree
Parameters:
    TrieNode root: the root node of a trie triee
    str new_word: a str of morse letters seperated by a space
        to be the word added to the trietree
    dict morseLib : dictionary of with morse letter as key and english letter as value
returns: void

'''
def add_word(root: TrieNode, new_word: str, morseLib):
    current = root
    for letter in new_word.replace(" ",""):
        if letter not in current.children:
            current.children[letter] = TrieNode()
        current = current.children[letter]
    current.word.append(handle_spaced_letters(new_word, morseLib))


'''
funtion that finds a word in a trie triee
Parameters:
    TrieNode root: the root node of a trie triee
    str target: a str of morse letters representing a word you would like to search for
        in the trie tree
    dict morseLib : dictionary of with morse letter as key and english letter as value
returns: list of english words or an empty list if no words are found
'''
def find_word(root: TrieNode, target: str):
    current = root
    for letter in target:
        if letter in current.children:
            current = current.children[letter]
        else:
            return []
    
    return current.word
    

'''
helper funtion that takes an english word and converts it to a string of morse letters spererated by spaces
Parameters:
    str given: a string of letters you want to convert to morse code
    dict morseLib : dictionary of with morse letter as key and english letter as value
returns: string of morse letters sperated by spaces

'''
def word_to_morse(given: str, morseLib):
    morseWord = ""
    length = len(given)
    i = 1
    for letter in given:
        letter = letter.capitalize()
        if(i != length):
            #gets the keys from values
            morseWord = (morseWord +
                         list(morseLib.keys())[list(morseLib.values()).index(letter)]
                         + " ")
        else:
            morseWord = (morseWord +
                         list(morseLib.keys())[list(morseLib.values()).index(letter)])
        i +=1
    return morseWord
        

'''
Problem 1 funtion that takes in a string of spaced morse letters and converts it to an
    english word
Parameters:
    str morse_code: a str of morse letters seperated by a space
    dict morseLib : dictionary of with morse letter as key and english letter as value
returns: string of english letters

'''

def handle_spaced_letters(morse_code: str, morseLib):
    translation = ""
    morseLetters = morse_code.split()
    
    for x in morseLetters:
        translation = translation + morseLib[x]
    return(translation)



'''
Problem 2 funtion that finds all words from an unspaced str of morse chars
Parameters:
    str morse_code: a str of morse letters
    [str] word: an empty str to be filled with morse letters
    #side note this prob could could be a normal string to increase performence
    dict morseLib : dictionary of with morse letter as key and english letter as value
returns: a list of strings in english letters that when translated to morse code match morse_code

'''
def handle_word(morse_code: str, word: [str], morseLib):
    joinedWord = ""
    joinedWord = "".join(word)
    if(joinedWord not in morse_code):
        return []
    
    if(joinedWord == morse_code):
        translation = ""
        for x in word:
            translation = translation + morseLib[x]
        return [translation]
    else:
        possible_words = [morseLetter for morseLetter in morseLib]
        final_result = []
        for potential_word in possible_words:
            word.append(potential_word)
            result = handle_word(morse_code, word, morseLib)
            if(result != []):       
                final_result.extend(result)
            word.pop()
        return final_result
    

#part 3
'''
Problem 3 funtion that finds all words possible english substitutes for a str of spaced morse words
Parameters:
    str morse_code: a str of morse letters
    TrieNode TrieTree: the root of a trie tree
returns: NULL prints the possible combinations

'''
def handle_spaced_words(morse_code: str, TrieTree):
    #get a list of all the words in the morse code
    morse_code_list = morse_code.split()
    
    #initialize a 2darray
    twoDList = []
    
    # find all possible english substitutes for each word in the morse code
    for word in morse_code_list:    
        twoDList.append((find_word(TrieTree, word)))
    length = len(twoDList)
    
    #make all combinations
    if length == 1:
        for x in twoDList[0]:
            print(x)
            return None
    if length > 1:
        for i in range(0, length-1):
            if i == 0:
                prodList = (list(product(twoDList[i], twoDList[i+1])))
            else:
                prodList = (list(product(prodList, twoDList[i+1])))
    
    for combo in prodList:
        spaced_words = ""
        for value in combo:
            if (type(value) != str):
                for x in value:
                    spaced_words = spaced_words + x + " "
            else:
                spaced_words = spaced_words + value + " "
        print(spaced_words[:-1])
    return None

'''
funtions for prob 4
Funtion that finds the shortest sentence from a str of unspaced morse chars
Parameters:
    str morse_code: a str of morse letters
    TrieNode TrieTree: the root of a trie tree
    [str] sentence: an empty list
    dict MorseLib = key value for morse chars and english chars
returns: a list of strings with each sentence seperated by an empty string
'''


def find_all_words(morse_code, root: TrieNode, sentence: [str], morseLib):
    #initialize the length of the sentence by morse chars
    sentLen = 0
    length_mc = len(morse_code)
    
    #calculates the morse lenght of a list of english words
    for word in sentence:
        currentMorse = word_to_morse(word, morseLib).replace(" ", "")
        sentLen += len(currentMorse)
        
    #Pruning
    if(len(sentence) > 5):
        return []
    
    if(sentLen == length_mc):
        copy = sentence.copy()
        #add space to indicate end of a sentence
        copy.extend([""])
        
        #return copy to avoid poping issues
        return copy
    else:
        
        #uses helper funtion to get the rest of words that could possible come after the list of words used
        possible_next = check_rest(morse_code[sentLen:], root)
        final_result = []
        
        for x in possible_next:
            sentence.append(x)
            #add more
            result = find_all_words(morse_code, root, sentence, morseLib)
            if(result != []):
                #add in results
                final_result.extend(result)
            sentence.pop()
    #return
    return final_result


'''
funtion for prob 4
finds all the words that can be made from the starting char in a morse string
Parameters:
    str morse_code: a str of morse letters
    TrieNode TrieTree: the root of a trie tree
returns: a list of strings in english representing all the strings made from the first char

this funtion iterates through the string backwords
this results in the largest words that can be found being returned first
'''

def check_rest(morse_code, root: TrieNode):
    final_result = []
    currentIndex = 0
    length = len(morse_code)
    #keeps removing the last letter of the string to check for words
    while currentIndex > length*-1:
        if(currentIndex == 0):
            word = morse_code
        else:
            word = morse_code[:currentIndex]
        #check current string for words
        currentList = find_word(root,word)
        if (currentList != []):
            #add to final results
            final_result.extend(currentList)
        currentIndex -= 1
    #return
    return final_result


'''
funtion for prob 4
takes in the found sentences and sorts them by length and alphabeticly and prints the shortest sentences
Parameters:
    str morse_code: a str of morse letters
    TrieNode TrieTree: the root of a trie tree
    dict MorseLib = key value for morse chars and english chars
returns: void but prints the shortest sentences
'''
def handle_sentence(morse_code: str, root, morseLib):
    #get the list of strings reperesenting all the sentences
    str_sentences = find_all_words(morse_code, root, [], morseLib)
    sentence = []
    list_sentence = []
    #convert list of strings to list of list of strings
    for x in str_sentences:
        if(x == ""):
            list_sentence.append(sentence)
            sentence = []
        else:
            sentence.append(x)
    #sort the list to find the length of the shortest sentence
    sortedList = sorted( list_sentence, key=len )
    length = len(sortedList[0])
    #resort if len > 0
    if(length > 1):
        #use lambda funtion with one line for loop to break ties in possible words
        sortedList = sorted( sortedList, key = lambda x: (len(x), [x[y] for y in range(0,len(x))]))
        
    #print the sentences
    for x in sortedList:
        if(len(x) == length):
            print(print_list(x))
        else:
            break
        
'''
funtion that takes in a list of strings and converts them to a strings
as im commenting this I realized I could have just used the built in one
'''
def print_list(list_string):
    word = ""
    if(len(list_string) == 1):
        return(list_string[0])
    word = ""
    for x in list_string:
        word = word + " " + x
    return word
    
    
def main():
    morse_file = "morse.txt"
    morse_dict = "dictionary.txt"
    
#import morseLib
    with open(morse_file) as i:
        lines = i.readlines()
    morseLib = {}
    for x in lines:
        givenLine = x.split()
        curLine = []
        for element in givenLine:
            curLine.append(element.strip())
        if(curLine[0] == "1"):
            break
        morseLib[curLine[1]] = curLine[0]


#import morseDictionary
    with open(morse_dict) as i:
        lines = i.readlines()
    dictionary = []
    for x in lines:
        value = x.strip()
        dictionary.extend([value])
 
 #Establish TrieTree
    TrieTree = TrieNode()
    for word in dictionary:
        word = word_to_morse(word, morseLib)
        add_word(TrieTree, word, morseLib)
    

    # Type in an input to try it out.
    style, morsed = input().split(":")
    morse_code = morsed.strip()
    # morse_code will be the string of morse coded text(e.g., '..--.-')
    
    
    if style == 'Spaced Letters':
        print(handle_spaced_letters(morse_code, morseLib))
        
    elif style == 'Word':
        start_time = time.time()
        possible_words = handle_word(morse_code, [], morseLib)
        #print(possible_words)
        for word in possible_words:
            if (word in dictionary):
                print(word)
        print("--- %s seconds ---" % (time.time() - start_time))
        
        
        
    elif style == 'Spaced Words':
        handle_spaced_words(morse_code, TrieTree)
        
        
        
    elif style == 'Sentence':
        handle_sentence(morse_code, TrieTree, morseLib)


if __name__ == '__main__':
    main()
