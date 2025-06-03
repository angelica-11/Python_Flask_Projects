from flask import Flask, url_for, redirect, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Book model definition
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

# Create the database (run only once)
db.create_all()

# ------------------ HTML ROUTES ------------------ #

@app.route('/')
def home():
    books = db.session.query(Book).all()
    return render_template("index.html", books=books)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        try:
            book_name = request.form['book-name']
            book_author = request.form['book-author']
            book_rating = request.form['book-rating']
        except KeyError:
            return "Missing form data", 400

        new_book = Book(title=book_name, author=book_author, rating=book_rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add.html")

@app.route("/edit_book/<int:id>", methods=["GET", "POST"])
def edit_book(id):
    book = Book.query.get(id)
    if not book:
        return "Book not found", 404

    if request.method == "POST":
        try:
            new_rating = request.form['new-book-rating']
        except KeyError:
            return "Missing form data", 400

        book.rating = new_rating
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit_book.html", book=book)

@app.route("/delete")
def delete_book():
    book_id = request.args.get('id')
    book = Book.query.get(book_id)
    if not book:
        return "Book not found", 404

    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))

# ------------------ REST API ROUTES ------------------ #

@app.route("/api/books", methods=["GET"])
def get_all_books():
    books = Book.query.all()
    return jsonify(books=[{
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "rating": book.rating
    } for book in books]), 200

@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "rating": book.rating
        }), 200
    return jsonify(error="Book not found"), 404

@app.route("/api/books", methods=["POST"])
def add_book_api():
    title = request.args.get("title")
    author = request.args.get("author")
    rating = request.args.get("rating")

    if not title or not author or not rating:
        return jsonify(error="Missing data"), 400

    try:
        rating = float(rating)
    except ValueError:
        return jsonify(error="Invalid rating value"), 400

    new_book = Book(title=title, author=author, rating=rating)
    db.session.add(new_book)
    db.session.commit()
    return jsonify(message="Book added successfully"), 201

@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify(error="Book not found"), 404

    title = request.args.get("title")
    author = request.args.get("author")
    rating = request.args.get("rating")

    if title:
        book.title = title
    if author:
        book.author = author
    if rating:
        try:
            book.rating = float(rating)
        except ValueError:
            return jsonify(error="Invalid rating value"), 400

    db.session.commit()
    return jsonify(message="Book updated successfully"), 200

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book_api(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify(error="Book not found"), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify(message="Book deleted successfully"), 200

# ------------------ MAIN ------------------ #

if __name__ == "__main__":
    app.run(debug=True)
