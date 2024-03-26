from fastapi import FastAPI, Request
from fastapi_keycloak import FastAPIKeycloak


app = FastAPI()
idp = FastAPIKeycloak(
    server_url="http://localhost:8080/",
    client_id="flaskr",
    client_secret="y5WWBskC8ZTRyE94mhKGW36XcCwf1vUq",
    admin_client_secret="p2ZVsANbkeWyq74Xq1U6AWHk6DSg37gd",
    callback_uri="http://localhost:8081/callback",
    realm="duyrealm"
)


@app.middleware("http")
async def authorize(request: Request, call_next):
    print(request)


@app.get("/")
async def root():
    return {"message": "Hello World"}