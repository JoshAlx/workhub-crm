# utils/password_hasher.py
import bcrypt

def hashear_password(password_plano):
    """Hashea una contraseña."""
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(password_plano.encode('utf-8'), salt)
    return hash_bytes.decode('utf-8') # Guardar como string

def verificar_password(password_plano, hash_guardado):
    """Verifica si el password plano coincide con el hash."""
    return bcrypt.checkpw(password_plano.encode('utf-8'), hash_guardado.encode('utf-8'))