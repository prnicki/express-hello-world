import sqlite3 as sq
import datetime as time
import logging as log
import os
from tkinter import *


date = time.date.today()
print("Welcome to Student Database\n Login with username at ", date)
# sqlite codes for database

with sq.connect("Students Portal.db") as connector:
    cursor = connector.cursor()


now = date.year

# beginning of sqlite3 creation tables.
# students table
cursor.execute("""CREATE TABLE IF NOT EXISTS students (
                student_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                student_course TEXT NOT NULL,
                student_DOB INTEGER,
                student_Age INTEGER,
                FOREIGN KEY (student_course) REFERENCES courses(course_name)
                )
                """)

connector.commit()
# courses table
cursor.execute("""CREATE TABLE IF NOT EXISTS courses (
                    course_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    course_name TEXT NOT NULL,
                    Fees INTEGER NOT NULL
                    )
                    """)
connector.commit()
# fees records table
cursor.execute("""CREATE TABLE IF NOT EXISTS fees_records (
                    Invoice_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    student_name TEXT NOT NULL,
                    course_name TEXT NOT NULL,
                    payment_method TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    date TEXT NOT NULL, /* import time from current machine time (date)*/
                    FOREIGN KEY (course_name) REFERENCES courses (course_name)
            )
            """)
connector.commit()
# end of sqlite3 table creations


def fees_payment():
    fees_data = [];
    s_id = input("Enter your student id to pay fees: ");
    
    try:
        student = cursor.execute(
            """SELECT student_ID,student_name, student_course, student_DOB, student_Age FROM students WHERE student_ID =?;""", s_id);
        the_user = student.fetchone();
        u_name = the_user[1];
        course = the_user[2];
        # the user[1]= username the user[2]= course_name
        print("\nWelcome back", u_name, "pursuing", course)

        payment_method = input(
            "\nEnter method of payment \n 1.Cheque \n 2.Cash\n");

        fees_query = None
        fees_query = cursor.execute(
            """SELECT course_ID,course_name,Fees FROM courses WHERE course_name=?""", [course]);
    #    successful upto here

        student_fees = fees_query.fetchone();
        total_fees = student_fees[2];
        print("\nYou are required to pay", total_fees)
        total_fees = int(total_fees);
        # the_user[2];
        amount = input("How much are you paying?\n");
        amount = int(amount);

        while amount > total_fees:
            print("You cannot pay more than", total_fees)
            amount = input("How much are you paying?\n");
            amount = int(amount);

        last_invoice = cursor.execute(
            """SELECT MAX(Invoice_ID) AS last_invoice FROM fees_records""");
        current = last_invoice.fetchone();
        current_now = current[0];
        
        if current_now == None:
            current_invoice = 1
        else:
            current_invoice = current_now + 1
           
        fees_data.append(current_invoice)
        fees_data.append(u_name)
        fees_data.append(course)
        fees_data.append(payment_method)
        fees_data.append(amount)
        fees_data.append(date)
       

        print("Please confirm the following detail: ")
        for record in fees_data:
            print(record)
        
        cursor.execute("""INSERT INTO fees_records VALUES (?,?,?,?,?,?)""", fees_data);
        connector.commit();
        print("Saving Records...")
        # time.time.sleep(3);
        print("Successfully sent");

    except:
        print("Please check your user id and try again.")

    
def courses():  # course function
    print("Welcome to courses section!")
    course_id = input("Enter course ID: ");
    try:
        course = cursor.execute("""SELECT course_ID FROM courses WHERE course_ID=?""", course_id);
        info = course.fetchone();
        print("Course already exists", info[1]);
    except:
        course_info = []
        course_info.append(course_id)
        course_name = input("enter the course name: ");
        course_info.append(course_name)
        fees = input("How much should each student pay: ");
        course_info.append(fees)
        course_info
        cursor.execute("""INSERT INTO courses (course_ID, course_name, Fees) VALUES (?,?,?)""", course_info);
        connector.commit();


def addStudent():  # student function
    user_data = []
    student_ID = input("Please enter a student ID:  ")
    user_data.append(student_ID)
    student_name = input("Please enter your name:  ")
    user_data.append(student_name)
    course_id = input("Please enter your course_id:  ")

    try:
        result = cursor.execute("""SELECT * FROM courses WHERE course_ID=?""", [course_id]);
        id_of_course = result.fetchone();
        c_name = id_of_course[1];
        print(c_name) # getting the course name from course table using id_of_course.

        try:
            user_data.append(c_name);# adding the name of the course to the list of students data.
            student_DOB = input("Please enter your date of birth (YYYY):  ")
            student_DOB = int(student_DOB)
            user_data.append(student_DOB)
            student_Age = now-student_DOB
            user_data.append(student_Age)
            user_data
        except:
            print("the error will appear here")

    except:
        print("Sorry we don't have a course by that ID")
 # sqlite validating that there is no student with such a name
    try:
        # inserting to the database
        cursor.execute(
            """INSERT INTO students (student_ID, student_name, student_course, student_DOB, student_Age) VALUES (?,?,?,?,?) """, user_data)
        connector.commit()
    except:
        print("Student with id", student_ID, "already exists")
    # sqlite end for students


def login():  # login from users side
    userCredentials = [];
    username = input("Please enter your userID: ");
    try:
        currentUser = cursor.execute("""SELECT student_ID,student_name, student_course, student_DOB, student_Age FROM students WHERE student_ID =?;""",[username]);
        the_user = currentUser.fetchone();
        # checking if the users input is actually registered with us
        for record in the_user:
            print([record])
    except:
        print("No such student in our database sign up instead")
        addStudent()

def fees_balance():
    print("we are checking fees paid and balance here");

# addStudent();


# def delete():
#     user_down=cursor.execute("""DELETE FROM students WHERE student ID=? AND student""")
# # connector.close()
# login();
def paid_fees():
    print("Please select the options here\n 1.By Student ID\n 2.By Course ID\n");
    try:
        option=int(input());
        if option==1:
            print("Enter student ID for query search: ");
            student=int(input());
            try:
                students=cursor.execute("""SELECT * FROM students WHERE student_ID=?""", [student]);
                search_results=students.fetchone();
                name=search_results[1];
                print(name);
                student_name=cursor.execute("""SELECT * FROM fees_records WHERE student_name=?""", [name]);
                all_data=students.fetchall();
                print("Please wait while we extract records\n");
                print("Inv no" , " Course", "\t\tPayment mtd " , " ", " Amount ", " Date");
                total_sum=0;
                for record in all_data:
                    print(record[0],"\t", record[2]," ", record[3], " ", record[4], " ", record[5]);
                    total_sum+=record[4];
                
               
                course_name=search_results[2];
                print(course_name);
                courses_query=cursor.execute("""SELECT * FROM courses WHERE course_name=?""", [course_name]);
                course_details=courses_query.fetchone();
              
                c_name=course_details[1];
                t_fees=0;
                t_fees=course_details[2]
                fees_bal=(t_fees - total_sum);
            
                
                print(f"\nTotal fees to be paid Ksh.{t_fees}\nTotal amount paid is: Ksh.{total_sum}\nDue amount is Ksh.{fees_bal}\n");

            except:
                print("We do not have any records of paying fees");

        elif option==2:
            print("Please select the course you want to check via its ID\n");
            course_table=cursor.execute("""SELECT * FROM courses """);
            all_courses=course_table.fetchall();
            print("ID\t Course Name \t\t\t Charges ")
            for record in all_courses:
                print(record[0]," ", record[1],"\t", record[2]);
            
            print(" : ");
            course_check=int(input());
            courses_extract=cursor.execute("""SELECT * FROM courses WHERE course_ID=?""", [course_check])
            
            # response=int(input());

    except:
        print("nothing");

