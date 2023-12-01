from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


types = Blueprint('types', __name__)

# Get all the animal types from the database
@types.route('/', methods=['GET'])
def get_types():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT * FROM types')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

@types.route('/', methods=['POST'])
def add_new_type():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    species = the_data['species']
    subSpecies = the_data['subSpecies']
    animalID = the_data['animalID']
    animalTypeID = the_data['animalTypeID']

    # Constructing the query
    query = 'insert into type (species, subSpecies, animalID, animalTypeID) values ("'
    query += species + '", "'
    query += subSpecies + '", "'
    query += animalID + '", "'
    query += animalTypeID + '") '
    print(query)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Get a certain type from the database based on ID
@types.route('/<typeID>', methods=['GET'])
def get_type(typeID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT * FROM type WHERE typeID={0}'.format(typeID))

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)
