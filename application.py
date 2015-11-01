from flask import Flask, render_template, request
import sys
import json
import pymongo
from bson import json_util
from bson.json_util import dumps
from credens import *


# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username


FIELDS = {'school_state': True, 'resource_type': True, 'poverty_level': True, 'date_posted': True, 'total_donations': True, '_id': False}

# EB looks for an 'application' callable by default.
application = Flask(__name__)
#application = app;
#connect to mongolab -- all database credentials in a 'credens' file


@application.route('/')
def index():
    return render_template("index.html")


@application.route('/viewdb') #view the entire json file
def viewdbfile():
    connection = pymongo.MongoClient(MONGODB_URI)
    db = connection[DBS_NAME][COLLECTION_NAME] #which database and which collection to use goes here
    results = db.find(limit=50000)
    json_projects = []
    if results:
        for result in results:
            json_projects.append(result)
        json_projects = json.dumps(json_projects, default=json_util.default)
        connection.close()
        return json_projects
    else:
        return 'file too big'
    


'''
@application.route('/files/read')
def readingFile():
    file_name = application.send_static_file('finalFile.json')
    if file_name:
        return file_name
    return 'No file presenttt..'
'''

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #app.debug = True
    application.run()

