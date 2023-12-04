from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


customers = Blueprint('customers', __name__)

# Get all the customers from the database
@customers.route('/', methods=['GET'])
def get_customers():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of customers
    cursor.execute('SELECT * FROM customer')

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

# add a new customer to the db
@customers.route('/', methods=['POST'])
def add_new_customer():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    firstName = the_data['firstName']
    lastName = the_data['lastName']
    cellPhone = the_data['cellPhone']
    homePhone = the_data['homePhone']
    email = the_data['email']
    street = the_data['street']
    city = the_data['city']
    state = the_data['state']
    zip = the_data['zip']
    profileText = the_data['profileText']

    if firstName is None:
        return jsonify({"message": "Error: firstName is null"}), 400
    if lastName is None:
        return jsonify({"message": "Error: lastName is null"}), 400
    if cellPhone is None:
        return jsonify({"message": "Error: cellPhone is null"}), 400
    if homePhone is None:
        return jsonify({"message": "Error: homePhone is null"}), 400
    if email is None:
        return jsonify({"message": "Error: email is null"}), 400
    if street is None:
        return jsonify({"message": "Error: street is null"}), 400
    if city is None:
        return jsonify({"message": "Error: city is null"}), 400
    if state is None:
        return jsonify({"message": "Error: state is null"}), 400
    if zip is None:
        return jsonify({"message": "Error: zip is null"}), 400
    if profileText is None:
        return jsonify({"message": "Error: profileText is null"}), 400

    # Constructing the query
    query = 'insert into customer (firstName, lastName, cellPhone, homePhone, email, street, city, state, zip, profileText) values ("'
    query += firstName + '", "'
    query += lastName + '", "'
    query += cellPhone + '", "'
    query += homePhone + '", "'
    query += email + '", "'
    query += street + '", "'
    query += city + '", "'
    query += state + '", '
    query += str(zip) + ', "'
    query += profileText + '")'
    print(query)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Get a certain customer from the database based on ID
@customers.route('/<customerID>', methods=['GET'])
def get_type(customerID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT * FROM customer WHERE customerID={0}'.format(customerID))

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

    # Delete a specific customer from the database based on its customerID
@customers.route('/<customerID>', methods=['DELETE'])
def delete_type(customerID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    # use cursor to query the database for a list of customers
    cursor.execute('DELETE FROM animal_type WHERE animalTypeID={0}'.format(customerID))
    db.get_db().commit()
    return jsonify({"message": "Success!"}) 
