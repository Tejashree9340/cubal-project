-- ===============================
-- CubaL Database Setup
-- Emergency Blood & Organ Network
-- ===============================

-- Drop old database if exists (for clean run)
DROP DATABASE IF EXISTS cubal;

-- Create database
CREATE DATABASE cubal;

-- Use database
USE cubal;

-- ===============================
-- TABLE 1: DONORS
-- ===============================
CREATE TABLE donors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    location VARCHAR(100) NOT NULL,
    contact VARCHAR(15) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample donors (for testing)
INSERT INTO donors (name, blood_group, location, contact) VALUES
('Rahul', 'A+', 'Bangalore', '9876543210'),
('Sneha', 'O+', 'Whitefield', '9123456780'),
('Arjun', 'B+', 'Marathahalli', '9988776655'),
('Priya', 'AB+', 'Electronic City', '9090909090');


-- ===============================
-- TABLE 2: EMERGENCY REQUESTS
-- ===============================
CREATE TABLE requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    location VARCHAR(100) NOT NULL,
    urgency ENUM('High', 'Medium', 'Low') NOT NULL,
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample requests
INSERT INTO requests (patient_name, blood_group, location, urgency) VALUES
('Kiran', 'O+', 'Bangalore', 'High'),
('Anjali', 'A+', 'Whitefield', 'Medium');


-- ===============================
-- VIEW (ADVANCED FEATURE 🔥)
-- ===============================
-- Shows matched donors for emergency requests

CREATE VIEW donor_match AS
SELECT 
    d.name AS donor_name,
    d.blood_group,
    d.location,
    d.contact,
    r.patient_name,
    r.urgency
FROM donors d
JOIN requests r
ON d.blood_group = r.blood_group
AND d.location = r.location;

-- ===============================
-- TEST QUERIES
-- ===============================

-- View all donors
SELECT * FROM donors;

-- View all requests
SELECT * FROM requests;

-- Match donors automatically
SELECT * FROM donor_match;