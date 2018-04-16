# Text Analytics - Connectavo

This repository provides a Python implementation to serve word count, parts of speech count and sentence difference in text documents using [NLTK] and [Gensim].
It stores the data in PyMongo and delivers it over an API created in Flask.

[NLTK]: https://www.nltk.org/
[Gensim]: https://github.com/RaRe-Technologies/gensim

## Table of Contents

 - **Getting Started**
 - **API Calling**
 - **Methodologies**
 
## Getting Started

### Prerequisites

You're going to need:

 - **Python 3.5+** — In this project, [Python 3.5] was used.
 - **MongoDB 3+**
 - **pip** — Comes preinstalled with Python 3.4+
 - **vrtualenv** — `pip install virtualenv`. You can use other virtual environments as well
 - **Flask** — `pip install flask` 
 - **PyMongo** — `pip install pymongo`
 - **NLTK** — `pip install -U nltk`
 - **Gensim** — `pip install -U gensim`
 - **Numpy** — `pip install numpy`
 - **Scipy** — `pip install scipy`
 
 [Python 3.5]: https://www.python.org/downloads/release/python-354/
 
 ### Installing
 
 1. Make sure the above mentioned requirements are installed.
 2. Clone this repository.
 3. Run a mongo server with `mongod` in command line
 4. `cd Text_Analytics-Connectavo` 
 5. Run virtual environment with `connect\Scripts\activate`
 6. Run api.py with `python api.py` — This will take a few minutes to store all the data in MongoDB and will then fire up a flask server on [http://127.0.0.1:5000/]
 
 ##### Note: nltk may require some packages to be downloaded when imported. You can download it using `nltk.download(<package>)` after `import nltk`
 
 [http://127.0.0.1:5000/]: http://127.0.0.1:5000/
 
## API Calling

### Word Count

`http://127.0.0.1:5000/words` shows word count collection and links to individual word counts

![words](https://user-images.githubusercontent.com/25735076/38771176-b838989c-4037-11e8-8e9d-bfae1fa2f2f1.PNG)

`http://127.0.0.1:5000/words/<id>` shows word count of book with id where id = 1-3
 
`http://127.0.0.1:5000/words/all` shows word count of all books combined

![wordsall](https://user-images.githubusercontent.com/25735076/38771219-9ad2ee50-4038-11e8-8e65-8a10c1b50da7.PNG)

### Parts of Speech Count

`http://127.0.0.1:5000/pos` shows noun & verb count collection and links to individual pos counts

![pos](https://user-images.githubusercontent.com/25735076/38771256-523da4a4-4039-11e8-9e40-83acf5cee1d5.PNG)

`http://127.0.0.1:5000/words/<id>` shows noun and verb count of book with id where id = 1-3
 
`http://127.0.0.1:5000/words/all` shows noun and verb count of all books combined

![posall](https://user-images.githubusercontent.com/25735076/38771272-a30eee38-4039-11e8-927b-48a6cbef87ec.PNG)

### Sentence Difference

`http://127.0.0.1:5000/top10/<id>` shows top 10 most similar and dissimilar sentences and their score in book id where id = 1-3

![similar](https://user-images.githubusercontent.com/25735076/38771317-8a95b9f8-403a-11e8-9948-304efc211df4.PNG)

Alternatively, you can also choose book from the home page for this task.
At home page: enter a sentence in text box and choose book, and it will show you most similar and dissimlar sentence in that book

![similar1](https://user-images.githubusercontent.com/25735076/38771664-5a8f1992-4040-11e8-966d-2de5ff25b452.PNG)

## Methodologies

### Word Count

Lines read from book is tokenized into words, where each word is treated in lower case and all the special characters and numbers are removed from words using `''.join(filter(str.isalpha, word))`. These words are then stored in python dictionaries with word as key and its occurence as value.
Even though this tokenization is fast and simpler but, it converts words like no-one and i.e to noone and ie.
To treat this, another option is to remove special characters only before and after the words and not from the middle. The only downside to this option is that it will take a lot more time to run.

### PoS Count

NLTK's sentence tokenizer `nltk.sent_tokenize(lines)` is used to tokenize whole document. Each sentence is then tokenized into words where every word is treated the same way mentioned in Word Count. `nltk.pos_tag(words)` returns a word and its tag that specifies the part of speech. To find out about the meaning of nltk's tags, view this [list]

[list]: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

### Sentence Difference

Sentense tokenization was again done using nltk. A bag of words containing the word and its occurence in whole document is made for each word in a sentence. For each 'sentence's bag of words'/corpus a tf-idf is generated. tf-idf is Term Frequency - Inverse Document Frequency where tf is the occurence of word in a document and idf scales the value by how rare the word is in the corpus. This way, the word 'the' even though it appears a lot of times but because its not rare, it doesnt add any value.

I followed this [step-by-step tutorial] on gensim.

[step-by-step tutorial]: https://www.oreilly.com/learning/how-do-i-compare-document-similarity-using-python

Now, to find top 10 similar/unique sentences, a `tf-idf` is created for every sentence and it is sent to the similarity corpus of all other sentences. This returns an array of similarity fraction with the given sentence where, each fraction's location corresponds to the location of sentence in the sentence list. A sentence's score is computed by summing up all these fractions.

#### Why not NLTK's WordNet for Sentence Difference?
I tried using WordNet but in nltk, `path_similarity` sometimes returns None if there’s no path between 2 synsets. To handle this, we'll have to filter out those None values, but this does not give a good result. This issue has reported [here] in the comments section

[here]: http://nlpforhackers.io/wordnet-sentence-similarity/
