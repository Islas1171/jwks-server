# JWKS Server

## Overview

This project implements a simple JWKS (JSON Web Key Set) server with a RESTful API that provides public keys and signs JWT tokens.

### Endpoints

- `/jwks`: Returns the JWKS with public keys.
- `/auth`: Returns a JWT signed with an RSA key. Optionally returns an expired JWT when the `expired` query parameter is passed.

## How to Run

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the server: `python app.py`.
4. Access the API via `localhost:8080`.

## Example Requests

- Get public keys:
  ```bash
  curl http://localhost:8080/jwks
# jwks-server
