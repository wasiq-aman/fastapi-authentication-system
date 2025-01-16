# import jwt # type: ignore
# from datetime import datetime, timedelta
# import os
# from dotenv import load_dotenv # type: ignore

# # Load environment variables
# load_dotenv()

# # Secret key and algorithm
# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = "HS256"

# # Function to create JWT token
# def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# # Function to verify JWT token
# def verify_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except jwt.ExpiredSignatureError:
#         return None
#     except jwt.JWTError:
#         return None



import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Secret key and algorithm
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify JWT token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None
