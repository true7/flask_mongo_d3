from flask import Flask, render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'world'
DBS_NAME_ISO = 'isonames'
COLLECTION_NAME = 'bank'
COLLECTION_NAME_ISO = '2to3'
FIELDS = {'project_name': True, 'countryname': True, 'countrycode': True, 'lendprojectcost': True, '_id': False}
FIELDS_ISO = {'_id': False}

@app.route("/")
def home_page():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find(projection=FIELDS)

    collection_iso = connection[DBS_NAME_ISO][COLLECTION_NAME_ISO]
    projects_iso = collection_iso.find(projection=FIELDS_ISO)

    # Make a dictionary of country codes in format --> {'2_letters_code': '3_letters_code'}
    codes = {}
    for project in projects_iso:
            codes.update(project)

    # Preparing data for a choropleth, substitute country codes.
    # For this map I have to skip 'East Asia and Pacific', 'Pacific Islands', 'Africa', 'World', 'South Asia' 
    # 'Middle East and North Africa', 'Europe and Central Asia' --> they are not countries, but the whole regions.
    # I commented out rows with these values.
    choro_data = []
    for project in projects:
        countrycode = codes[project['countrycode']]
        choro_data.append([project['project_name'], project['countryname'], countrycode, project['lendprojectcost']])
    connection.close()
    return render_template('layout.html', choro_data=choro_data)








# json format
# @app.route("/")
# def home_page():
#     connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
#     collection = connection[DBS_NAME][COLLECTION_NAME]
#     projects = collection.find(projection=FIELDS)
#     json_projects = []
#     for project in projects:
#         json_projects.append(project)
#     json_projects = json.dumps(json_projects, default=json_util.default)
#     connection.close()
#     return render_template('layout.html', json_projects=json_projects)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
