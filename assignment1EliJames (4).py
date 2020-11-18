"""
assignment1EliJames.py is a program that calculates the evaluation, activity and potency of words in text files by using the known scores of these words from the Osgood Wordse.
This program was written by Elijah James, and includes methods written by the instructors of the course. 
Last Modified on April 10th, 2020
"""
#note: on the forum, Prof Allison clarified that a few seconds of run time lag is acceptable, and that file names can be hard coded into the script without grade penalty
#to experiment with other text files, change 'PoliticalSpeech.txt' to your file name of choice, and be sure to have the file saved in the same place as this .py file

import nltk

"""
Importing the necessary NLTK libraries and modules.
"""
from nltk.tag import StanfordPOSTagger
from nltk.corpus import wordnet
from nltk import pos_tag, word_tokenize
from nltk.corpus import words
from nltk.tokenize import word_tokenize



"""
To identify the part-of-speech of the words retrieved from
Word2vec, we used the conditional frequency feature of the NLTK module
which returns a frequency-ordered list of the possible parts of speech associated
with all of the English words that are found in the Brown Corpus. Our sys-
tem uses the Brown Corpus to generate the frequency-ordered list because
of the fact that the words contained in the Brown Corpus are annotated with
part-of-speech tags.
"""

wordtags = nltk.ConditionalFreqDist((w.lower(), t) 
        for w, t in nltk.corpus.brown.tagged_words(tagset="universal"))

#This is a function that accepts a string as a parameter and determines what part of speech the word is. Only returns the part-of-speech of words that are adjectives, adverbs or nouns
def findPOS(word):

    """
    This is a function that accepts a word as its parameter and returns the part-of-speech of the word.
    The function considers adjectives, adverbs and nouns.
    """
	
    lisPOS = list(wordtags[word])
    if "ADJ" in lisPOS:
        return "ADJECTIVE"
    if "ADV" in lisPOS:
        return "ADVERB"
    if "NOUN" in lisPOS:
        return "NOUN"
    

#this function accepts a file path as a parameter, reads the file, and returns the file
def readFile(filename):

    """
    This is a function that accepts a path to a file as its parameter, reads in and returns the file
    """
    speechFile = open(filename, "r")
    speech = speechFile.read()
    speechFile.close()
    return speech


#this function accepts a file as a parameter and returns an array with each index holding a word from the original file 
def getWords(speech): 
    """
    This is a function that segments the words in a document
    """
    return speech.split()


#this function creates an array that holds dictioaries. Each dictionary stores a word, and its respective EAP values. 
def prepareSemanticDifferential():

    """
    This is a function that reads in the EPA values from the Osgood wordlist and stores the values in 
    a Python dictionary.
    """
	
    filename = ("OsgoodOriginal.csv") 
    fileIn = open(filename, 'r')
    allData = []
    line = fileIn.readline()
    while line != "":
        line = fileIn.readline().strip()
        if line != "":
            values = line.split(',')
            wordData = {}
            wordData['word'] = str(values[0])
            wordData['evaluation'] = float(values[1])
            wordData['activity'] = float(values[2])
            wordData['potency'] = float(values[3])
            allData.append(wordData)
    fileIn.close()
    return allData


#this function accepts an array of text and creates a new array with each index being identical to the inputted array, except all puntuation has been stripped from the words at each index. 
def cleanWords(arrayOfText):
    cleanArray = []
    for word in arrayOfText: #for each word in arrayOfText, removes the punctuation and makes in lower case, as to make the funciton case-insensitive, then stores the cleaned word in a list
        word = word.strip(".,'?;:")
        word = word.lower()
        cleanArray.append(word)
    return cleanArray  


"""
Finds the EPA values of a text file, by turning that text file into a list of words, iteerating through the list, searching the OSgood Wordlist
for each word and adding the word's EPA values to their respective counters. Outputs the final EPA values of all the text. 
"""
def calculateSD():

    """
    This is the function that you need to write. This function will calculate the evaluation, activity and 
    potency levels of the text. You will need to use all of provided functions findPOS(), readFile(), 
    getWords() and prepareSemanticDifferential() in your solution. 
    """
    evaluationSum, activitySum, potencySum = 0, 0, 0 #creates the variables that store the running sums of evaluation, activity and potency respectively
    arrayOfDictionaries = prepareSemanticDifferential() #reads the EPA values from the Osgood wordlist, and fills a dictionary with them. This is how the script knows to rate the EPA values of following text files.
    
    #This is the portion of the program that accepts new text files
    
    speech = readFile('PoliticalSpeech.txt')        #stores obama's speech to a variable called speech, using the readFile method
    speechArray = getWords(speech)      #turns that paragraph into an array with an index for each word, by calling the getWords method
    speechArrayClean = cleanWords(speechArray)      #uses the cleanWords method to remove punctuation and make it case insensitive
    
    #turns the Osgood wordlist into a list of all the words, without their values, to be used as a check for whether the word in the speechArrayClean list is in the Osgood Wordlist
    possibleWords = []
    for i in range(len(arrayOfDictionaries)):
        whichDictionary = arrayOfDictionaries[i]
        possibleWords.append(whichDictionary['word'])
    
    #Iterates through the osgood wordlist. If the word from the wordlist is in the speech, add that words EPA values to the running counters
    for word in range(len(possibleWords)): #goes through the array that just holds the words from the Osgood wordlist
        currentDictionary = arrayOfDictionaries[word] #stores which dictioary in the wordlist we're using in this iteration, which is to say which word we are checking for and the values it holds
        if findPOS(currentDictionary['word']) == "ADJECTIVE" or findPOS(currentDictionary['word']) == "ADVERB":
            if currentDictionary['word'] in speechArrayClean:
                #if the word is an adj/adv and is in the speech, it's EPA values are added to the counters
                evaluationSum+=currentDictionary['evaluation']
                activitySum+=currentDictionary['activity']
                potencySum+=currentDictionary['potency']
    print(f"The evaluation sum of the text file is: {evaluationSum}, the activity sum of the text file is: {activitySum}, The Potency sum of the text file is: {potencySum}")



#creates the countAdjectives method which loads the text file, puts its words into a list in lowercase form, the iterates through the list, passing it through findPOS to check if its an adjectiv
def countAdjectives():
    textAdj = readFile('PoliticalSpeech.txt')#stores obama's speech to a variable called text
    textAdj = textAdj.lower()
    textArrayAdj = getWords(textAdj) #turns that paragraph into an array with an index for each word
    #print(textArrayAdj)
    numAdjectives = 0
    for i in range(len(textArrayAdj)):
        if findPOS(textArrayAdj[i]) == "ADJECTIVE":
            numAdjectives+=1
            i+=1
        else:
            i+=1
    return numAdjectives


 #does the same thing as countAdjectives, except checks if its an adverb, and increases the adverb counter accordingly   
def countAdverbs():
    textAdv = readFile('PoliticalSpeech.txt')#stores obama's speech to a variable called text
    textArrayAdv = getWords(textAdv) #turns that paragraph into an array with an index for each word
    numAdverbs = 0
    for i in range(len(textArrayAdv)):
        if findPOS(textArrayAdv[i]) == "ADVERB":
            numAdverbs+=1
            i+=1
        else:
            i+=1
    return numAdverbs


#creates a list of all the words that occur at least once in the Political speech text file
def getUniqueWords():
    textUnique = readFile('PoliticalSpeech.txt')
    textUnique = textUnique.lower()# makes the function case insensitive
    textArrayUnique = getWords(textUnique)
    uniqueWords = [] #empty list to which I add the words
    uniqueWords.append(textArrayUnique[0]) #no matter what, the first word in the text file is unique 
    
    #populates the list with the unique words. If the word is already in the list, go to the next word. If not, add the word to the list, and go to the next word.
    for i in range(len(textArrayUnique)):
        
        if textArrayUnique[i] in uniqueWords:
            i+=1 #go to next word, because the word is already in the list of unique words
        else: 
            uniqueWords.append(textArrayUnique[i])
            i+=1
    return uniqueWords


#creates a dictionary that tracks the number of times each unique word occurs in the political speech text file
def countWords():
    textUnique = readFile('PoliticalSpeech.txt')
    textUnique = textUnique.lower()# makes the function case insensitive
    textArrayUnique = getWords(textUnique)
    uniqueWords = getUniqueWords()
    uniqueWordCount = {}#creates the empty dictionary to which the words and their frequencies will be added
    #popoulates the dictionary with all the unique words, and starts their frequency counters at 0
    for word in uniqueWords:
        uniqueWordCount[word]=0
    #adds 1 to the frequency of a word each time it shows up in the array holding the text from the political speech file. x is just a program counter
    for x in textArrayUnique:
        uniqueWordCount[x]+=1

    return uniqueWordCount


#main method where the magic happens. Finds EPA values, the nmumber of adjectives, adverbs, and which words are unique and frequent they are
def main():
    calculateSD()
    numAdjectives = countAdjectives()
    numAdverbs = countAdverbs()
    uniqeWordCount = countWords()
    uniqueWords = getUniqueWords()
    print(f"The number of adjectives in this text file is: {numAdjectives} ")
    print(f"The number of adverbs in this text file is: {numAdverbs}")
    print("The unique words in this text file are: ", uniqueWords)
    print("The unique words were used this many times each: ", uniqeWordCount)
main()