
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Dummy data
books_db = [
    {"id": 1, "title": "Flask for Beginners", "author": "John Doe"},
    {"id": 2, "title": "Advanced Python", "author": "Jane Smith"}
]

reviews_db = []

# Route Methods

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books_db)


@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    required_keys = {"id", "title", "author"}

    if not data or not required_keys.issubset(data):
        return jsonify({"error": "Invalid book data"}), 400

    books_db.append(data)
    return jsonify(data), 201


# Route Variables
@app.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books_db if b["id"] == book_id), None)
    return jsonify(book) if book else ('Not Found', 404)


@app.route('/login', methods=['GET', 'POST'])
def login():
    VALID_USERNAME = "admin"
    VALID_PASSWORD = "secret"

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            return f"Logged in as {username}", 200
        else:
            return "Invalid credentials", 401
    return render_template("login.html")


@app.route('/api/review', methods=['POST'])
def post_review():
    review_data = request.get_json()

    # Check if 'book_id' is present and equals 1
    if review_data.get('book_id') != 1:
        return jsonify({"error": "Reviews only allowed for book with id=1"}), 400

    # Add review to the database (list)
    reviews_db.append(review_data)
    return jsonify(review_data), 201


@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    return jsonify(reviews_db)

# Home page using base template
@app.route('/')
def home():
    return render_template("home.html", books=books_db)

if __name__ == '__main__':
    app.run(debug=True)
