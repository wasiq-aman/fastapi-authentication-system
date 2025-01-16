# from pymongo import MongoClient # type: ignore
# import os
# from dotenv import load_dotenv # type: ignore

# # Load environment variables from .env file
# load_dotenv()

# # MongoDB URI from .env file
# MONGO_URI = os.getenv("MONGO_URI")
# client = MongoClient(MONGO_URI)

# # Database and collection setup
# db = client['mydatabase']
# users_collection = db['users']


from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB URI from .env file
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

# Database and collection setup
db = client['mydatabase']
users_collection = db['users']
