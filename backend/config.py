"""
PolicySonar configuration using only Python standard library
"""
import os

# Environment variables loader (simplified dotenv replacement)
def load_env():
    try:
        with open('.env') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    except FileNotFoundError:
        pass

load_env()

# API credentials
SONAR_API_KEY = os.getenv("SONAR_API_KEY")

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "policysonar"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}
