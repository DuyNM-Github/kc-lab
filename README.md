Proof of Concept and Demo for implementing RBAC with Keycloak and FastAPI. 
With FastAPI act as the primary validator and Keycloak as the primary Identity Provider.

# Flask configuration (app.py)
Used primarily for authenticating and receiving tokens
```
flask --app app run --debug 
```

# FastAPI configuration (main.py)
Used for testing the authorization validation
```
unvicorn main:app --reload
```

# Keycloak Configurations
- Realm configuration: kc_samle.json
- Authorization configuration: sample-authz-config.json
