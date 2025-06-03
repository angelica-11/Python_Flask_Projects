# Virtual Bookshelf – REST API Project

This is a Flask-based web app and REST API for managing a personal virtual bookshelf. It allows users to add, view, edit, and delete book entries through both HTML forms and a RESTful API.

---

## Features

- Add, edit, delete books via web interface
- Full REST API (GET, POST, PUT, DELETE)
- Status code handling (`200`, `201`, `400`, `404`)
- SQLite database using SQLAlchemy
- Environment variables with `python-dotenv`
- Clean, modular Flask application

---

## REST API Endpoints

| Method   | Endpoint              | Description         |
|----------|-----------------------|---------------------|
| `GET`    | `/api/books`          | Get all books       |
| `GET`    | `/api/books/<id>`     | Get a specific book |
| `POST`   | `/api/books`          | Add a new book      |
| `PUT`    | `/api/books/<id>`     | Update book data    |
| `DELETE` | `/api/books/<id>`     | Delete a book       |

---

##  How to Test the API

###  Example: Add a New Book (POST)

```bash
POST /api/books?title=Test+Book&author=Jane+Doe&rating=4.5
```

### Example: Update a Book (PUT)

```bash
PUT /api/books/2?rating=9.9
```

### Example: Delete a Book (DELETE)

```bash
DELETE /api/books/2
```

 Use tools like **Postman** or `curl` to send requests.

---

## How to Run the Project

### Requirements

- Python 3.11
- Flask
- Flask-SQLAlchemy
- python-dotenv

### Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/your-username/Virtual_Bookshelf_API.git
cd Virtual_Bookshelf_API

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python main.py
```

Open your browser and go to:  
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🗂 Project Structure

```
 07_Virtual_Bookshelf/
├── main.py                # Main Flask app
├── templates/             # HTML templates
├── books-collection.db    # SQLite database
├── .env                   # (optional) Environment variables
├── requirements.txt       # List of packages
└── README.md              # Project documentation
```

---

That’s it! This project was built using Flask and includes a fully functional REST API.
