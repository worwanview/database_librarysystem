import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="134.209.101.105",
        user="group19",
        password="password19",
        database="db_group19"
    )

def search_book():
    db = connect_db()
    cursor = db.cursor()
    keyword = input("Enter book title or part of it: ")
    sql = "SELECT BookID, BookTitle FROM Books WHERE BookTitle LIKE %s"
    cursor.execute(sql, ("%" + keyword + "%",))
    results = cursor.fetchall()
    
    if results:
        print("\nBooks found:")
        print(f"{'Book ID'.ljust(10)} {'Title'.ljust(40)}")
        print("-" * 50)
        for row in results:
            print(f"{str(row[0]).ljust(10)} {row[1].ljust(40)}")
    else:
        print("No books found.")
    
    cursor.close()
    db.close()


def list_all_books():
    db = connect_db()
    cursor = db.cursor()
    
    # Query ที่ใช้ JOIN ระหว่าง Books, AuthorBookList และ Authors
    cursor.execute("""
        SELECT Books.BookID, Books.BookTitle, Authors.AuthorName
        FROM Books
        JOIN AuthorBookList ON Books.BookID = AuthorBookList.BookID
        JOIN Authors ON AuthorBookList.AuthorID = Authors.AuthorID
    """)
    
    results = cursor.fetchall()
    
    if results:
        print("\nList of all books with authors:")
        print(f"{'Book ID'.ljust(10)} {'Title'.ljust(40)} {'Author'.ljust(30)}")
        print("-" * 80)
        for row in results:
            print(f"{str(row[0]).ljust(10)} {row[1].ljust(40)} {row[2].ljust(30)}")
    else:
        print("No books found.")
    
    cursor.close()
    db.close()



def add_book():
    db = connect_db()
    cursor = db.cursor()
    
    title = input("Enter book title: ")
    price = input("Enter price: ")
    publisher = input("Enter publisher: ")
    pub_year = input("Enter publication year: ")
    category_id = input("Enter book category ID: ")
    
    author_name = input("Enter author name: ")

    # เช็คว่านักเขียนมีอยู่หรือไม่
    cursor.execute("SELECT AuthorID FROM Authors WHERE AuthorName = %s", (author_name,))
    author = cursor.fetchone()

    if author:
        author_id = author[0]
    else:
        cursor.execute("INSERT INTO Authors (AuthorName) VALUES (%s)", (author_name,))
        db.commit()
        author_id = cursor.lastrowid

    # เพิ่มหนังสือ
    cursor.execute(
        "INSERT INTO Books (BookTitle, Price, Publisher, PublicationYear, BookCategoryID) VALUES (%s, %s, %s, %s, %s)",
        (title, price, publisher, pub_year, category_id)
    )
    db.commit()
    book_id = cursor.lastrowid

    # เพิ่มข้อมูลใน AuthorBookList
    cursor.execute("INSERT INTO AuthorBookList (AuthorID, BookID, PublicationYear) VALUES (%s, %s, %s)", 
                   (author_id, book_id, pub_year))
    db.commit()
    
    print("\nBook added successfully!")
    print(f"{'Book Title:'.ljust(20)} {title}")
    print(f"{'Author:'.ljust(20)} {author_name}")
    print(f"{'Publisher:'.ljust(20)} {publisher}")
    print(f"{'Publication Year:'.ljust(20)} {pub_year}")
    print(f"{'Category ID:'.ljust(20)} {category_id}")
    print(f"{'Price:'.ljust(20)} {price}")
    
    cursor.close()
    db.close()


def add_member():
    db = connect_db()
    cursor = db.cursor()
    
    full_name = input("Enter full name: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")
    membership_type = input("Enter membership type (ปกติ/พิเศษ): ")
    education_type = input("Enter education type (นักเรียน/นักศึกษา/อาจารย์): ")
    
    sql = """
        INSERT INTO LibraryUsers (FullName, Email, PhoneNumber, MembershipType, EducationType)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (full_name, email, phone, membership_type, education_type))
    db.commit()
    
    print("\nMember added successfully!")
    print(f"{'Full Name:'.ljust(20)} {full_name}")
    print(f"{'Email:'.ljust(20)} {email}")
    print(f"{'Phone Number:'.ljust(20)} {phone}")
    print(f"{'Membership Type:'.ljust(20)} {membership_type}")
    print(f"{'Education Type:'.ljust(20)} {education_type}")
    
    cursor.close()
    db.close()


def search_member():
    db = connect_db()
    cursor = db.cursor()
    
    keyword = input("Enter member name or email: ")
    sql = "SELECT MemberID, FullName, Email FROM LibraryUsers WHERE FullName LIKE %s OR Email LIKE %s"
    cursor.execute(sql, ("%" + keyword + "%", "%" + keyword + "%"))
    results = cursor.fetchall()

    if results:
        print("\nMembers found:")
        for row in results:
            print(f"{'Member ID:'.ljust(15)} {row[0]}")
            print(f"{'Name:'.ljust(15)} {row[1]}")
            print(f"{'Email:'.ljust(15)} {row[2]}")
            print("-" * 40) 
    else:
        print("--No members found.--")
    
    cursor.close()
    db.close()


def list_all_members():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT MemberID, FullName, Email FROM LibraryUsers")
    results = cursor.fetchall()
    
    print("\nList of all members:")
    if results:
        for row in results:
            print(f"{'Member ID:'.ljust(15)} {row[0]}")
            print(f"{'Name:'.ljust(15)} {row[1]}")
            print(f"{'Email:'.ljust(15)} {row[2]}")
            print("-" * 40)  
    else:
        print("No members found.")
    
    cursor.close()
    db.close()

def view_borrowing_history():
    db = connect_db()
    cursor = db.cursor()
    sql = """
        SELECT BorrowHistory.BorrowID, LibraryUsers.FullName, Books.BookTitle, BorrowHistory.BorrowDate, BorrowHistory.ReturnDate
        FROM BorrowHistory
        JOIN LibraryUsers ON BorrowHistory.MemberID = LibraryUsers.MemberID
        JOIN Books ON BorrowHistory.BookID = Books.BookID
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    
    print("\nBorrowing History:")
    if results:
        for row in results:
            print(f"{'Borrow ID:'.ljust(15)} {row[0]}")
            print(f"{'Member:'.ljust(15)} {row[1]}")
            print(f"{'Book:'.ljust(15)} {row[2]}")
            print(f"{'Borrowed:'.ljust(15)} {row[3]}")
            print(f"{'Return:'.ljust(15)} {row[4]}")
            print("-" * 40)  
    else:
        print("No borrowing history found.")
    
    cursor.close()
    db.close()


def add_borrow_record():
    db = connect_db()
    cursor = db.cursor()
    
    member_id = input("Enter Member ID: ")
    book_id = input("Enter Book ID: ")
    staff_id = input("Enter Staff ID: ")
    borrow_date = input("Enter Borrow Date (YYYY-MM-DD): ")

    # ตรวจสอบประเภทสมาชิก
    cursor.execute("SELECT MembershipType FROM LibraryUsers WHERE MemberID = %s", (member_id,))
    membership = cursor.fetchone()

    if not membership:
        print("Member not found.")
        return

    membership_type = membership[0]
    return_days = 14 if membership_type == "พิเศษ" else 7
    return_date = f"DATE_ADD({borrow_date}, INTERVAL {return_days} DAY)"

    # add BowrowHistory
    sql = """
        INSERT INTO BorrowHistory (MemberID, BookID, StaffID, BorrowDate, ReturnDate)
        VALUES (%s, %s, %s, %s, DATE_ADD(%s, INTERVAL %s DAY))
    """
    cursor.execute(sql, (member_id, book_id, staff_id, borrow_date, borrow_date, return_days))
    db.commit()

    # แสดงผลการยืม
    print("\nBorrow Record Added Successfully!")
    print(f"Member ID: {member_id}")
    print(f"Book ID: {book_id}")
    print(f"Staff ID: {staff_id}")
    print(f"Borrow Date: {borrow_date}")
    print(f"Return Date: {borrow_date} + {return_days} days = {borrow_date}")
    
    cursor.close()
    db.close()


def delete_borrow_record():
    db = connect_db()
    cursor = db.cursor()
    
    borrow_id = input("Enter Borrow ID to delete: ")
    
    # ตรวจสอบว่า BorrowID มีอยู่ในฐานข้อมูลหรือไม่
    cursor.execute("SELECT * FROM BorrowHistory WHERE BorrowID = %s", (borrow_id,))
    borrow_record = cursor.fetchone()
    
    if borrow_record:
        sql = "DELETE FROM BorrowHistory WHERE BorrowID = %s"
        cursor.execute(sql, (borrow_id,))
        db.commit()
        print(f"Borrow record with Borrow ID {borrow_id} deleted successfully!")
    else:
        print(f"Borrow ID {borrow_id} not found. No record deleted.")
    
    cursor.close()
    db.close()


def delete_book():
    db = connect_db()
    cursor = db.cursor()
    
    book_id = input("Enter Book ID to delete: ")
    
    # ตรวจสอบว่า BookID มีอยู่ในฐานข้อมูลหรือไม่
    cursor.execute("SELECT * FROM Books WHERE BookID = %s", (book_id,))
    book_record = cursor.fetchone()
    
    if book_record:
        sql = "DELETE FROM Books WHERE BookID = %s"
        cursor.execute(sql, (book_id,))
        db.commit()
        print(f"Book with Book ID {book_id} deleted successfully!")
    else:
        print(f"Book ID {book_id} not found. No record deleted.")
    
    cursor.close()
    db.close()

def delete_member():
    db = connect_db()
    cursor = db.cursor()
    
    member_id = input("Enter Member ID to delete: ")
    
    # ตรวจสอบว่า MemberID มีอยู่ในฐานข้อมูลหรือไม่
    cursor.execute("SELECT * FROM LibraryUsers WHERE MemberID = %s", (member_id,))
    member_record = cursor.fetchone()
    
    if member_record:
        sql = "DELETE FROM LibraryUsers WHERE MemberID = %s"
        cursor.execute(sql, (member_id,))
        db.commit()
        print(f"Member with Member ID {member_id} deleted successfully!")
    else:
        print(f"Member ID {member_id} not found. No record deleted.")
    
    cursor.close()
    db.close()




def main():
    while True:
        print("\nLibrary Management System")
        print("1. Search for a Book")
        print("2. Search for a Member")
        print("3. List All Books")
        print("4. List All Members")
        print("5. View Borrowing History")
        print("6. Add a Book")
        print("7. Add a Member")
        print("8. Add Borrow Record")
        print("9. Delete Borrow Record")
        print("10. Delete a Book")
        print("11. Delete a Member")
        print("12. Logout")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            search_book()
        elif choice == "2":
            search_member()
        elif choice == "3":
            list_all_books()
        elif choice == "4":
            list_all_members()
        elif choice == "5":
            view_borrowing_history()
        elif choice == "6":
            add_book()
        elif choice == "7":
            add_member()
        elif choice == "8":
            add_borrow_record()
        elif choice == "9":
            delete_borrow_record()
        elif choice == "10":
            delete_book()
        elif choice == "11":
            delete_member()
        elif choice == "12":
            print("----Logging out----")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
