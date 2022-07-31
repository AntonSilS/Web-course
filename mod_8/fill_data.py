
from faker import Faker
from random import randint, choice

import os
import sqlite3
import time

NUMBER_GROUPS = 3
NUMBER_STUDENTS = 30
NUMBER_GRADES = 20
NUMBER_SUBJECTS = 5
NUMBER_TEACHERS = 3

fake_data = Faker()

def generate_data (stds):
    grades = list(range(1, 13))
    groups = ['201_B', '202_C', '203_D']
    subjects = ['Math', 'IT', 'EE', 'ECE', 'Law']
  
    students = [fake_data.name() for _ in range(stds)]
    teachers = ['Cons Freddy', 'Johnson Nill', 'Brown Jacob']

    return groups, students, grades, subjects, teachers


def prepare_data(groups, students, grades, subjects, teachers):

    for_groups = [(group, ) for group in groups]

    for_students = [(std, randint(1, NUMBER_GROUPS)) for std in students]

    for_subjects = [(sbj, choice(teachers)) for sbj in subjects]

    for_grades = []

    for std_id in range(1, NUMBER_STUDENTS + 1):
        for _ in range(NUMBER_GRADES):
            date = fake_data.date_time_between(start_date='-90d', end_date='now').date()
            for_grades.append((choice(grades), randint(1, NUMBER_SUBJECTS), std_id, date))

    return for_groups, for_students, for_subjects, for_grades


def insert_data_to_db(groups, students, subjects, grades, path):
    with sqlite3.connect(path) as con:
        cur = con.cursor()

        sql_grps = """INSERT INTO grps(group_name)
                               VALUES (?)"""
        cur.executemany(sql_grps, groups)

        sql_students = """INSERT INTO students(student_name, group_id)
                               VALUES (?, ?)"""
        cur.executemany(sql_students, students)

        sql_subjects = """INSERT INTO subjects(subject_name, teacher_name)
                               VALUES (?, ?)"""
        cur.executemany(sql_subjects, subjects)

        sql_grades = """INSERT INTO grades(grade, subject_id, student_id, date_of)
                               VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_grades, grades)

def main(path):
    groups, students, grades, subjects, teachers = generate_data(NUMBER_STUDENTS)
    for_groups, for_students, for_subjects, for_grades = prepare_data(groups, students, grades, subjects, teachers)
    insert_data_to_db(for_groups, for_students, for_subjects, for_grades, path)
    print(f'Database: {os.path.split(path)[1]} was succefully filled\n')
    time.sleep(2)

def fill_db(path):
    main(path)