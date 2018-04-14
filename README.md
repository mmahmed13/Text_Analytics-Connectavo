# Text Analytics - Connectavo

This repository provides a Python implementation to serve word count, parts of speech count and sentence difference in text documents using [NLTK] and [Gensim].
It stores the data in PyMongo and delivers it over an API created in Flask.

[NLTK]: https://www.nltk.org/
[Gensim]: https://github.com/RaRe-Technologies/gensim

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
 6. Run api.py with `python api.py` — This will fire up a flask server on [http://127.0.0.1:5000/]
 
 Note: nltk may require some packages to be downloaded when imported. You can download it using `nltk.download(<package>)` after `import nltk`
 
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

`http://127.0.0.1:5000/top10/<id>` shows top 10 most similar and dissimilar sentences in book id where id = 1-3

![similar](https://user-images.githubusercontent.com/25735076/38771317-8a95b9f8-403a-11e8-9948-304efc211df4.PNG)

Alternatively, you can also choose book from the home page for this task.
At home page: enter a sentence in text box and choose book, and it will show you most similar and dissimlar sentence in that book

![similar1](https://user-images.githubusercontent.com/25735076/38771378-9fbc4288-403b-11e8-89b0-c2c0a1b596f5.PNG)

