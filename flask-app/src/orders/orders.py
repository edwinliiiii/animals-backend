from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


orders = Blueprint('orders', __name__)

# Get all the orders from the database
@orders.route('/', methods=['GET'])
def get_orders():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of orders
    cursor.execute('SELECT * FROM `order`')

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

# add a new order to the db
@orders.route('/', methods=['POST'])
def add_new_order():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    orderDate = the_data['orderDate']
    paymentAmount = the_data['paymentAmount']
    paymentMethod = the_data['paymentMethod']
    customerID = the_data['customerID']

    # Constructing the query
    query = 'insert into `order` (orderDate, paymentAmount, paymentMethod, customerID) values ("'
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

# Get a certain order from the database based on ID
@orders.route('/<orderID>', methods=['GET'])
def get_order(orderID):
    
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    cursor.execute('SELECT * FROM `order` WHERE orderID={0}'.format(orderID))

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

# Update the specified order in the database
@orders.route('/<orderID>', methods=['PUT'])
def update_order(orderID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    query = 'UPDATE `order` SET '

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

    #remove unnecessary comma    and    update the appropriate order by orderID
    query = query[0:len(query) - 1] + " WHERE orderID = {0}".format(orderID)

    print(query)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return jsonify({"message": "Success!"})

# Delete a specific order from the database
@orders.route('/<orderID>', methods=['DELETE'])
def delete_order(orderID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    # use cursor to query the database for a list of products
    cursor.execute('DELETE FROM `order` WHERE orderID={0}'.format(orderID))
    db.get_db().commit()
    return jsonify({"message": "Success!"}) 