from flask import Flask, jsonify
from keycloak import KeycloakOpenID
import jwt

app = Flask(__name__)

# Configure client
keycloak_openid = KeycloakOpenID(server_url="http://localhost:8080/",
                                 client_id="flaskr",
                                 realm_name="duyrealm",
                                 client_secret_key='y5WWBskC8ZTRyE94mhKGW36XcCwf1vUq')

# config_well_known = keycloak_openid.well_known()

@app.route('/test', methods=('GET','POST'))
def test():
    data = keycloak_openid.token("duynm", "1")

    KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid.public_key() + "\n-----END PUBLIC KEY-----"
    options = {"verify_signature": True, "verify_exp": True}
    token_info = keycloak_openid.decode_token(data['access_token'], key=KEYCLOAK_PUBLIC_KEY, options=options)

    return jsonify(token_info)