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
