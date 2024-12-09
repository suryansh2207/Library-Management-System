import secrets

# Generate a random token when the server starts
SECRET_TOKEN = secrets.token_hex(16)

def verify_token(token):
    return token == SECRET_TOKEN