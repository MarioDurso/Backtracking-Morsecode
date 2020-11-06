#backtracking multithreaded
import threading
#import multiprocessing
import concurrent.futures
import time




#num_thread = 0;
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

'''
def factor(value):
    factors = [0, 10000000]
    
    for i in range(1, int(value/2)):
        int(i)
        if value % i == 0:
            if(abs((int(value/i)-i)) < abs(factors[1]-factors[0])):
                factors[0] = i
                factors[1] = int(value/i)
    return factors
'''
def multi_handle_word(morse_code, word, morseLib, dictionary):
    for x in handle_word(morse_code, word, morseLib):
        if x in dictionary:
            print (x)

#MAIN

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


    # Type in an input to try it out.
    style, morsed = input().split(":")
    morse_code = morsed.strip()
    # morse_code will be the string of morse coded text(e.g., '..--.-')
    
    
    
    if style == 'Spaced Letters':
        print(handle_spaced_letters(morse_code, morseLib))
        
    elif style == 'Word':
        start_time = time.time()

        
        #mulitprocesses on each letter in the alphabet
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for x in morseLib:
                f1 = executor.submit(multi_handle_word, morse_code, [x], morseLib, dictionary)


        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
