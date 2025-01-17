from fastapi import FastAPI, HTTPException, Response, Depends # type: ignore
from passlib.context import CryptContext # type: ignore
from datetime import timedelta
from models import UserIn, UserOut, LoginRequest
from database import users_collection
from auth import create_access_token, verify_token

app = FastAPI()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Helper functions
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/signup", response_model=UserOut)
async def signup(user_in: UserIn):
    # Check if user exists
    existing_user = users_collection.find_one({"username": user_in.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Hash password
    hashed_password = hash_password(user_in.password)
    
    # Insert user into DB
    user_data = {
        "username": user_in.username,
        "email": user_in.email,
        "password": hashed_password
    }
    result = users_collection.insert_one(user_data)
    
    # Return user information (without password)
    user_in_db = users_collection.find_one({"_id": result.inserted_id})
    return UserOut(username=user_in_db["username"], email=user_in_db["email"])


@app.post("/login")
async def login(login_req: LoginRequest, response: Response):
    # Check if user exists
    user_in_db = users_collection.find_one({"username": login_req.username})
    if not user_in_db:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Verify password
    if not verify_password(login_req.password, user_in_db["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Create JWT token
    access_token = create_access_token(data={"sub": login_req.username})
    
    # Set the JWT token in an HTTP cookie
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True,  # The cookie is only accessible by the server
        max_age=timedelta(hours=1),  # Expiration time for the token
        secure=True,  # Only set cookie over HTTPS, set to False for development without HTTPS
        samesite="Lax"  # Helps prevent CSRF attacks
    )
    
    # Return success message and token
    return {
        "msg": "Login successful", 
        "access_token": access_token, 
        "token_type": "bearer"
    }


@app.post("/logout")
async def logout(response: Response):
    # Clear the access token cookie
    response.delete_cookie("access_token")
    return {"msg": "Logged out successfully"}

# Dependency to get token from cookies for protected routes
def get_token_from_cookies(request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing from cookies")
    return token

# Protected route example
@app.get("/protected")
async def protected_route(token: str = Depends(get_token_from_cookies)):
    # Verify the token
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # Your protected route logic
    return {"msg": "This is a protected route", "user": payload["sub"]}
