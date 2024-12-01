from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access the environment variables
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL is not set in the .env file")
