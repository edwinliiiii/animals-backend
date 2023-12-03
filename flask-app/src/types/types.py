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
    cursor.execute('SELECT * FROM animal_type')

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

# add a new animal type to the db
@types.route('/', methods=['POST'])
def add_new_type():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    species = the_data['species']
    subSpecies = the_data['subSpecies']
    animalID = the_data['animalID']

    # Constructing the query
    query = 'insert into animal_type (species, subSpecies, animalID) values ("'
    query += species + '", "'
    query += subSpecies + '", "'
    query += str(animalID) + '")'
    print(query)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Get a certain animal type from the database based on ID
@types.route('/<animalTypeID>', methods=['GET'])
def get_type(animalTypeID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT * FROM animal_type WHERE animalTypeID={0}'.format(animalTypeID))

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

    # Update the specified animal type in the database based on animalTypeID
@types.route('/<animalTypeID>', methods=['PUT'])
def update_type(animalTypeID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    query = 'UPDATE animal_type SET '

    #construct query
    if 'species' in the_data:
        species = the_data['species']
        query += ('species = "' + species + '",')
    if 'subSpecies' in the_data:
        subSpecies = the_data['subSpecies']
        query += ('subSpecies = "' + subSpecies + '",')
    if 'animalID' in the_data:
        animalID = the_data['animalID']
        query += ('animalID = "' + str(animalID) + '",')
    if 'animalTypeID' in the_data:
        animalTypeID = the_data['animalTypeID']
        query += ('animalTypeID = "' + animalTypeID + '",')

    #remove unnecessary comma    and    update the appropriate type by animalTypeID
    query = query[0:len(query) - 1] + " WHERE animalTypeID = {0}".format(animalTypeID)

    print(query)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return jsonify({"message": "Success!"})

    # Delete a specific animal type from the database based on its animalTypeID
@types.route('/<animalTypeID>', methods=['DELETE'])
def delete_type(animalTypeID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    # use cursor to query the database for a list of products
    cursor.execute('DELETE FROM animal_type WHERE animalTypeID={0}'.format(animalTypeID))
    db.get_db().commit()
    return jsonify({"message": "Success!"}) 
