from flask import Flask, render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'world'
COLLECTION_NAME = 'bank'
FIELDS = {'project_name': True, 'countryname': True, 'lendprojectcost': True, '_id': False}

@app.route("/")
def home_page():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find(projection=FIELDS)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return render_template('layout.html', json_projects=json_projects)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
