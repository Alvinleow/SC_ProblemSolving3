# Simple Library System

# -------------------------------------------
# Reading and Writing Data
# -------------------------------------------

def load_books(filename="books.txt"):
    """
    Loads book records from a file into a dictionary.
    Each record: book_id,title,availability
    """
    books = {}
    with open(filename, "r") as file:
        for line in file:
            book_id, title, available = line.strip().split(",")
            books[book_id] = {"title": title, "available": available == "True"}
    return books

def save_books(books, filename="books.txt"):
    """
    Saves the updated books dictionary back to the file.
    """
    with open(filename, "w") as file:
        for book_id, info in books.items():
            file.write(f"{book_id},{info['title']},{info['available']}\n")

def load_users(filename="user.txt"):
    """
    Loads user records from a file into a dictionary.
    Each record: user_id,name,borrowed_book_ids...
    """
    users = {}
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            user_id, name = parts[0], parts[1]
            borrowed = parts[2:] if len(parts) > 2 else []
            users[user_id] = {"name": name, "borrowed": borrowed}
    return users

def save_users(users, filename="user.txt"):
    """
    Saves the updated users dictionary back to the file.
    """
    with open(filename, "w") as file:
        for user_id, info in users.items():
            borrowed = ",".join(info["borrowed"])
            if borrowed:
                file.write(f"{user_id},{info['name']},{borrowed}\n")
            else:
                file.write(f"{user_id},{info['name']}\n")


# -------------------------------------------
# Get Available Books
# -------------------------------------------

def get_available_books(books):
    """
    Returns a list of books that are currently available.
    """
    return [f"{bid}: {b['title']}" for bid, b in books.items() if b["available"]]

# -------------------------------------------
# Borrowing Books
# -------------------------------------------

def borrow_book(users, books, user_id, book_id):
    """
    Allows a user to borrow a book.
    Uses assertions to ensure design-by-contract rules.
    """
    # Pre-conditions
    assert user_id in users, "Invalid user ID"
    assert book_id in books, "Invalid book ID"
    assert books[book_id]["available"], "Book is already borrowed"
    assert book_id not in users[user_id]["borrowed"], "Book already borrowed by user"

    # Process
    users[user_id]["borrowed"].append(book_id)
    books[book_id]["available"] = False

    # Post-conditions
    assert not books[book_id]["available"], "Book should now be unavailable"
    assert book_id in users[user_id]["borrowed"], "Book should be in user's borrowed list"

    print(f"Book '{books[book_id]['title']}' successfully borrowed by {users[user_id]['name']}")

# -------------------------------------------
# Returning Books
# -------------------------------------------

def return_book(users, books, user_id, book_id):
    """
    Allows a user to return a previously borrowed book.
    Uses assertions to ensure contract rules are followed.
    """
    # Pre-conditions
    assert user_id in users, "Invalid user ID"
    assert book_id in users[user_id]["borrowed"], "User hasn't borrowed this book"
    assert not books[book_id]["available"], "Book is already marked as available"

    # Process
    users[user_id]["borrowed"].remove(book_id)
    books[book_id]["available"] = True

    # Post-conditions
    assert books[book_id]["available"], "Book should now be available"
    assert book_id not in users[user_id]["borrowed"], "Book should be removed from user's list"

    print(f"Book '{books[book_id]['title']}' returned by {users[user_id]['name']}")

# -------------------------------------------
# User Interface & Program Flow
# -------------------------------------------

def show_menu():
    """
    Displays the main menu and returns user's choice.
    """
    print("\nWelcome to Simple Library System")
    print("1. View Available Books")
    print("2. Borrow a Book")
    print("3. Return a Book")
    print("4. Exit")
    return input("\nChoose an option (1-4): ")

# -------------------------------------------
# Main Program Execution
# -------------------------------------------

if __name__ == "__main__":
    books = load_books()
    users = load_users()

    while True:
        choice = show_menu()

        if choice == "1":
            print("\nAvailable Books:")
            for book in get_available_books(books):
                print(" -", book)

        elif choice == "2":
            user_id = input("\nEnter your user ID: ").upper()

            available = get_available_books(books)
            if not available:
                print("No books available to borrow.")
                continue

            print("\nAvailable Books:")
            for book in available:
                print(" -", book)

            book_id = input("\nEnter book ID to borrow: ").upper()
            try:
                borrow_book(users, books, user_id, book_id)
                save_books(books)
                save_users(users)
            except AssertionError as e:
                print("Error:", e)

        elif choice == "3":
            user_id = input("\nEnter your user ID: ").upper()

             # Check if user exists and has borrowed books
            if user_id not in users:
                print("Invalid user ID.")
                continue

            borrowed_list = users[user_id]["borrowed"]
            if not borrowed_list:
                print("You have not borrowed any books.")
                continue

            print("\nYour Borrowed Books:")
            for bid in borrowed_list:
                title = books[bid]["title"] if bid in books else "Unknown Title"
                print(f" - {bid}: {title}")

            book_id = input("\nEnter book ID to return: ").upper()
            try:
                return_book(users, books, user_id, book_id)
                save_books(books)
                save_users(users)
            except AssertionError as e:
                print("Error:", e)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")
