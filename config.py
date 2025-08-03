import os
from dotenv import load_dotenv

# Load environment variables from a .env file for local development
load_dotenv()

# Fetch the database URL from the environment variables.
# This is the connection string you get from your Supabase project settings.
DATABASE_URL = os.getenv('postgresql://postgres:[YOUR-PASSWORD]@db.kzsmflqtsqqgsxbufhxu.supabase.co:5432/postgres')

# Raise an error if the DATABASE_URL is not set, to prevent the app from running with a missing configuration.
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for Flask application")

