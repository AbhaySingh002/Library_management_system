import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from library_system import Book, User, Issue

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.hdqwalls.com/download/hard-candy-trap-4k-8r-3840x2160.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: black;
    }
    .sidebar-content {
        color: black;
        font-weight: bold;
    }
    .title-text {
        color: black;
        font-size: 2.5em;
    }
    .divider {
        margin-top: 1em;
        margin-bottom: 1em;
        height: 2px;
        background-color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header 
st.markdown('<div class="title-text">📚 Welcome to the Enhanced Library Management System</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Sidebar 
st.sidebar.markdown('<div class="sidebar-content">Library Functions</div>', unsafe_allow_html=True)

tab = st.sidebar.radio("Select a Function", ["Manage Books", "Manage Users", "Issue/Return Books", "View Borrowing Stats"])

# Book Management 
if tab == "Manage Books":
    st.subheader("📘 Book Management")
    action = st.selectbox("Choose Action", ("Add Book", "Remove Book", "Display Books"))
    
    if action == "Add Book":
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        title = st.text_input("Enter Book Title")
        author = st.text_input("Enter Author")
        book_id = st.text_input("Enter Book ID")
        if st.button("Add Book"):
            if title and author and book_id:
                Book.add_book(title, author, book_id)
                st.success(f'Book "{title}" added successfully.')
                
    elif action == "Remove Book":
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        book_id = st.text_input("Enter Book ID to Remove")
        if st.button("Remove Book"):
            Book.remove_book(book_id)
            st.success(f"Book with ID '{book_id}' removed successfully.")
    
    elif action == "Display Books":
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.subheader("📚 Books Available in Library")
        books = Book.display_books()
        st.dataframe(books)

# User Management Section
elif tab == "Manage Users":
    st.subheader("👥 User Management")
    user_action = st.selectbox("User Action", ("Add User", "Display Users"))

    if user_action == "Add User":
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        name = st.text_input("Enter User Name")
        user_id = st.text_input("Enter User ID")
        if st.button("Add User"):
            if name and user_id:
                User.add_user(name, user_id)
                st.success(f"User '{name}' added successfully.")

    elif user_action == "Display Users":
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.subheader("👥 Registered Users")
        users = User.display_users()
        st.dataframe(users)

# Book Issuing and Returning Section
elif tab == "Issue/Return Books":
    st.subheader("🔄 Issue & Return Books")
    issue_action = st.selectbox("Choose Action", ("Borrow Book", "Return Book", "View Issued Books"))

    if issue_action == "Borrow Book":
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        user_id = st.text_input("User ID")
        book_id = st.text_input("Book ID")
        if st.button("Borrow Book"):
            result = Issue.borrow_book(user_id, book_id)
            st.success(result)

    elif issue_action == "Return Book":
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        user_id = st.text_input("User ID")
        book_id = st.text_input("Book ID")
        if st.button("Return Book"):
            result = Issue.return_book(user_id, book_id)
            st.success(result)

    elif issue_action == "View Issued Books":
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        issued_books_df = Issue.display_issued_books()
        if isinstance(issued_books_df, str):
            st.info(issued_books_df)
        else:
            st.dataframe(issued_books_df)

# Stats Graph
elif tab == "View Borrowing Stats":
    st.subheader("📊 Borrowing Statistics")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.write("Overview of books borrowed by each user.")
    fig, ax = plt.subplots()
    sns.barplot(data=User.users.reset_index(), x='Name', y='Number of Book issued', palette="viridis", ax=ax)
    ax.set_title("Books Borrowed per User")
    ax.set_xlabel("User Name")
    ax.set_ylabel("Number of Books Borrowed")
    st.pyplot(fig)

    st.write("See trends and patterns in library usage.")