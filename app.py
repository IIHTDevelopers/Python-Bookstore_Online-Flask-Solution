
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Dummy data
books_db = [
    {"id": 1, "title": "Flask for Beginners", "author": "John Doe"},
    {"id": 2, "title": "Advanced Python", "author": "Jane Smith"}
]

reviews_db = []

# Route Methods
@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        return jsonify(books_db)
    elif request.method == 'POST':
        data = request.json
        books_db.append(data)
        return jsonify(data), 201

# Route Variables
@app.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books_db if b["id"] == book_id), None)
    return jsonify(book) if book else ('Not Found', 404)

# Query String
@app.route('/search')
def search():
    keyword = request.args.get('q', '').lower()
    results = [b for b in books_db if keyword in b['title'].lower()]
    return jsonify(results)


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


# JSON Data
@app.route('/api/review', methods=['POST'])
def post_review():
    review_data = request.get_json()
    reviews_db.append(review_data)
    return jsonify(review_data), 201

# Home page using base template
@app.route('/')
def home():
    return render_template("home.html", books=books_db)

if __name__ == '__main__':
    app.run(debug=True)
