-- Create the database for the application
CREATE DATABASE IF NOT EXISTS pwdmanager;

-- creating the users table
CREATE TABLE IF NOT EXISTS users
(
usrid INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(30),
password VARCHAR(255)
);

-- Inserting the root user information to the users table
-- Replace the text inside angle brackets <>
INSERT INTO users (name, password)
VALUES (<USER NAME HERE>, <PASSWORD HERE>);

-- creating the sites table which contains the login information
CREATE TABLE IF NOT EXISTS sites
(
id INT PRIMARY KEY AUTO_INCREMENT,
usrname VARCHAR(30),
registered_mail VARCHAR(50),
site_name VARCHAR(50) NOT NULL,
password VARCHAR(15) NOT NULL
);