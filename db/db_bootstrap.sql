-- This file is to bootstrap a database for the CS3200 project. 

-- Create a new database.  You can change the name later.  You'll
-- need this name in the FLASK API file(s),  the AppSmith 
-- data source creation.
create database cool_db;

-- Via the Docker Compose file, a special user called webapp will 
-- be created in MySQL. We are going to grant that user 
-- all privilages to the new database we just created. 
-- TODO: If you changed the name of the database above, you need 
-- to change it here too.
grant all privileges on cool_db.* to 'webapp'@'%';
flush privileges;

-- Move into the database we just created.
-- TODO: If you changed the name of the database above, you need to
-- change it here too. 
use cool_db;

-- Put your DDL 
DROP TABLE IF EXISTS guides;
CREATE TABLE IF NOT EXISTS guides
(
    title       varchar(75) NOT NULL,
    guideText  text        NOT NULL,
    dateCreated datetime    NOT NULL,
    guideID     int AUTO_INCREMENT PRIMARY KEY
);

DROP TABLE IF EXISTS customer;
CREATE TABLE IF NOT EXISTS customer
(
    firstName   varchar(50) NOT NULL,
    lastName    varchar(50) NOT NULL,
    cellPhone   varchar(15) NOT NULL,
    homePhone   varchar(15) NOT NULL,
    email       varchar(75) NOT NULL,
    street      varchar(50) NOT NULL,
    city        varchar(50) NOT NULL,
    state       varchar(25) NOT NULL,
    zip         int         NOT NULL,
    profileText text        NOT NULL,
    customerID  int AUTO_INCREMENT PRIMARY KEY,
    CONSTRAINT unique_email UNIQUE (email),
    CONSTRAINT unique_cell UNIQUE (cellPhone),
    CONSTRAINT unique_home UNIQUE (homePhone)
);

DROP TABLE IF EXISTS review;
CREATE TABLE IF NOT EXISTS review
(
    title         varchar(75) NOT NULL,
    reviewText    text,       NOT NULL
    dateCreated   datetime    NOT NULL,
    dateEdited    datetime,
    datePublished datetime,
    author        varchar(25),
    customerID    int         NOT NULL,
    reviewID      int AUTO_INCREMENT PRIMARY KEY,
    FOREIGN KEY (customerID) REFERENCES customer (customerID) ON UPDATE cascade ON DELETE restrict
);

DROP TABLE IF EXISTS `order`;
CREATE TABLE IF NOT EXISTS `order`
(
    orderDate     datetime          NOT NULL,
    paymentAmount decimal(15, 2)    NOT NULL,
    paymentMethod varchar(15)       NOT NULL,
    customerID    int               NOT NULL,
    orderID       int AUTO_INCREMENT PRIMARY KEY,
    FOREIGN KEY (customerID) REFERENCES customer (customerID) ON UPDATE cascade ON DELETE restrict
);

DROP TABLE IF EXISTS animal_supplier;
CREATE TABLE IF NOT EXISTS animal_supplier
(
    firstName     varchar(50) NOT NULL,
    lastName      varchar(50) NOT NULL,
    phone         varchar(15) NOT NULL,
    email         varchar(75) NOT NULL,
    company       varchar(75) NOT NULL,
    city          varchar(50) NOT NULL,
    state         varchar(25) NOT NULL,
    country       varchar(25) NOT NULL,
    contactLink   varchar(50) NOT NULL,
    countSupplied int NOT NULL,
    profileText   text NOT NULL,
    supplierID    int AUTO_INCREMENT PRIMARY KEY,
    CONSTRAINT unique_email UNIQUE (email),
    CONSTRAINT unique_phone UNIQUE (phone)
);

DROP TABLE IF EXISTS animal;
CREATE TABLE IF NOT EXISTS animal
(
    specialRequirements varchar(75),
    age                 tinyint        NOT NULL,
    gender              tinyint(1)     NOT NULL,           # 1 = female, 0 = male
    price               decimal(15, 2) NOT NULL,
    healthStatus        varchar(75)    NOT NULL,
    behavior            varchar(75)    NOT NULL,
    origin              varchar(75)    NOT NULL,
    availability        tinyint(1)     NOT NULL DEFAULT 1, # 1 = available, 0 = unavailable
    orderID             int,
    supplierID          int            NOT NULL,
    animalID            int AUTO_INCREMENT PRIMARY KEY,
    FOREIGN KEY (orderID) REFERENCES `order` (orderID) ON UPDATE cascade ON DELETE restrict,
    FOREIGN KEY (supplierID) REFERENCES animal_supplier (supplierID) ON UPDATE cascade ON DELETE restrict
);

DROP TABLE IF EXISTS animal_type;
CREATE TABLE IF NOT EXISTS animal_type
(
    species      varchar(75) NOT NULL,
    subSpecies   varchar(75) NOT NULL,
    animalID     int         NOT NULL,
    animalTypeID int AUTO_INCREMENT PRIMARY KEY,
    FOREIGN KEY (animalID) REFERENCES animal (animalID) ON UPDATE cascade ON DELETE restrict
);

-- Add sample data. 
INSERT INTO guides (title, guideText, dateCreated)
VALUES
('Getting Started with Pet Adoption', 'This guide will help you navigate the process of adopting a new pet.', '2022-11-25'),
('Caring for Your New Companion', 'Learn about the essential care tips for your newly adopted pet.', '2022-11-24'),
('Understanding Pet Behavior', 'Explore common behaviors in pets and how to address them.', '2022-11-23');

INSERT INTO customer(firstName, lastName, cellPhone, homePhone, email, street, city, state, zip, profileText)
VALUES
('John', 'Doe', '123-456-7890', '987-654-3210', 'john.doe@example.com', '123 Main St', 'Cityville', 'CA', 12345, 'Pet lover and advocate.'),
('Alice', 'Smith', '555-123-4567', '555-987-6543', 'alice.smith@example.com', '456 Oak St', 'Townsville', 'NY', 67890, 'Excited to bring a new furry friend into our home.'),
('Bob', 'Johnson', '999-888-7777', '111-222-3333', 'bob.johnson@example.com', '789 Elm St', 'Villagetown', 'TX', 54321, 'Looking for a playful companion for my family.');

INSERT INTO review (title, reviewText, dateCreated, dateEdited, datePublished, author, customerID)
VALUES
('Great Experience', 'I adopted a lovely cat from this shelter. The staff was friendly, and the process was smooth.', '2022-11-25', NULL, '2022-11-26', 'HappyAdopter', 1),
('Wonderful Service', 'The team at AdoptAllAnimals is dedicated and caring. They helped me find the perfect pet for my family.', '2022-11-24', NULL, '2022-11-25', 'PetLover123', 2),
('Highly Recommend', 'AdoptAllAnimals is doing fantastic work. I am grateful for their commitment to animal welfare.', '2022-11-23', '2022-11-24', '2022-11-25', 'AnimalAdvocate', 3);

INSERT INTO `order`(orderDate, paymentAmount, paymentMethod, customerID)
VALUES
('2022-11-25', 50.00, 'Credit Card', 1),
('2022-11-24', 75.50, 'PayPal', 2),
('2022-11-23', 100.00, 'Cash', 3);

INSERT INTO animal_supplier(firstName, lastName, phone, email, company, city, state, country, contactLink, countSupplied, profileText)
VALUES
('Emily', 'Jones', '555-111-2222', 'emily.jones@example.com', 'Pet World Supplies', 'Cityville', 'CA', 'USA', 'petworldsupplies.com', 50, 'Providing high-quality pet supplies.'),
('Michael', 'Lee', '999-888-7777', 'michael.lee@example.com', 'Furry Friends Supply Co.', 'Townsville', 'NY', 'USA', 'furryfriendssupply.com', 75, 'Your one-stop-shop for all pet needs.'),
('Sarah', 'Smith', '123-456-7890', 'sarah.smith@example.com', 'Happy Tails Pet Supply', 'Villagetown', 'TX', 'USA', 'happytailssupply.com', 100, 'Dedicated to the well-being of pets.');

INSERT INTO animal(specialRequirements, age, gender, price, healthStatus, behavior, origin, availability, orderID, supplierID)
VALUES
('None', 2, 1, 25.00, 'Healthy', 'Playful', 'Local', 1, 1, 1),
('Vaccinated', 1, 0, 30.00, 'Stable', 'Calm', 'International', 1, 2, 2),
('Special Diet', 3, 1, 40.00, 'Good', 'Energetic', 'Local', 1, 3, 3);

INSERT INTO animal_type(species, subSpecies, animalID)
VALUES
('Dog', 'Golden Retriever', 1),
('Cat', 'Siamese', 2),
('Dog', 'Labrador', 3);
