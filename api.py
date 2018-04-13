from flask import Flask, render_template, request
from pymongo import MongoClient
from collections import Counter
import json
import main
from bson import Binary, Code
from bson.json_util import dumps

client = MongoClient('localhost:27017')
db = client.ConnectavoDB

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sentenceDifference", methods=['GET'])
def sentenceDifference():
    book = request.args.get("book")
    sentence =request.args.get("sentence")
    most_similar, least_similar = main.sentenceDifference(book, sentence)
    print (most_similar, "\n", least_similar)
    return render_template ("sentenceDifference.html", book=book[0], sentence=sentence, most=most_similar, least=least_similar)


@app.route("/top10/<book>")
def top10(book=None):
    if book==None:
        return "Enter book id"
    sentenceCollection = db.sentenceCollection
    doc = sentenceCollection.find_one({"_id": book[0]})
    return render_template("top10.html", similiar=doc["similar"], dissimilar=doc["dissimilar"], book=book[0])

@app.route("/words")
@app.route("/words/")
@app.route("/words/<book>")
def words(book=None):
    if book==None:
        data = db.wordCollection.find()
        wordColl = dict()
        for doc in data:
            wordColl[doc["_id"]] = json.loads(doc["words"])

        return render_template("wordCollection.html", collection=wordColl)

    elif book=='all':
        data1 = db.wordCollection.find_one({"_id":"1"})
        data2 = db.wordCollection.find_one({"_id":"2"})
        data3 = db.wordCollection.find_one({"_id":"3"})

        words1 = json.loads(data1["words"])
        words2 = json.loads(data2["words"])
        words3 = json.loads(data3["words"])

        allWords = dict(Counter(words1) + Counter(words2) + Counter(words3))
        return render_template("words.html", words=allWords, book="all")

    else:
        data=db.wordCollection.find_one({"_id":book})
        if (data==None):
            return "No such book available"
        words=json.loads(data["words"])
        return render_template("words.html", words=words, book=book)


@app.route("/pos")
@app.route("/pos/")
@app.route("/pos/<book>")
def pos(book=None):
    if book==None:
        data = db.posCollection.find()
        nounColl = dict()
        verbColl = dict()
        nounCount = dict()
        verbCount = dict()
        for doc in data:
            nounColl[doc["_id"]] = json.loads(doc["nouns"])
            verbColl[doc["_id"]] = json.loads(doc["verbs"])
            nounCount[doc["_id"]] = json.loads(doc["nounCount"])
            verbCount[doc["_id"]] = json.loads(doc["verbCount"])

        return render_template("posCollection.html", nouns=nounColl, verbs=verbColl, nounCount=nounCount, verbCount=verbCount)

    elif book == 'all':
        data1 = db.posCollection.find_one({"_id": "1"})
        data2 = db.posCollection.find_one({"_id": "2"})
        data3 = db.posCollection.find_one({"_id": "3"})

        nouns1 = json.loads(data1["nouns"])
        nouns2 = json.loads(data2["nouns"])
        nouns3 = json.loads(data3["nouns"])
        verbs1 = json.loads(data1["verbs"])
        verbs2 = json.loads(data2["verbs"])
        verbs3 = json.loads(data3["verbs"])

        allNouns = dict(Counter(nouns1) + Counter(nouns2) + Counter(nouns3))
        allVerbs = dict(Counter(verbs1) + Counter(verbs2) + Counter(verbs3))
        nounCount = sum(allNouns.values())  # sums all noun values
        verbCount = sum(allVerbs.values())  # sums all verb values

        return render_template("pos.html", nouns=allNouns, verbs=allVerbs, nounCount=nounCount, verbCount=verbCount,
                               book="all")

    else:
        data=db.posCollection.find_one({"_id":book})
        if (data==None):
            return "No such book available"
        nouns = json.loads(data["nouns"])
        verbs = json.loads(data["verbs"])
        nounCount = json.loads(data["nounCount"])
        verbCount = json.loads(data["verbCount"])
        return render_template("pos.html", nouns=nouns, verbs=verbs, nounCount=nounCount, verbCount=verbCount, book=book)


if __name__ == '__main__':
    app.run()
