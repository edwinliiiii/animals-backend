from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


reviews = Blueprint('reviews', __name__)

# Get all the reviews from the database
@reviews.route('/', methods=['GET'])
def get_reviews():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT * FROM review')

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

@reviews.route('/', methods=['POST'])
def add_new_review():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    title = the_data['title']
    fullText = the_data['fullText']
    dateCreated = the_data['dateCreated']
    dateEdited = the_data['dateEdited']
    datePublished = the_data['datePublished']
    author = the_data['author']
    customerID = the_data['customerID']

    # Constructing the query
    query = 'insert into review (title, fullText, dateCreated, dateEdited, datePublished, author, customerID) values ("'
    query += title + '", "'
    query += fullText + '", '
    query += dateCreated + '", "'
    query += datePublished + '", "'
    query += dateEdited + '", "'
    
    query += author + '", '
    query += str(customerID) + ')'
    print(query)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return jsonify({"message": 'Success!'})

# Get a certain review from the database based on ID
@reviews.route('/<reviewID>', methods=['GET'])
def get_review(reviewID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT * FROM review WHERE reviewID={0}'.format(reviewID))

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

# Update the specified review in the database
@reviews.route('/<reviewID>', methods=['PUT'])
def update_review(reviewID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    query = 'UPDATE review SET '

    #construct query
    if 'title' in the_data:
        title = the_data['title']
        query += ('title = "' + title + '",')
    if 'fullText' in the_data:
        fullText = the_data['fullText']
        query += ('fullText = "' + fullText + '",')
    if 'dateCreated' in the_data:
        dateCreated = the_data['dateCreated']
        query += ('dateCreated = ' + str(dateCreated) + ',')
    if 'dateEdited' in the_data:
        dateEdited = the_data['dateEdited']
        query += ('dateEdited = ' + str(dateEdited) + ',')
    if 'datePublished' in the_data:
        datePublished = the_data['datePublished']
        query += ('datePublished = ' + str(datePublished) + ',')
    if 'author' in the_data:
        author = the_data['author']
        query += ('author = "' + author + '",')
    if 'customerID' in the_data:
        author = the_data['customerID']
        query += ('customerID = ' + str(customerID) + ',')

    #remove unnecessary comma    and    update the appropriate animal by animalID
    query = query[0:len(query) - 1] + " WHERE reviewID = {0}".format(reviewID)

    print(query)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return jsonify({"message": "Success!"})


# Delete a specific review from the database
@reviews.route('/<reviewID>', methods=['DELETE'])
def delete_review(reviewID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    # use cursor to query the database for a list of reviews
    cursor.execute('DELETE FROM review WHERE reviewID={0}'.format(reviewID))
    db.get_db().commit()
    return jsonify({"message": "Success!"}) 
