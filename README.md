# Library Management System

A comprehensive web-based Library Management System built with Python Flask and SQLite.

## Features

- **User Authentication**: Separate login for librarians and regular users
- **Book Management**: Add, view, and manage books in the library
- **Loan Management**: Track book checkouts and returns
- **Search Functionality**: Search for books by title, author, or ISBN
- **Responsive Design**: Works on desktop and mobile devices

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd library-management-system
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Initialize the database:
   ```bash
   python
   >>> from app import app, db
   >>> with app.app_context():
   ...     db.create_all()
   ```

2. Run the development server:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to `http://localhost:5000`

## Default Accounts

- **Librarian** (Admin)
  - Username: librarian
  - Password: librarian123

## Project Structure

```
library-management-system/
├── app.py                 # Main application file
├── requirements.txt        # Python dependencies
├── instance/
│   └── library.db         # SQLite database (created after first run)
└── templates/             # HTML templates
    ├── base.html          # Base template
    ├── index.html         # Home page
    ├── login.html         # Login page
    ├── books.html         # Book listing page
    ├── add_book.html      # Add book form
    ├── librarian_dashboard.html  # Admin dashboard
    └── user_dashboard.html       # User dashboard
```

## Features in Detail

### For Librarians
- Add new books to the library
- View all books and their availability
- Track all active loans
- Manage book returns
- View overdue books

### For Regular Users
- Browse available books
- Check out available books
- View personal loan history
- Return borrowed books

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
