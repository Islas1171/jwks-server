# JWKS Server in Python
This project implements a simple JWKS server using Flask, JWT, and RSA keys. It provides an authentication endpoint to issue JWTs and serves public keys in JWKS format.
## Need to download
- Python
- Flask
- PyJWT
- Cryptography
1. Clone the repository:
    git clone https://github.com/<your-repo>/jwks-server-python.git
    cd jwks-server-python
2. Install the required packages:
    pip install Flask pyjwt cryptography
3. Run the Flask server:
    python jwks_server.py
The server will start on `http://localhost:8080`.
## Endpoints
### `/jwks` (GET)
Returns the public RSA keys in JWKS format.
curl http://localhost:8080/jwks
