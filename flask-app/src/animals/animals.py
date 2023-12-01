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