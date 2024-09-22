from flask import Flask, jsonify, request
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import datetime
import uuid
app = Flask(__name__)
def generate_rsa_key():
    private_key = rsa.generate_private_key( #generate the private key
        public_exponent=65537,
        key_size=2048
    )
    kid = str(uuid.uuid4())  # Generate a unique Key ID (kid)
    expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)  # Key will expiry in 1 hour
    public_key_pem = private_key.public_key().public_bytes( # public key for the code
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    return {
        'kid': kid, #kid
        'private_key': private_key,
        'public_key': public_key_pem,
        'expiry': expiry
    }
# Generate 2 RSA keys for testing
keys = [generate_rsa_key() for _ in range(2)]
def create_jwt(kid, private_key, expired=False):
    now = datetime.datetime.now(datetime.timezone.utc) #changed the time zone to fit the require testing
    expiry_time = now - datetime.timedelta(minutes=5) if expired else now + datetime.timedelta(minutes=15)
    token = jwt.encode({ #token for the characters in the code
        'sub': '1234567890',
        'name': 'John Doe',
        'iat': now.timestamp(),
        'exp': expiry_time.timestamp(),
    }, private_key, algorithm='RS256', headers={'kid': kid})
    return token
def get_jwks():
    jwks = {"keys": []} #empty JWKS structure
    for key in keys:
        if key['expiry'] > datetime.datetime.now(datetime.timezone.utc): #checks if key has not expired
            jwks['keys'].append({
                "kid": key['kid'],
                "kty": "RSA",
                "alg": "RS256",#refers to RSA signature with SHA-256
                "use": "sig", #key used to sign JWTs
                "n": jwt.utils.base64url_encode(
                    #acess the public part of RSA key, and extracts n(modulus)
                    key['private_key'].public_key().public_numbers().n.to_bytes(256, 'big') #converts 256 bytes in big-endian format
                ).decode('utf-8'), #converts Base 64 encoded bytes into UTF-8 string
                #e is the exponent of the code
                "e": jwt.utils.base64url_encode(b'\x01\x00\x01').decode('utf-8')
            })
    return jwks

@app.route('/jwks', methods=['GET']) #only accepts HTTP Get request
def jwks():
    return jsonify(get_jwks()) #function that converts into a JSON response
@app.route('/auth', methods=['POST'])
def auth():
    expired = request.args.get('expired', 'false') == 'true' #if not present false
    selected_key = None

    if expired:
        for key in keys: #iterates over all keys
            if key['expiry'] < datetime.datetime.now(datetime.timezone.utc): #compares the key's timestamp with the current UTC time
                selected_key = key #the first key found
                break
    else:
        #selects a non-expired key
        for key in keys:
            if key['expiry'] > datetime.datetime.now(datetime.timezone.utc):
                selected_key = key
                break
#no valid key is found
    if not selected_key:
        return jsonify({"error": "No valid key found"}), 500
#calls function to generate a JWT token
    token = create_jwt(selected_key['kid'], selected_key['private_key'], expired=expired)
    return jsonify({"token": token}) #returns a JSON response which contains the generated JWT
if __name__ == '__main__':
    app.run(port=8080) #run localhost 8080