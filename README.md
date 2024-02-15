# Authix: Scalable Authentication Service

Welcome to **Authix**, an authentication service designed based on a [talk by
Brian Pontarelli](https://www.youtube.com/watch?v=SLc3cTlypwM).

Authix provides a comprehensive solution for user authentication, built on the
principles of JWT (pronounced 'jot') and refresh tokens.

## How do I run this?

```yml
version: "3.8"

services:
  authix:
    image: nymann/authix:latest
    networks:
      - authix
    environment:
      - AUTH_TITLE="Auth Service"
      - KEY_FOLDER="keys"
      - LOG_LEVEL=DEBUG
      - MONGODB_URL="mongodb://authix:test123@user_mongodb:27017"
      - PASSWORD__MAX_LENGTH=128
      - PASSWORD__MIN_LENGTH=12
      - PASSWORD__MIN_DIGITS=1
      - PASSWORD__MIN_LOWERCASE_CHARS=1
      - PASSWORD__MIN_SPECIAL_CHARS=1
      - PASSWORD__MIN_UPPERCASE_CHARS=1
      - PASSWORD__SYMBOLS='!@#$%^&*()[]-_=+{}\|";:<>,.'
      - REFRESH_REDIS="redis://:test123@refresh_redis:6379"
  refresh_redis:
    container_name: refresh_redis
    build:
      context: docker
      dockerfile: redis.Dockerfile
    networks:
      - authix
    volumes:
      - ./docker/redis.conf:/usr/local/etc/redis/redis.conf
      - /tmp/refresh_redis_data:/data
  user_mongodb:
    image: mongo:latest
    container_name: user_mongodb
    networks:
      - authix
    environment:
      MONGO_INITDB_ROOT_USERNAME: authix
      MONGO_INITDB_ROOT_PASSWORD: test123
    volumes:
      - /tmp/authix_mongo_db:/data/db
```

## Key Features

1. **User Registration**: Users can sign up using their email and password.
   Users are stored in MongoDB.

2. **User Login**: Upon successful login, users receive:

   - A JWT access token in the Authorization header for immediate access.
   - A longer-lived refresh token as an HTTP cookie for extended sessions.

3. **Access Token Management**: Generate new JWT access tokens using the
   provided refresh token, ensuring seamless user experiences.

4. **Public Key**: Services can verify JWTs independently via public key,
   thereby reducing inter-service network calls.

5. **Secure Logout**: Users are logged out by deleting their refresh token from
   storage, which thereby removes the possibility to create new access tokens.
   Furthermore, it informs all connected services via Kafka to reject JWTs from
   the logged-out user, that have been created prior to logging out.

6. **Token Lifespan**:
   - JWT access tokens are valid for 5 minutes.
   - Refresh tokens, stored in REDIS, last for 4 weeks.

## Diagrams

### User Perspective

```mermaid
graph TB
  A["User"] -- "Register" --> B["/register"]
  A -- "Login" --> C["/login"]
  C -- "JWT & Refresh Token" --> A
  A -- "Use Refresh Token" --> D["/access_token"]
  D -- "New JWT" --> A
  A -- "Logout" --> E["/logout"]
```

### Service Perspective

```mermaid
graph TB
  S["Service"] -- "Retrieve Public Key" --> PK["/public_key"]
  S -- "Verify JWT" --> V["Verify JWT using Public Key"]
  S -- "Handle Logout Broadcast" --> L["Reject soon-to-expire JWTs"]
```

## Performance

On a single computer, running Authix via uvicorn with 16 workers, expect:

Create 1K users

```
1000 /register

2.97 seconds
```

Create 1K users, and login each user.

```
1000 /register
1000 /login

6.28 seconds
```

Create 10 users, for each user login, and call `/access_token` 1K times.

```
10 /register
10 /login
10000 /access_token

3.43 seconds
```
