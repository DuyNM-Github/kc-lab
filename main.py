import re
from urllib.parse import urlparse

from fastapi import FastAPI, Request, Response
from keycloak import KeycloakOpenID, KeycloakPostError



app = FastAPI()
# Configure client
kc_handler = KeycloakOpenID(server_url="http://localhost:8080/",
                                 client_id="flaskr",
                                 realm_name="duyrealm",
                                 client_secret_key='y5WWBskC8ZTRyE94mhKGW36XcCwf1vUq')


@app.middleware("http")
async def authorize(request: Request, call_next):
    path = urlparse(str(request.url)).path
    path_compositions = path.split("/")[1:]

    if re.search("^\/auth\/[\w\/]+", path) is None:

        token = request.headers.get('Authorization')[7:]
        if token is None:
            return Response(status_code=401)
        
        resource = path_compositions[0]
        scopes = path_compositions[1:] if len(path_compositions) > 1 else None
        print("/".join(scopes))

        perm = f"/{resource}"
        if scopes is not None:
            perm = "#".join((perm, f"/{'/'.join(scopes)}"))

        try:
            evaluation = kc_handler.has_uma_access(token, permissions=perm)
            print(evaluation)
        except KeycloakPostError as err:
            return Response(status_code=401)

        if not evaluation.is_authorized or not evaluation.is_logged_in:
            return Response(status_code=401)
            

    response = await call_next(request)
    return response


@app.post("/auth/login")
async def login():
    return {"message": "Log In"}


@app.get("/gene/data")
async def data():
    return {"message": "Get gene data"}