import datetime
import sqlite3
DB = sqlite3.connect("library.db")
CURSOR = DB.cursor()
CURSOR.execute('''CREATE TABLE IF NOT EXISTS user(ID INT PRIMARY KEY, NAME TEXT, PHONENO TEXT, EMAILID TEXT, PASSWORD TEXT, FINE INT DEFAULT 0);''')
CURSOR.execute('''CREATE TABLE IF NOT EXISTS librarian(ID INT PRIMARY KEY, NAME TEXT, PHONENO TEXT);''')
CURSOR.execute('''CREATE TABLE IF NOT EXISTS book(NAME TEXT, AUTHOR TEXT, PUBLICATIONCOMPANY TEXT, RENTEDDATE TEXT, USERNAME TEXT);''')
class User:
    def registration(self):
        id_user = int(input("Enter user id:"))
        name_user = input("Enter user name:")
        password_user = input("Create password:")
        phone_no = int(input("Enter user's phone no:"))
        email_id = input("Enter user's email id:")
        CURSOR.execute('''INSERT INTO user(ID, NAME, PHONENO, EMAILID, PASSWORD) VALUES (?, ?, ?, ?, ?);''', (id_user, name_user, phone_no, email_id, password_user,))
        DB.commit()
        print("User details added successfully")
    def login(self):
        id_user = int(input("Enter user id:"))
        password_login = input("Enter your password:")
        CURSOR.execute('''SELECT PASSWORD from user WHERE ID=?;''', (id_user,))
        user_password = list(CURSOR.fetchone())
        if password_login == user_password[0]:
            print("Login successful")
        else:
            print("Invalid password")
    def update(self):
        N = None
        while N != 0:
            print("Press 1 to update phone no of the user\nPress 2 to update email ID of the user\nPress 3 to update password\n")
            N = int(input("Enter the number"))
            name_user = input("Enter the user name you want to update:")
            if N == 1:
                phone_no = int(input("Enter the phone number of the user:"))
                CURSOR.execute('''UPDATE user SET PHONENO=? WHERE NAME=?;''', (phone_no, name_user,))
                DB.commit()
                print("User details updated successfully")
                break
            if N == 2:
                email_id = input("Enter the mail id of the user:")
                CURSOR.execute('''UPDATE user SET EMAILID=? WHERE NAME=?;''', (email_id, name_user,))
                DB.commit()
                print("User details updated successfully")
                break				
            if N == 3:
                password_user = input("Enter new password:")
                CURSOR.execute('''UPDATE user SET PASSWORD=? WHERE NAME=?;''', (password_user, name_user,))
                DB.commit()
                print("Password updated successfully")
                break				
    def delete(self):
        user_name = input("Enter the name of the user you want to delete")
        CURSOR.execute('''DELETE FROM user WHERE NAME=?;''', (user_name,))
        DB.commit()
        print("Deleted user from the database")
class Books:
    def add(self):
        name_book = input("Enter the book name:")
        author_book = input("Enter author name:")
        pub_company = input("Enter the publication company of the book:")
        user_book = input("Enter the user who rented the book:")
        rented_date = input("Enter the rented date of the book:")
        dt_obj = datetime.datetime.strptime(rented_date, '%m/%d/%Y')
        dt_str = datetime.datetime.strftime(dt_obj, '%m/%d/%Y')
        CURSOR.execute('''INSERT INTO book(NAME, AUTHOR, PUBLICATIONCOMPANY, USERNAME, RENTEDDATE) VALUES (?, ?, ?, ?, ?);''', (name_book, author_book, pub_company, user_book, dt_str,))
        DB.commit()
        print("Book details added successfully")
    def update(self):
        book_name = input("Enter the book name you want to update:")
        user_update = input("Enter new user name:")
        date_update = input("Enter rented date:")	
        dt_obj = datetime.datetime.strptime(date_update, '%m/%d/%Y')
        dt_str = datetime.datetime.strftime(dt_obj, '%m/%d/%Y')		
        CURSOR.execute('''UPDATE book SET USERNAME=?, RENTEDDATE=? WHERE NAME=?;''', (user_update, dt_str, book_name,))
        DB.commit()
        print("Book details updated successfully")
    def delete(self):
        book_name = input("Enter the book name:")
        CURSOR.execute('''DELETE FROM book WHERE NAME=?;''', (book_name,))
        DB.commit()
        print("Book details deleted successfully")
    def view(self):
        N = None
        while N != 0:
            print("press 1 for Book details\npress 2 for list of book available")
            N = int(input("Enter the number:"))
            if N == 1:
                book_name = input("Enter the book name:")
                print("Book details")
                CURSOR.execute('''SELECT NAME, AUTHOR, PUBLICATIONCOMPANY, RENTEDDATE, USERNAME FROM book WHERE NAME=?;''', (book_name,))
                LIST1 = cursor.fetchall()
                for row in LIST1:
                    print(row[0], row[1], row[2], row[3], row[4])
                break
            if N == 2:
                print("List of books available")
                CURSOR.execute('''SELECT NAME FROM book;''')
                LIST2 = cursor.fetchall()
                for row in LIST2:
                    print(row[0])
                break
    def rental_operation(self):
        NOW = datetime.datetime.now()
        user_name = input("Enter the user name:")
        CURSOR.execute('''SELECT RENTEDDATE FROM book WHERE USERNAME=?;''', (user_name,))
        rented_date = list(CURSOR.fetchone())
        dt_obj = datetime.datetime.strptime(rented_date[0], '%m/%d/%Y')
        date = NOW-dt_obj
        X = date.days
        if X > 20:
            INC = 0
            TEMP = 20
            for i in range(20, X, 5):
                FINE = TEMP + INC
                INC = FINE
                TEMP = TEMP + 5
                FINE = TEMP + INC
            print("Total fine is RS.", FINE)
            CURSOR.execute('''UPDATE user SET FINE=? WHERE NAME=?;''', (FINE, user_name,))
            DB.commit()
        else:
            print("No fine")
class Librarian:
    def add(self):
        ID = int(input("Enter librarian id:"))
        NAME = input("Enter the librarian name:")
        phone_no = int(input("Enter phone no of the liberarian:"))
        CURSOR.execute('''INSERT INTO librarian(ID, NAME, PHONENO) VALUES (?, ?, ?);''', (ID, NAME, phone_no,))
        DB.commit()
    def remove(self):
        lib_name = input("Enter the librarian name:")
        CURSOR.execute('''DELETE FROM librarian WHERE NAME=?;''', (lib_name,))
        DB.commit()
        print("Details deleted successfully")
OBJ1 = User()
OBJ2 = Books()
OBJ3 = Librarian()
while True:
    print("Library Management System\n")
    print("1.User\n2.Librarian\n3.exit\n")
    N = int(input("Enter your choice:"))
    if N == 1:
        REPEAT = 'yes'
        while(REPEAT == 'yes'):
            print("User based operation")
            print("\n1.Registration.\n2.login\n3.Remove a user from database.\n4.Update User details.\n5.View book details\n")
            user_input = int(input("Enter the number between 1-4:"))
            if user_input == 1:
                print("User registration")
                OBJ1.registration()
                REPEAT = input("\nEnter yes if you want to continue:")
            if user_input == 2:
                print("User login")
                OBJ1.login()
                REPEAT = input("Enter yes if you want to continue:")
            if user_input == 3:
                print("Remove user from the database")
                OBJ1.delete()
                REPEAT = input("\nEnter yes if you want to continue:")
            if user_input == 4:
                print("Update user details")
                OBJ1.update()
                REPEAT = input("\nEnter yes if you want to continue:")
            if user_input == 5:
                print("Read book details and list of books available")
                OBJ2.view()
                REPEAT = input("\nEnter yes if you want to continue:")
        else:
            print("Exit")
    if N == 2:
        REPEAT = 'yes'
        while(REPEAT == 'yes'):
            print("Librarian")
            print("\n1.Add librarian to the database.\n2.Add a book to database.\n3.Update book details.\n4.Remove a book from database\n5.List of all avaliable books.\n6.Rental operation\n7.Remove liberarian from the database\n")
            user_input = int(input("Enter the number between 1-4:"))
            if user_input == 1:
                print("Add librarian to the database")
                N = int(input("Enter the no of entry:"))
                for i in range(0, N):
                    OBJ3.add()
                REPEAT = input("\nEnter yes if you want to continue:")
            if user_input == 2:
                print("Add a book to the database")
                N = int(input("Enter the no of entry:"))
                for i in range(0, N):
                    OBJ2.add()
                REPEAT = input("\nEnter yes if you want to continue:")
            if user_input == 3:
                print("Update the book details")
                OBJ2.update()
                REPEAT = input("\nEnter yes if you want to continue:")
            if user_input == 4:
                print("Remove a book from the database")
                OBJ2.delete()
                REPEAT = input("\nEnter yes if you want to continue:")
            if user_input == 5:
                print("Read book details and list of books available")
                OBJ2.view()
                REPEAT = input("Enter yes if you want to continue:")
            if user_input == 6:
                print("Rental operation")
                OBJ2.rental_operation()
                REPEAT = input("\nEnter yes if you want to continue:")
            if user_input == 7:
                print("Delete Librarian from the database")
                OBJ3.remove()
                REPEAT = input("\nEnter yes if you want to continue:")
        else:
            print("Exit")
    if N == 3:
        print("Exit")
        break
DB.commit()
DB.close()	    
	    







