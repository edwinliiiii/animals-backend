from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


suppliers = Blueprint('suppliers', __name__)

# Get all the suppliers from the database
@suppliers.route('/', methods=['GET'])
def get_suppliers():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of suppliers
    cursor.execute('SELECT * FROM animal_supplier')

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

# add a new supplier to the db
@suppliers.route('/', methods=['POST'])
def add_new_supplier():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    firstName = the_data['firstName']
    lastName = the_data['lastName']
    phone = the_data['phone']
    email = the_data['email']
    company = the_data['company']
    city = the_data['city']
    state = the_data['state']
    country = the_data['country']
    contactLink = the_data['contactLink']
    countSupplied = the_data['countSupplied']
    profileText = the_data['profileText']

    # Constructing the query
    query = 'insert into animal_supplier (firstName, lastName, phone, email, company, city, state, country, contactLink, countSupplied, profileText) values ("'
    query += firstName + '", "'
    query += lastName + '", "'
    query += phone + '", "'
    query += email + '", "'
    query += company + '", "'
    query += city + '", "'
    query += state + '", "'
    query += country + '", "'
    query += contactLink + '", '
    query += str(countSupplied) + ', "'
    query += profileText + '")'
    print(query)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Get a certain supplier from the database based on ID
@suppliers.route('/<supplierID>', methods=['GET'])
def get_supplier(supplierID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT * FROM animal_supplier WHERE supplierID={0}'.format(supplierID))

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

    # Update the specified supplier in the database based on supplierID
@suppliers.route('/<supplierID>', methods=['PUT'])
def update_supplier(supplierID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    query = 'UPDATE animal_supplier SET '

    #construct query
    if 'firstName' in the_data:
        firstName = the_data['firstName']
        query += ('firstName = "' + firstName + '",')
    if 'lastName' in the_data:
        lastName = the_data['lastName']
        query += ('lastName = "' + lastName + '",')
    if 'phone' in the_data:
        phone = the_data['phone']
        query += ('phone = "' + phone + '",')
    if 'email' in the_data:
        email = the_data['email']
        query += ('email = "' + email + '",')
    if 'company' in the_data:
        company = the_data['company']
        query += ('company = "' + company + '",')
    if 'city' in the_data:
        city = the_data['city']
        query += ('city = "' + city + '",')
    if 'state' in the_data:
        state = the_data['state']
        query += ('state = "' + state + '",')
    if 'country' in the_data:
        country = the_data['country']
        query += ('country = "' + country + '",')
    if 'contactLink' in the_data:
        contactLink = the_data['contactLink']
        query += ('contactLink = "' + contactLink + '",')
    if 'countSupplied' in the_data:
        countSupplied = the_data['countSupplied']
        query += ('countSupplied = "' + str(countSupplied) + '",')
    if 'profileText' in the_data:
        profileText = the_data['profileText']
        query += ('profileText = "' + profileText + '",')

    #remove unnecessary comma    and    update the appropriate supplier by supplierID
    query = query[0:len(query) - 1] + " WHERE supplierID = {0}".format(supplierID)

    print(query)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return jsonify({"message": "Success!"})

    # Delete a specific supplier from the database based on its supplierID
@suppliers.route('/<supplierID>', methods=['DELETE'])
def delete_supplier(supplierID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    # use cursor to query the database for a list of suppliers
    cursor.execute('DELETE FROM animal_supplier WHERE supplierID={0}'.format(supplierID))
    db.get_db().commit()
    return jsonify({"message": "Success!"}) 

# Get a certain supplier from the database based on state
@suppliers.route('/state/<state>', methods=['GET'])
def get_supplier_by_state(state):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT * FROM animal_supplier WHERE state={0}'.format(state))

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

# Get a certain suppliers contact link from the database based on ID
@suppliers.route('/<supplierID>/contact', methods=['GET'])
def get_supplier_contact_link(supplierID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for the contact link
    cursor.execute('SELECT contactLink FROM animal_supplier WHERE supplierID={0}'.format(supplierID))

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