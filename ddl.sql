DROP DATABASE IF EXISTS railway;
CREATE DATABASE railway;
USE railway;

CREATE TABLE students
(
    id         INTEGER PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name  VARCHAR(255) NOT NULL,
    unix_id    VARCHAR(10)  NOT NULL UNIQUE
);

CREATE TABLE courses
(
    id         INTEGER PRIMARY KEY AUTO_INCREMENT,
    moniker    VARCHAR(10) NOT NULL UNIQUE,
    name       VARCHAR(255) NOT NULL,
    department VARCHAR(255) NOT NULL
);

CREATE TABLE prerequisites
(
    id        INTEGER PRIMARY KEY AUTO_INCREMENT,
    course    VARCHAR(10) NOT NULL,
    prereq    VARCHAR(10) NOT NULL,
    min_grade INTEGER NOT NULL,
    FOREIGN KEY (course) REFERENCES courses (moniker),
    FOREIGN KEY (prereq) REFERENCES courses (moniker),
    CHECK (min_grade >= 0 AND min_grade <= 100)
);
