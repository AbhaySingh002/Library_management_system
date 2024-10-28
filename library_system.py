# library_system.py

import pandas as pd
from datetime import timedelta

class Book:
    books = pd.DataFrame(columns=['Title', 'Author', 'is_borrowed', 'Book ID']).set_index('Book ID')
    
    @classmethod
    def add_book(cls, title, author, book_id):
        new_book = pd.DataFrame({'Title': [title], 'Author': [author], 'is_borrowed': [False]}, index=[book_id])
        cls.books = pd.concat([cls.books, new_book])
        return f'Book "{title}" added successfully'
        
    @classmethod
    def remove_book(cls, book_id):
        cls.books.drop(book_id, errors='ignore', inplace=True)
        return f'Book ID {book_id} removed successfully.'
        
    @classmethod
    def display_books(cls):
        return cls.books
        

class User:
    users = pd.DataFrame(columns=['Name', 'User ID', 'Number of Book issued']).set_index('User ID')
    
    @classmethod
    def add_user(cls, name, user_id):
        new_user = pd.DataFrame({'Name': [name], 'Number of Book issued': [0]}, index=[user_id])
        cls.users = pd.concat([cls.users, new_user])
        return f'{name} is successfully added to the User list.'
    
    @classmethod    
    def display_users(cls):
        return cls.users


class Issue:
    issued_books = pd.DataFrame(columns=['User ID', 'Book ID', 'Time', 'Due Date'])
    
    @classmethod
    def borrow_book(cls, user_id, book_id):
        if user_id not in User.users.index:
            return 'User not found 🥺! Please add the user first.'
        if book_id not in Book.books.index:
            return 'Book not found 🥺!'
        if Book.books.at[book_id, 'is_borrowed']:
            return f'The book with ID "{book_id}" is already borrowed.'
        
        issue_time = pd.Timestamp.now()
        Book.books.at[book_id, 'is_borrowed'] = True
        due_date = issue_time + timedelta(days=14)
        issuing = pd.DataFrame({'User ID': [user_id], 'Book ID': [book_id], 'Time': [issue_time], 'Due Date': [due_date]})
        cls.issued_books = pd.concat([cls.issued_books, issuing], ignore_index=True)

        book_title = Book.books.at[book_id, 'Title']
        user_name = User.users.at[user_id, 'Name']
        User.users.at[user_id, 'Number of Book issued'] += 1
        return f'Book "{book_title}" borrowed by {user_name}.'
    
    @classmethod
    def display_issued_books(cls):
        if cls.issued_books.empty:
            return "No books have been issued yet 🙄 ."
        return cls.issued_books

        
    @classmethod
    def return_book(cls, user_id, book_id):
        borrowed_row = cls.issued_books[(cls.issued_books['User ID'] == user_id) & (cls.issued_books['Book ID'] == book_id)]
        
        if borrowed_row.empty:
            return "This user has not borrowed this book 🥺."
        
        cls.issued_books.drop(borrowed_row.index, inplace=True)
        Book.books.at[book_id, 'is_borrowed'] = False
        User.users.at[user_id, 'Number of Book issued'] -= 1
        return f'Book with ID "{book_id}" has been returned by user with ID {user_id}.'