from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


guides = Blueprint('guides', __name__)

# Get all the guides from the database
@guides.route('/', methods=['GET'])
def get_guides():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of guides
    cursor.execute('SELECT * FROM guides')

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

# add a new guides to the db
@guides.route('/', methods=['POST'])
def add_new_guides():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    orderDate = the_data['orderDate']
    paymentAmount = the_data['paymentAmount']
    paymentMethod = the_data['paymentMethod']
    customerID = the_data['customerID']

    # Constructing the query
    query = 'insert into guides (orderDate, paymentAmount, paymentMethod, customerID) values ("'
    query += str(orderDate) + '", "'
    query += str(paymentAmount) + '", "'
    query += str(paymentMethod) + '", "'
    query += str(customerID) + '")'
    print(query)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return jsonify({"message": "Success!"})

# Get a certain guide from the database based on ID
@guides.route('/<guideID>', methods=['GET'])
def get_guide(guideID):
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    cursor.execute('SELECT * FROM guides WHERE guideID={0}'.format(guideID))

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

# Update the specified guide in the database
@guides.route('/<guideID>', methods=['PUT'])
def update_guide(guideID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    query = 'UPDATE guides SET '

    #construct query
    update_params = []
    if 'orderDate' in the_data:
        orderDate = the_data['orderDate']
        query += ('orderData = ' + str(orderDate) + ',')
    if 'paymentAmount' in the_data:
        paymentAmount = the_data['paymentAmount']
        query += ('paymentAmount = ' + str(paymentAmount) + ',')
    if 'paymentMethod' in the_data:
        paymentMethod = the_data['paymentMethod']
        query += ('paymentMethod = ' + str(paymentMethod) + ',')
    if 'customerID' in the_data:
        customerID = the_data['customerID']
        query += ('customerID = ' + str(customerID) + ',')

    #remove unnecessary comma    and    update the appropriate order by guideID
    query = query[0:len(query) - 1] + " WHERE guideID = {0}".format(guideID)

    print(query)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return jsonify({"message": "Success!"})

# Delete a specific guide from the database
@guides.route('/<guideID>', methods=['DELETE'])
def delete_guide(guideID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    # use cursor to query the database for a list of guides
    cursor.execute('DELETE FROM guides WHERE guideID={0}'.format(guideID))
    db.get_db().commit()
    return jsonify({"message": "Success!"}) 