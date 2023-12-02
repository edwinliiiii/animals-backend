from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


animals = Blueprint('animals', __name__)

# Get all the animals from the database
@animals.route('/', methods=['GET'])
def get_animals():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT * FROM animal')

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

# add a new animal to the db
@animals.route('/', methods=['POST'])
def add_new_animal():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    specialRequirements = the_data['specialRequirements']
    age = the_data['age']
    gender = the_data['gender']
    price = the_data['price']
    healthStatus = the_data['healthStatus']
    behavior = the_data['behavior']
    origin = the_data['origin']
    availability = the_data['availability']
    orderID = the_data['orderID']
    supplierID = the_data['supplierID']

    # Constructing the query
    query = 'insert into animal (specialRequirements, healthStatus, behavior, origin, age, gender, price, availability, orderID, supplierID) values ("'
    query += specialRequirements + '", "'
    query += healthStatus + '", "'
    query += behavior + '", "'
    query += origin + '", '
    query += str(age) + ', '
    query += str(gender) + ', '
    query += str(price) + ', '
    query += str(availability) + ', '
    query += str(orderID) + ', '
    query += str(supplierID) + ')'
    print(query)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return jsonify({"message": "Success!"})

# Delete a specific animal from the database
@animals.route('/<animalID>', methods=['DELETE'])
def delete_animal(animalID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    # use cursor to query the database for a list of products
    cursor.execute('DELETE FROM animal WHERE animalID={0}'.format(animalID))
    db.get_db().commit()
    return jsonify({"message": "Success!"}) 

# Get a certain animal from the database based on ID
@animals.route('/<animalID>', methods=['GET'])
def get_animal(animalID):
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    cursor.execute('SELECT * FROM animal WHERE animalID={0}'.format(animalID))

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

# Update the specified animal in the database
@animals.route('/<animalID>', methods=['PUT'])
def update_animal(animalID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    query = 'UPDATE animal SET '

    #construct query
    if 'specialRequirements' in the_data:
        specialRequirements = the_data['specialRequirements']
        query += ('specialRequirements = "' + specialRequirements + '",')
    if 'healthStatus' in the_data:
        healthStatus = the_data['healthStatus']
        query += ('healthStatus = "' + healthStatus + '",')
    if 'behavior' in the_data:
        behavior = the_data['behavior']
        query += ('behavior = "' + behavior + '",')
    if 'origin' in the_data:
        origin = the_data['origin']
        query += ('origin = "' + origin + '",')
    if 'age' in the_data:
        age = the_data['age']
        query += ('age = ' + str(age) + ',')
    if 'gender' in the_data:
        gender = the_data['gender']
        query += ('gender = ' + str(gender) + ',')
    if 'price' in the_data:
        price = the_data['price']
        query += ('price = ' + str(price) + ',')
    if 'availability' in the_data:
        availability = the_data['availability']
        query += ('availability = ' + str(availability) + ',')
    if 'orderID' in the_data:
        orderID = the_data['orderID']
        query += ('orderID = ' + str(orderID) + ',')
    if 'supplierID' in the_data:
        supplierID = the_data['supplierID']
        query += ('supplierID = ' + str(supplierID) + ',')

    #remove unnecessary comma    and    update the appropriate animal by animalID
    query = query[0:len(query) - 1] + " WHERE animalID = {0}".format(animalID)

    print(query)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return jsonify({"message": "Success!"})


# Get all animals from the database based on a certain species
@animals.route('/type/<species>', methods=['GET'])
def get_animal_by_species(species):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    strSpecies = '"' + species + '"'
    # use cursor to query the database for a list of animals
    cursor.execute('SELECT * FROM animal JOIN animal_type ON animal.animalID=animal_type.animalID WHERE species={0}'.format(strSpecies))

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

# Get all animals from the database based on a certain species and subspecies
@animals.route('/type/<species>/<subSpecies>', methods=['GET'])
def get_animal_by_species_subspecies(species, subSpecies):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    strSpecies = '"' + species + '"'
    strSubSpecies = '"' + subSpecies + '"'
    # use cursor to query the database for a list of animals
    cursor.execute('SELECT * FROM animal JOIN animal_type ON animal.animalID=animal_type.animalID WHERE species={0} AND subSpecies={1}'.format(strSpecies, strSubSpecies))

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

# Get all animals from the database based on a certain origin
@animals.route('/origin/<origin>', methods=['GET'])
def get_animal_by_origin(origin):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    strOrigin = '"' + origin + '"'
    # use cursor to query the database for a list of animals
    cursor.execute('SELECT * FROM animal JOIN animal_type ON animal.animalID=animal_type.animalID WHERE origin={0}'.format(strOrigin))

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

# Get all animals from the database based on a certain availability
@animals.route('/availability/<availability>', methods=['GET'])
def get_animal_by_availability(availability):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    strAvailability = str(availability)
    # use cursor to query the database for a list of animals
    cursor.execute('SELECT * FROM animal JOIN animal_type ON animal.animalID=animal_type.animalID WHERE availability={0}'.format(strAvailability))

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
