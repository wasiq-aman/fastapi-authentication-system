# Load environment variables from .env file
import os


load_dotenv() # type: ignore
# Secret key and algorithm for JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
