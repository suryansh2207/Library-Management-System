from routes.books import books_bp
from routes.members import members_bp
from utils.auth import verify_token
from flask import Flask, request, jsonify
import secrets

app = Flask(__name__)

# Register blueprints
app.register_blueprint(books_bp)
app.register_blueprint(members_bp)

@app.route('/token', methods=['GET'])
def get_token():
    return jsonify({'token': SECRET_TOKEN})

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Library Management System API!"})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized'}), 401

# Generate a random token on server start
SECRET_TOKEN = secrets.token_hex(16)
print(f"Generated Token: {SECRET_TOKEN}")  # Output the token for use

# Middleware to verify token
def verify_token(token):
    return token == SECRET_TOKEN

@app.before_request
def check_authentication():
    token = request.headers.get("Authorization")
    print(f"Received token: {token}")  # Debugging
    if not verify_token(token):
        return jsonify({"error": "Unauthorized"}), 401


# Middleware for token-based authentication
@app.before_request
def require_auth():
    token = request.headers.get("Authorization")
    print(f"Received token: {token}")  # Debugging line
    if not verify_token(token):
        print(f"Validation failed for token: {token}")  # Debugging line
        return jsonify({"error": "Unauthorized"}), 401
    print(f"Validation succeeded for token: {token}")  # Debugging line

@app.route('/test-auth')
def test_auth():
    token = request.headers.get("Authorization")
    return {"validation_result": verify_token(token), "received_token": token}



if __name__ == "__main__":
    app.run(debug=True)
