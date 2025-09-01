from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_librarian = db.Column(db.Boolean, default=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=14))
    return_date = db.Column(db.DateTime, nullable=True)
    book = db.relationship('Book', backref='loans')
    user = db.relationship('User', backref='loans')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        
        if user:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_librarian:
        books = Book.query.all()
        loans = Loan.query.filter_by(return_date=None).all()
        return render_template('librarian_dashboard.html', books=books, loans=loans)
    else:
        user_loans = Loan.query.filter_by(user_id=current_user.id, return_date=None).all()
        return render_template('user_dashboard.html', loans=user_loans)

@app.route('/books')
@login_required
def books():
    search = request.args.get('search', '')
    if search:
        books = Book.query.filter(Book.title.contains(search) | Book.author.contains(search) | Book.isbn.contains(search)).all()
    else:
        books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/checkout/<int:book_id>', methods=['POST'])
@login_required
def checkout(book_id):
    book = Book.query.get_or_404(book_id)
    if book.available_copies > 0:
        book.available_copies -= 1
        loan = Loan(user_id=current_user.id, book_id=book.id)
        db.session.add(loan)
        db.session.commit()
        flash('Book checked out successfully!')
    else:
        flash('No copies available for checkout')
    return redirect(url_for('books'))

@app.route('/return/<int:loan_id>', methods=['POST'])
@login_required
def return_book(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    if loan.user_id == current_user.id or current_user.is_librarian:
        loan.return_date = datetime.utcnow()
        loan.book.available_copies += 1
        db.session.commit()
        flash('Book returned successfully!')
    return redirect(url_for('dashboard'))

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if not current_user.is_librarian:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        copies = int(request.form.get('copies', 1))
        
        book = Book(title=title, author=author, isbn=isbn, 
                   total_copies=copies, available_copies=copies)
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('add_book.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create a default librarian if not exists
        if not User.query.filter_by(username='librarian').first():
            librarian = User(username='librarian', password='librarian123', is_librarian=True)
            db.session.add(librarian)
            db.session.commit()
    app.run(debug=True)
