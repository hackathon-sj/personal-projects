import streamlit as st
import pandas as pd
from datetime import date

# Initialize the borrower data
if "borrower_data" not in st.session_state:
    st.session_state.borrower_data = pd.DataFrame(columns=["Name", "Book Title", "Borrow Date", "Return Date"])

# Initialize the library data
if "library_data" not in st.session_state:
    st.session_state.library_data = pd.DataFrame(columns=["Title", "Author", "Genre", "Year"])

st.title("Library App")

# Sidebar for navigation
menu = st.sidebar.selectbox("Menu", ["Home", "Add Book", "View Library", "Lend Book"])

if menu == "Home":
    st.write("Welcome to the Archit's Library App!This is fun place to read all the amazing books")
    st.write("Use the sidebar to navigate.")

elif menu == "Add Book":
    st.subheader("Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        genre = st.text_input("Genre")
        year = st.number_input("Year", min_value=0, step=1)
        submitted = st.form_submit_button("Add Book")
        if submitted:
            new_book = {"Title": title, "Author": author, "Genre": genre, "Year": year}
            st.session_state.library_data = pd.concat([st.session_state.library_data, pd.DataFrame([new_book])], ignore_index=True)
            st.success("Book added successfully!")

elif menu == "View Library":
    st.subheader("Library Collection")
    if st.session_state.library_data.empty:
        st.write("No books in the library yet.")
    else:
        st.dataframe(st.session_state.library_data)

elif menu == "Lend Book":
    st.subheader("Lend a Book")
    if st.session_state.library_data.empty:
        st.write("No books available to lend.")
    else:
        with st.form("lend_book_form"):
            borrower_name = st.text_input("Borrower's Name")
            book_title = st.selectbox("Select a Book to Lend", st.session_state.library_data["Title"].unique())
            borrow_date = st.date_input("Borrow Date", value=date.today())
            return_date = st.date_input("Return Date")
            submitted = st.form_submit_button("Lend Book")
            if submitted:
                # Add the lending record
                new_borrower = {
                    "Name": borrower_name,
                    "Book Title": book_title,
                    "Borrow Date": borrow_date,
                    "Return Date": return_date,
                }
                st.session_state.borrower_data = pd.concat([st.session_state.borrower_data, pd.DataFrame([new_borrower])], ignore_index=True)
                # Remove the book from the library
                st.session_state.library_data = st.session_state.library_data[st.session_state.library_data["Title"] != book_title]
                st.success(f"Book '{book_title}' lent to {borrower_name} successfully!")