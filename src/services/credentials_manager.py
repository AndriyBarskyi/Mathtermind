import os
import json
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CredentialsManager:
    """Manager for handling user credentials storage and retrieval."""
    
    # File to store encrypted credentials
    CREDENTIALS_FILE = os.path.join(os.path.expanduser("~"), ".mathtermind_credentials")
    
    @staticmethod
    def _get_encryption_key():
        """Generate an encryption key based on machine-specific information."""
        # Use a combination of machine-specific information as a salt
        # This is a simple approach - for production, consider more secure methods
        machine_info = os.path.expanduser("~") + os.name
        salt = hashlib.sha256(machine_info.encode()).digest()[:16]
        
        # Generate a key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        # Use a fixed passphrase - in production, this should be more secure
        key = base64.urlsafe_b64encode(kdf.derive(b"mathtermind_app_key"))
        return key
    
    @classmethod
    def save_credentials(cls, email, password):
        """Save user credentials to an encrypted file."""
        try:
            # Create encryption object
            key = cls._get_encryption_key()
            fernet = Fernet(key)
            
            # Encrypt the credentials
            credentials = {
                "email": email,
                "password": password
            }
            encrypted_data = fernet.encrypt(json.dumps(credentials).encode())
            
            # Save to file
            with open(cls.CREDENTIALS_FILE, "wb") as f:
                f.write(encrypted_data)
                
            return True
        except Exception as e:
            print(f"Error saving credentials: {str(e)}")
            return False
    
    @classmethod
    def load_credentials(cls):
        """Load user credentials from the encrypted file."""
        if not os.path.exists(cls.CREDENTIALS_FILE):
            return None
        
        try:
            # Read encrypted data
            with open(cls.CREDENTIALS_FILE, "rb") as f:
                encrypted_data = f.read()
            
            # Create decryption object
            key = cls._get_encryption_key()
            fernet = Fernet(key)
            
            # Decrypt the data
            decrypted_data = fernet.decrypt(encrypted_data)
            credentials = json.loads(decrypted_data.decode())
            
            return credentials
        except Exception as e:
            print(f"Error loading credentials: {str(e)}")
            # If there's an error, remove the potentially corrupted file
            if os.path.exists(cls.CREDENTIALS_FILE):
                try:
                    os.remove(cls.CREDENTIALS_FILE)
                except:
                    pass
            return None
    
    @classmethod
    def clear_credentials(cls):
        """Remove saved credentials."""
        if os.path.exists(cls.CREDENTIALS_FILE):
            try:
                os.remove(cls.CREDENTIALS_FILE)
                return True
            except Exception as e:
                print(f"Error clearing credentials: {str(e)}")
                return False
        return True 