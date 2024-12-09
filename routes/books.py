from flask import Blueprint, request, jsonify
from utils.pagination import paginate
from models import books

books_bp = Blueprint('books', __name__)

# Create a new book
@books_bp.route('/books', methods=['POST'])
def create_book():
    data = request.json
    book_id = len(books) + 1
    books[book_id] = {
        "id": book_id,
        "title": data["title"],
        "author": data["author"],
        "year": data["year"],
        "genre": data["genre"]
    }
    # Proceed with book creation
    return jsonify({"id": book_id, **books[book_id]}), 201


# Get all books with pagination
@books_bp.route('/books', methods=['GET'])
def get_books():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))
    paginated_books = paginate(list(books.values()), page, per_page)
    return jsonify(paginated_books), 200

# Search for books by title or author
@books_bp.route('/books/search', methods=['GET'])
def search_books():
    query = request.args.get("query", "").lower()
    filtered_books = [
        book for book in books.values()
        if query in book["title"].lower() or query in book["author"].lower()
    ]
    return jsonify(filtered_books), 200

# Update a book
@books_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if book_id not in books:
        return jsonify({"error": "Book not found"}), 404
    data = request.json
    books[book_id].update(data)
    return jsonify({"message": "Book updated", "book": books[book_id]}), 200

# Delete a book
@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    if book_id not in books:
        return jsonify({"error": "Book not found"}), 404
    del books[book_id]
    return jsonify({"message": "Book deleted"}), 200
