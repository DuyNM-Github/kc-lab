from flask import Flask, jsonify, Response, request, make_response
from keycloak import KeycloakOpenID, KeycloakPostError
import re
import functools

app = Flask(__name__)

# Configure client
keycloak_openid = KeycloakOpenID(server_url="http://localhost:8080/",
                                 client_id="flaskr",
                                 realm_name="duyrealm",
                                 client_secret_key='y5WWBskC8ZTRyE94mhKGW36XcCwf1vUq')
config_well_know = keycloak_openid.well_known()

# config_well_known = keycloak_openid.well_known()

@app.before_request
def auth():
    print(request.path)
    print()
    if re.search('test', request.path) is None:
        if request.headers.get('Authorization') is None:
            return Response(status=401)
        
        KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid.public_key() + "\n-----END PUBLIC KEY-----"
        options = {"verify_signature": True, "verify_exp": True}
        token_info = keycloak_openid.decode_token(request.headers.get('Authorization')[7:], key=KEYCLOAK_PUBLIC_KEY, options=options)

        print(token_info['realm_access']['roles'])

        print(keycloak_openid.uma_permissions(request.headers.get('Authorization')[7:]))
        # print(keycloak_openid.)
        
        try:
            auth_status = keycloak_openid.has_uma_access(
                request.headers.get('Authorization')[7:],
                "Audit#/rnd"
            )
            print(auth_status)
        except KeycloakPostError:
            return Response(status=401)
        # print(request.headers.get('Authorization')[7:])
    


@app.route('/test', methods=('GET','POST'))
def test():
    data = keycloak_openid.token("test", "1")

    return jsonify(data)


@app.route('/rnd', methods=('GET','POST'))
def rnd():
    rq = request.get_json()
    return jsonify(rq)


