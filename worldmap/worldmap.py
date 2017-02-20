from flask import Flask, render_template
from pymongo import MongoClient
# import json
# from bson import json_util
# from bson.json_util import dumps

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

    # Make a dictionary of country codes in format --> {'2_letters_code': '3_letters_code'}.
    codes = {}
    for project in projects_iso:
            codes.update(project)

    # Preparing data for a choropleth, substitute country codes.
    # For this map I had to skip 'East Asia and Pacific', 'Pacific Islands', 'Africa', 'World', 'South Asia' 
    # 'Middle East and North Africa', 'Europe and Central Asia' --> they are not countries, but the whole regions.
    # I commented out rows with these values in source JSON file.

    # Count all projects for each country, costs and result cost. After that we don't have more than one row 
    # for one country and data don't override themselves.
    count = {}
    for item in projects:
        countrycode = codes[item['countrycode']]
        if not count.get(countrycode) == None:

            # I've decided wrtite code this way to avoid nested lists.
            project_names = count[countrycode][0]
            project_names += '; ' + item['project_name']
            
            result = count[countrycode][4]
            result += item['lendprojectcost']

            costs = count[countrycode][3]
            costs += '; ' + str(item['lendprojectcost'])

            data = [project_names, item['countryname'], countrycode, costs, result]
            count.update({countrycode: data})
        else:
            result = item['lendprojectcost']
            count[countrycode] = [item['project_name'], item['countryname'], countrycode, str(item['lendprojectcost']), result]

    # Normalize data for choropleth.
    choropleth_data = []
    for key, val in count.items():
        lendprojectcost = val[3].split(';')
        project_name = val[0].split(';')

        projects_and_costs = []
        for line in range(len(lendprojectcost)):
            string = ' <strong>Project name:</strong> ' + project_name[line] + ', <strong>cost:</strong> ' + lendprojectcost[line]
            projects_and_costs.append(string)

        data = [val[2], projects_and_costs, val[1], val[4]]
        choropleth_data.append(data)

    connection.close()
    return render_template('layout.html', choropleth_data=choropleth_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)





# DON'T MENTION IT:
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
