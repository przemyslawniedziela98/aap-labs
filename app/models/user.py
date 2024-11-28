from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils.logger import GlobalLogger
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """
    Represents a user in the application.
    """
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(128), nullable=False)

    def set_password(self, password: str) -> None:
        """
        Hashes the user's password and stores it.

        Args:
            password (str): The plain-text password to hash.
        """
        try:
            self.password_hash = generate_password_hash(password)
            GlobalLogger.log_info(f"Password hash successfully generated for user: {self.username}")
        except Exception as e:
            GlobalLogger.log_error(f"Error setting password for user {self.username}: {e}")
            raise

    def check_password(self, password: str) -> bool:
        """
        Verifies a given password against the stored password hash.

        Args:
            password (str): The plain-text password to verify.

        Returns:
            bool: True if the password matches the stored hash, False otherwise.
        """
        try:
            is_valid = check_password_hash(self.password_hash, password)
            if is_valid:
                GlobalLogger.log_info(f"Password verification successful for user: {self.username}")
            else:
                GlobalLogger.log_warning(f"Password verification failed for user: {self.username}")
            return is_valid
        except Exception as e:
            GlobalLogger.log_error(f"Error verifying password for user {self.username}: {e}")
            raise
