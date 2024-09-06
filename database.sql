

CREATE TABLE student_login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE student_detail (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login_id INT NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    FOREIGN KEY (login_id) REFERENCES student_login(id) ON DELETE CASCADE
);


CREATE TABLE student_activity (
    activity_id INT AUTO_INCREMENT PRIMARY KEY,
    activity_name VARCHAR(255) NOT NULL,
    description TEXT,
    score INT,
    student_username VARCHAR(255),
    FOREIGN KEY (student_username) REFERENCES student_login(username) ON DELETE SET NULL
);


CREATE TABLE eventinfo (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    event_description TEXT,
    event_type VARCHAR(255),
    points INT
);

CREATE TABLE points (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    total_points INT DEFAULT 0
);

CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    activityname VARCHAR(255),
    report_description TEXT,
    student_id INT,
    teacher VARCHAR(255),
    FOREIGN KEY (student_id) REFERENCES student_detail(id) ON DELETE SET NULL
);

CREATE TABLE certificate_submission (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    name VARCHAR(255),
    email VARCHAR(255),
    organization VARCHAR(255),
    work_done TEXT,
    hours INT,
    certificate_path VARCHAR(255),
    FOREIGN KEY (student_id) REFERENCES student_login(id) ON DELETE CASCADE
);
CREATE TABLE incident_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reporter_name VARCHAR(255),
    reporter_email VARCHAR(255),
    person_name VARCHAR(255),
    cause TEXT,
    incident_date DATE,
    incident_location VARCHAR(255),
    witnesses TEXT,
    status VARCHAR(255) DEFAULT 'Pending'
);
CREATE TABLE adminlogin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    afirstname VARCHAR(255),
    alastname VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    feedback TEXT,
    rating INT
);
