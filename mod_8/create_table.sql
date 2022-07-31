-- Table: groups
DROP TABLE IF EXISTS groups;
CREATE TABLE grps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name VARCHAR(30) UNIQUE
);

-- Table: students
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name VARCHAR(255) UNIQUE,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES grps (id)
      ON DELETE SET NULL
      ON UPDATE CASCADE
);
 
-- Table: subjects
DROP TABLE IF EXISTS subjects;
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name VARCHAR(100) UNIQUE,
    teacher_name VARCHAR(255)
);

-- Table: grades
DROP TABLE IF EXISTS grades;
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade INTEGER NOT NULL,
    subject_id INTEGER,
    student_id INTEGER,
    date_of DATE NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    UNIQUE(grade, student_id, subject_id, date_of)
);