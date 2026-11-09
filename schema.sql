-- Parking Management System: database schema
-- Run in MySQL Command Line Client:  SOURCE D:/path/to/Parking_Management_System/schema.sql;

CREATE DATABASE IF NOT EXISTS parkings;
USE parkings;

-- One row per parking lot
CREATE TABLE IF NOT EXISTS Park (
    pid        INT          PRIMARY KEY,
    pname      VARCHAR(100) NOT NULL,
    level      VARCHAR(20),
    totalspace INT          NOT NULL,
    freespace  INT          NOT NULL,
    CONSTRAINT chk_total_positive CHECK (totalspace > 0),
    CONSTRAINT chk_free_in_range  CHECK (freespace BETWEEN 0 AND totalspace)
);

-- One row per parking visit (entry -> exit). Past visits are kept as history.
CREATE TABLE IF NOT EXISTS Vehicle (
    id            INT          AUTO_INCREMENT PRIMARY KEY,
    pid           INT          NOT NULL,
    vehicleno     VARCHAR(20)  NOT NULL,
    vehiclemodel  VARCHAR(50),
    arrivaltime   DATETIME     NOT NULL,
    departuretime DATETIME     NULL,          -- NULL means the vehicle is still parked
    amount        DECIMAL(8,2) NULL,          -- fee charged at exit
    INDEX idx_vehicle_active (vehicleno, departuretime)
);
