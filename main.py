import nltk
from pymongo import MongoClient
import json
import gensim
import operator

client = MongoClient('localhost', 27017)
db = client.ConnectavoDB


def getWordCount (book):
      
    words = dict()
    for line in open('Ebooks/' + book, 'r', encoding="ISO-8859-1"):
        if line != "\n":
            line = line.rstrip('\n')        #strip \n from each non-empty line
            for word in line.split(" "):
                word = word.lower()         #convert to lower-case
                word = ''.join(filter(str.isalpha, word))       #remove special characters & numbers
                if word != "":          #ignore empty words
                    if word in words:
                        words[word] += 1
                    else:
                        words[word] = 1
    return words


def getPoS (book):

    nouns = dict()
    verbs = dict()
    file = open('Ebooks/' + book, 'r', encoding="ISO-8859-1")
    lines = file.read()
    sentences = nltk.sent_tokenize(lines)       #get a list of sentences
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        for word, pos in nltk.pos_tag(words):
            word = word.lower()
            word = ''.join(filter(str.isalpha, word))   #remove special characters & numbers
            if word != '':                #ignore empty words
                if pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS':
                    if word in nouns:
                        nouns[word] += 1
                    else:
                        nouns[word] = 1
                elif pos == 'VB' or pos == 'VBD' or pos == 'VBG' or pos == 'VBN' or pos == 'VBP' or pos == 'VBZ':
                    if word in verbs:
                        verbs[word] += 1
                    else:
                        verbs[word] = 1
            nounCount = sum(nouns.values())  # sums all noun values
            verbCount = sum(verbs.values())  # sums all verb values
    return nouns, verbs, nounCount, verbCount


def storeWordCount ():

    wordCollection = db.wordCollection

    if wordCollection.find_one({"_id":"1"}) == None:       #check if book 1's word count not available in db
        print ("Storing Word count of book 1")
        wordCount1 = getWordCount("1-Ulysses.txt")
        wordCollection.insert({
            "_id": "1",
            "words": json.dumps(wordCount1)
        })
    else:
        print ("Word Count of book 1 already available")
    if wordCollection.find_one({"_id": "2"}) == None:
        print("Storing Word count of book 2")
        wordCount2 = getWordCount("2-Leonardo.txt")
        wordCollection.insert({
            "_id": "2",
            "words": json.dumps(wordCount2)
        })
    else:
        print ("Word Count of book 2 already available")
    if wordCollection.find_one({"_id": "3"}) == None:
        print("Storing Word count of book 3")
        wordCount3 = getWordCount("3-Science.txt")
        wordCollection.insert({
            "_id": "3",
            "words": json.dumps(wordCount3)
        })
        print("Word Count data stored")
    else:
        print ("Word Count of book 3 already available")


def storePoS ():

    posCollection = db.posCollection

    if posCollection.find_one({"_id":"1"}) == None:         #check if book 1's pos count not available in db
        print ("Storing PoS count of book 1")
        nouns1, verbs1, nounCount1, verbCount1 = getPoS ("1-Ulysses.txt")
        posCollection.insert({
            "_id": "1",
            "nouns": json.dumps(nouns1),
            "verbs": json.dumps(verbs1),
            "nounCount": json.dumps(nounCount1),
            "verbCount": json.dumps(verbCount1)
        })
    else:
        print ("PoS Count of book 1 already available")
    if posCollection.find_one({"_id": "2"}) == None:
        print("Storing PoS count of book 2")
        nouns2, verbs2, nounCount2, verbCount2 = getPoS("2-Leonardo.txt")
        posCollection.insert({
            "_id": "2",
            "nouns": json.dumps(nouns2),
            "verbs": json.dumps(verbs2),
            "nounCount": json.dumps(nounCount2),
            "verbCount": json.dumps(verbCount2)
        })
    else:
        print ("PoS Count of book 2 already available")
    if posCollection.find_one({"_id": "3"}) == None:
        print("Storing PoS count of book 3")
        nouns3, verbs3, nounCount3, verbCount3 = getPoS("3-Science.txt")
        posCollection.insert({
            "_id": "3",
            "nouns": json.dumps(nouns3),
            "verbs": json.dumps(verbs3),
            "nounCount": json.dumps(nounCount3),
            "verbCount": json.dumps(verbCount3)
        })
    else:
        print("PoS Count of book 3 already available")


def sentenceDifference(book, sentence):         # for most similar & dissimilar sentence
    file = open('Ebooks/' + book + '.txt', 'r', encoding="ISO-8859-1")
    lines = file.read()
    sentences = nltk.sent_tokenize(lines)  # get a list of sentences

    gen_docs = [[''.join(filter(str.isalpha, w.lower())) for w in nltk.word_tokenize(text)]
                for text in sentences]      #a list of list containing words in each sentence

    dictionary = gensim.corpora.Dictionary(gen_docs)    #converts list of list to corpora dictionary

    """A corpus is a list of bags of words. A bag-of-words representation for a document just lists the number of times 
    each word occurs in the document."""

    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]

    """tf-idf = Term Frequency - Inverse Document Frequency. Term frequency is how often the word shows up 
    in the document and inverse document fequency scales the value by how rare the word is in the corpus."""

    tf_idf = gensim.models.TfidfModel(corpus)       #returns a model with # of sentences and # of tokens

    sims = gensim.similarities.Similarity('Ebooks/', tf_idf[corpus], num_features=len(dictionary))

    query_doc = [''.join(filter(str.isalpha, w.lower())) for w in nltk.word_tokenize(sentence)]     #converting given sentence to a tf_idf
    query_doc_bow = dictionary.doc2bow(query_doc)
    query_doc_tf_idf = tf_idf[query_doc_bow]

    similar_index, maxScore = max(enumerate(sims[query_doc_tf_idf]), key=operator.itemgetter(1))       #returns index & score of most similar sentence
    dissimilar_index, minScore = min(enumerate(sims[query_doc_tf_idf]), key=operator.itemgetter(1))   #returns index & score of least similar sentence

    return sentences[similar_index], sentences[dissimilar_index]


def allSenteceDifferences(book):        # for top 10 most unique sentences
    wordCollection = db.wordCollection

    file = open('Ebooks/' + book, 'r', encoding="ISO-8859-1")
    lines = file.read()
    sentences = nltk.sent_tokenize(lines)  # get a list of sentences

    gen_docs = [[''.join(filter(str.isalpha, w.lower())) for w in nltk.word_tokenize(text)]
                for text in sentences]  # a list of list containing words in each sentence

    dictionary = gensim.corpora.Dictionary(gen_docs)  # converts list of list to corpora dictionary

    """A corpus is a list of bags of words. A bag-of-words representation for a document just lists the number of times 
    each word occurs in the document."""

    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]

    """tf-idf = Term Frequency - Inverse Document Frequency. Term frequency is how often the word shows up 
    in the document and inverse document fequency scales the value by how rare the word is in the corpus."""

    tf_idf = gensim.models.TfidfModel(corpus)  # returns a model with # of sentences and # of tokens

    sims = gensim.similarities.Similarity('Ebooks/', tf_idf[corpus], num_features=len(dictionary))

    top10 = dict();
    for sentence in sentences:
        query_doc = [''.join(filter(str.isalpha, (w.lower()))) for w in
                     nltk.word_tokenize(sentence)]       # a list of list containing words in each sentence
        if len(query_doc)>3:
            query_doc_bow = dictionary.doc2bow(query_doc)
            query_doc_tf_idf = tf_idf[query_doc_bow]
            score = sum(sims[query_doc_tf_idf])
            if score != 0:
                top10[sentence] = sum(sims[query_doc_tf_idf])

    top10 = sorted(top10.items(), key=operator.itemgetter(1))
    topSimilar = top10[-10:]
    topDissimilar = top10[:10]

    return topSimilar, topDissimilar


def storeAllSenteceDifferences():
    sentenceCollection = db.sentenceCollection

    if sentenceCollection.find_one({"_id": "1"}) == None:
        print ("Storing sentence difference of book 1")
        similar, dissimilar = allSenteceDifferences("1-Ulysses.txt")
        sentenceCollection.insert({
            "_id": "1", "similar": similar, "dissimilar": dissimilar})

    if sentenceCollection.find_one({"_id": "2"}) == None:
        print ("Storing sentence difference of book 2")
        similar, dissimilar = allSenteceDifferences("2-Leonardo.txt")
        sentenceCollection.insert({
            "_id": "2", "similar": similar, "dissimilar": dissimilar})

    if sentenceCollection.find_one({"_id": "3"}) == None:
        print ("Storing sentence difference of book 3")
        similar, dissimilar = allSenteceDifferences("3-Science.txt")
        sentenceCollection.insert({
            "_id": "3", "similar": similar, "dissimilar": dissimilar})

    print("Sentence difference stored")


storeWordCount()
storePoS()
storeAllSenteceDifferences()

