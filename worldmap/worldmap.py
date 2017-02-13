from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'world'
mongo = PyMongo(app)

@app.route('/')
def home_page():
    result = []
    for row in mongo.db.bank.find():
        result.append(row)
    return render_template('layout.html', result=result)



    # pipeline = [
    # {'$group': {'_id': { 'city': '$city', 'state':  '$state'}, 'totalPop': { '$sum': '$pop' } } },
    # {'$match': {'totalPop': { '$gte' : 2000000 } } },
    # {'$sort': {'totalPop': 1}},
    # ]
    # qs = mongo.db.code.aggregate(pipeline=pipeline, useCursor=False)