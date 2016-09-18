"""
SQLite workshop to get comfortable with SQL and the operations
required for managing data.  Check out the pymotw link below under
Resources for further explanations and code samples
Resources:
    http://pymotw.com/2/sqlite3/
    https://docs.python.org/2/library/sqlite3.html
"""

import os
import sqlite3

course_data = [
    'Foundations of Data Analytics and Data Science',
    'Software Engineering for Data',
    'Data Sources',
    'Data Wrangling',
    'Data Analysis I: Statistics',
    'Data Analysis II: Machine Learning',
    'Data Story Telling',
    'Applied Data Analytics (capstone project)',
]

student_data = [
    {'name': 'Donna Evants', 'email': 'devants@gmail.com'},
    {'name': 'Michael Rosen', 'email': 'michael_rosen@yahoo.com'},
    {'name': 'Elaine Miller', 'email': 'elmiller20@gmail.com'},
]


def create_tables(conn):
    """
    Creates the necessary tables in the SQLite database
    """
    # create a Cursor object for the connection
    cursor = conn.cursor()

    # create the db tables
    cursor.execute("""CREATE TABLE courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )""")
    cursor.execute("""CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT
    )""")
    cursor.execute("""CREATE TABLE registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL
    )""")

    # commit changes to the database
    conn.commit()


def connect(path="workshop.db", syncdb=False):
    """
    Connects to the database and ensures there are tables.
    """
    if not os.path.exists(path):
        syncdb = True

    conn = sqlite3.connect(path)
    if syncdb:
        create_tables(conn)

    conn.row_factory = sqlite3.Row

    return conn


def delete_existing_data(conn):
    """
    Finish this function to delete all existing data from the 'courses',
    'students', and 'registration' tables.
    The code to delete 'registrations' records has been provided.
    """
    # create a Cursor object for the connection
    cursor = conn.cursor()

    # delete all rows from the registrations table
    cursor.execute('DELETE FROM registrations;')

    # delete all rows from the students table
    cursor.execute('DELETE FROM students;')

    # delete all rows from the courses table
    cursor.execute('DELETE FROM courses;')

    # commit all pending deletes
    conn.commit()


def insert_initial_data(conn):
    """
    Finish this function to insert the initial data to the database.
    The course and student data has been provided above.  Assume that
    all students are registered for all courses.
    Sample comments on how to proceed have been provided
    """
    # create a Cursor object for the connection
    cursor = conn.cursor()

    # loop over the courses and insert them into the courses table
    for c in course_data:
        cursor.execute("INSERT INTO courses (name) VALUES (?);", (c,))

    # loop over the students and insert them into the students table
    for s in student_data:
        cursor.execute("INSERT INTO students (name, email) VALUES (?,?);",
                       (s['name'], s['email']))

    # commit all pending inserts
    conn.commit()

    # select all courses from the courses table
    courses = cursor.execute('SELECT id, name FROM courses').fetchall()

    # selete all students from the students table
    students = cursor.execute('SELECT id, name FROM students').fetchall()

    # for each course, loop through each student and insert a registration
    # record
    for course in courses:
        for student in students:
            cursor.execute("INSERT INTO registrations (course_id,student_id) VALUES (?, ?);",
                           (course['id'], student['id']))

    # commit all pending inserts
    conn.commit()


def report(conn):
    """
    Finish this function to create a report of class registrations.
    The report should consist of printing out each course name followed
    by the names of students registered in the class.
    A SQL statement to SELECT students registered for a specific course
    might look like:
        SELECT
            name
        FROM
            students
        JOIN
            registrations on students.id = registrations.student_id
        WHERE
            registrations.course_id = ?
    """
    # returns a Cursor object for the connection
    cursor = conn.cursor()

    # query for courses
    courses = cursor.execute('SELECT id, name FROM courses').fetchall()

    # loop through each course
    for course in courses:

        # print name of course
        print('\n{!s}\n----------------------------'.format(course['name']))

        # query for each student registered in the course
        students = cursor.execute("""SELECT name
                FROM students
                JOIN registrations on students.id = registrations.student_id
                WHERE registrations.course_id = ?
            """, (course['id'],)).fetchall()

        # loop through registered students and print each one's name
        for student in students:
            print(student['name'])


if __name__ == '__main__':
    conn = connect()
    delete_existing_data(conn)
    insert_initial_data(conn)
    report(conn)
