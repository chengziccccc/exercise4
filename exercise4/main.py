import sqlite3


#Creating databases and tables
def create_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    # Create Books Table
    c.execute('''CREATE TABLE IF NOT EXISTS Books
                 (BookID TEXT PRIMARY KEY, Title TEXT, Author TEXT, ISBN TEXT, Status TEXT)''')

#Create Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS Users
                 (UserID TEXT PRIMARY KEY, Name TEXT, Email TEXT)''')

    # Create Reservations Table
    c.execute('''CREATE TABLE IF NOT EXISTS Reservations
                 (ReservationID TEXT PRIMARY KEY, BookID TEXT, UserID TEXT, ReservationDate TEXT,
                 FOREIGN KEY(BookID) REFERENCES Books(BookID),
                 FOREIGN KEY(UserID) REFERENCES Users(UserID))''')

    conn.commit()
    conn.close()


#Add new books to the Books table
def add_book():
    book_id = input("Please enter BookID: ")
    title = input("Please enter the book name: ")
    author = input("Please enter the author: ")
    isbn = input("请输入ISBN: ")
    status = input("Please enter the book status: ")

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("INSERT INTO Books VALUES (?, ?, ?, ?, ?)",
              (book_id, title, author, isbn, status))

    conn.commit()
    conn.close()
    print("Book added successfully!")


#Find detailed information about books based on BookID
def find_book_details():
    book_id = input("Please enter BookID: ")

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute('''SELECT Books.*, Users.Name, Users.Email
                 FROM Books
                 LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                 LEFT JOIN Users ON Reservations.UserID = Users.UserID
                 WHERE Books.BookID=?''', (book_id,))

    result = c.fetchone()
    if result:
        print("Book Information:")
        print("BookID:", result[0])
        print("Title:", result[1])
        print("Author:", result[2])
        print("ISBN:", result[3])
        print("Status:", result[4])
        if result[5]:
            print("Booking status: Booked")
            print("Booking User Information:")
            print("Name:", result[5])
            print("Email:", result[6])
        else:
            print("Booking status: Unsubscribed")
    else:
        print("The book does not exist in the database!")

    conn.close()


#Find the booking status of a book based on BookID, Title, UserID, and ReservationID
def find_reservation_status():
    user_input = input("Please enter query information: ")

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    if user_input.startswith('LB'):
        c.execute('''SELECT Books.Status
                     FROM Books
                     WHERE Books.BookID=?''', (user_input,))
        result = c.fetchone()
        if result:
            print("Book booking status:", result[0])
        else:
            print("The book does not exist in the database!")
    elif user_input.startswith('LU'):
        c.execute('''SELECT Books.Title, Books.Status
                     FROM Books
                     LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                     WHERE Reservations.UserID=?''', (user_input,))
        results = c.fetchall()
        if results:
            print("User Booking Books:")
            for result in results:
                print("Title:", result[0])
                print("Reserved:", result[1])
        else:
            print("The user has not booked any books!")
    elif user_input.startswith('LR'):
        c.execute('''SELECT Books.Title, Users.Name, Users.Email
                     FROM Books
                     LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                     LEFT JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Reservations.ReservationID=?''', (user_input,))
        result = c.fetchone()
        if result:
            print("Book booking information:")
            print("title:", result[0])
            print("User name:", result[1])
            print("User email:", result[2])
        else:
            print("Subscription ID does not exist in the database!")
    else:
        print("Invalid query information!")

    conn.close()


#Find detailed information about all books
def find_all_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute('''SELECT Books.*, Users.Name, Users.Email
                 FROM Books
                 LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                 LEFT JOIN Users ON Reservations.UserID = Users.UserID''')

    results = c.fetchall()
    if results:
        print("All book information:")
        for result in results:
            print("BookID:", result[0])
            print("Title:", result[1])
            print("Author:", result[2])
            print("ISBN:", result[3])
            print("Status:", result[4])
            if result[5]:
                print("Booking status: Booked")
                print("Booking User Information:")
                print("Name:", result[5])
                print("Email:", result[6])
            else:
                print("Booking status: Unsubscribed")
    else:
        print("There are no books in the database！")

    conn.close()


#Modify book details based on BookID
def update_book_details():
    book_id = input("Please enter BookID: ")

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status
                 FROM Books
                 WHERE Books.BookID=?''', (book_id,))

    result = c.fetchone()
    if result:
        print("Current Book Information:")
        print("BookID:", result[0])
        print("Title:", result[1])
        print("Author:", result[2])
        print("ISBN:", result[3])
        print("Status:", result[4])

        choice = input("Select the field to modify（Title/Author/ISBN/Status）: ")
        new_value = input("Please enter a new value: ")

        if choice == 'Title' or choice == 'Author' or choice == 'ISBN' or choice == 'Status':
            c.execute('''UPDATE Books SET {}=? WHERE BookID=?'''.format(choice), (new_value, book_id))
            conn.commit()
            print("Book information has been updated！")
        else:
            print("Invalid selection！")
    else:
        print("The book does not exist in the database！")

    conn.close()


#Delete a book based on BookID
def delete_book():
    book_id = input("Please enter BookID: ")

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
    result = c.fetchone()

    if result:
        if result[4] == 'Reserved':
            c.execute("DELETE FROM Reservations WHERE BookID=?", (book_id,))
        c.execute("DELETE FROM Books WHERE BookID=?", (book_id,))

        print("The book has been successfully deleted！")
    else:
        print("The book does not exist in the database！")

    conn.commit()
    conn.close()


#Main program
def main():
    create_database()

    while True:
        print("\nLibrary management system")
        print("1. Add New Book")
        print("2. Find detailed information about books")
        print("3. Find the booking status of books")
        print("4. Find all books")
        print("5. Modify book details")
        print("6. Delete Book")
        print("7. Exit program")

        choice = input("Please select an action: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            find_book_details()
        elif choice == '3':
            find_reservation_status()
        elif choice == '4':
            find_all_books()
        elif choice == '5':
            update_book_details()
        elif choice == '6':
            delete_book()
        elif choice == '7':
            print("The program has exited.")
            break
        else:
            print("Invalid selection!")


if __name__ == '__main__':
    main()
