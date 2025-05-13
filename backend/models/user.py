"""
SQLAlchemy User model with password hashing using standard library
"""
import hashlib
import secrets
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(128))
    salt = Column(String(32))
    role = Column(String(20), default="analyst")  # analyst, policymaker, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    def verify_password(self, plain_password: str) -> bool:
        """Verify password against stored hash using PBKDF2-HMAC-SHA256"""
        if not self.salt or not self.hashed_password:
            return False
        derived_key = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            self.salt.encode('utf-8'),
            100000
        )
        return derived_key.hex() == self.hashed_password
    
    @staticmethod
    def get_password_hash(password: str) -> tuple[str, str]:
        """Generate password hash and salt using PBKDF2-HMAC-SHA256"""
        salt = secrets.token_hex(16)
        derived_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return (derived_key.hex(), salt)
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"
