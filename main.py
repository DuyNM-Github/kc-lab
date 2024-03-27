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
config_well_know = kc_handler.well_known()


@app.middleware("http")
async def authorize(request: Request, call_next):
    path = urlparse(str(request.url)).path
    path_compositions = path.split("/")[1:]
    print(path_compositions)

    if re.search("^\/auth\/[\w\/]+", path) is None:

        token = request.headers.get('Authorization')[7:]
        if token is None:
            return Response(status_code=401)
        
        resource = path_compositions[0]
        scopes = path_compositions[1:] if len(path_compositions) > 1 else None
        print("/".join(scopes))

        # print(kc_handler.uma_permissions(token))
        perm = f"/{resource}"
        if scopes is not None:
            perm = "#".join((perm, f"/{'/'.join(scopes)}"))
        print(perm)
        print(kc_handler.has_uma_access(token, permissions="Empty"))


    response = await call_next(request)
    return response


@app.get("/qa/somethingelse/otherthing")
async def root():
    return {"message": "Hello World"}